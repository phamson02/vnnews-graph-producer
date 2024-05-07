from typing import Any

import transformers
from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline
from transformers.models.electra.configuration_electra import ElectraConfig

from vnnews_graph_producer.data_models.entity import Entity, EntityType

transformers.logging.set_verbosity(transformers.logging.CRITICAL)

config = ElectraConfig.from_pretrained(
    "nguyendangsonlam/lsg-ner-vietnamese-electra-base-1024"
)
model = AutoModelForTokenClassification.from_pretrained(
    "nguyendangsonlam/lsg-ner-vietnamese-electra-base-1024",
    trust_remote_code=True,
    config=config,
)
tokenizer = AutoTokenizer.from_pretrained(
    "nguyendangsonlam/lsg-ner-vietnamese-electra-base-1024"
)


def ner(text: str) -> list[dict[str, Any]]:
    nlp = pipeline("ner", model=model, tokenizer=tokenizer, config=config)
    ner_results = nlp(text)

    assert isinstance(ner_results, list)

    return ner_results


def get_entities_from_text(content: str) -> list[Entity]:
    """
    Extract Named Entity Recognition (NER) data from the content.
    """
    entities: set[Entity] = set()  # Use set to ensure unique entities

    try:
        ner_results = ner(content)
        new_entities = process_entities(ner_results)
        entities.update(new_entities)
    except Exception as e:
        print(f"Error in NER processing: {e}")

    return list(entities)


def process_entities(ner_results: list[dict[str, Any]]) -> list[Entity]:
    """
    Process NER results to filter, combine entities, and extract unique entities.
    """
    combined_entities: list[Entity] = []
    current_entity: list[str] = []
    current_type = None

    excluded_words: set[str] = set()

    extracted_types = [e.value for e in EntityType]

    for token in ner_results:
        word: str = token["word"]
        entity_type: str = token["entity"]

        if entity_type.split("-")[1] in extracted_types:
            if (
                entity_type.startswith("B-")
                or current_type != entity_type.split("-")[1]
            ):
                finalize_current_entity(
                    combined_entities, current_entity, current_type, excluded_words
                )
                current_entity = [word]
                current_type = entity_type.split("-")[1]
            elif (
                entity_type.startswith("I-")
                and current_type == entity_type.split("-")[1]
            ):
                current_entity.append(word)
        else:
            # Finalize the current entity if the current token is not part of an entity
            finalize_current_entity(
                combined_entities, current_entity, current_type, excluded_words
            )

    # Finalize the last entity if present
    finalize_current_entity(
        combined_entities, current_entity, current_type, excluded_words
    )

    return [
        entity
        for entity in combined_entities
        if (entity.name not in excluded_words) and is_valid_entity(entity)
    ]


def finalize_current_entity(
    combined_entities: list[Entity],
    current_entity: list[str],
    current_type: str | None,
    excluded_words: set[str],
):
    """
    Finalize the current entity and add it to the list of combined entities.
    """
    if current_entity and current_type:
        entity = " ".join(current_entity)
        entity_type = current_type
        combined_entities.append(Entity(name=entity, type=EntityType(entity_type)))

        # Add subwords to the list of excluded words (e.g. "Nguyễn Văn A" -> "Nguyễn", "Văn", "A", "Nguyễn Văn", "Văn A")
        subwords = get_subwords(entity)
        excluded_words.update(subwords)

        # Clear current entity and type for the next one
        current_entity = []
        current_type = None


def get_subwords(text: str) -> list[str]:
    """
    Get all possible subwords from a text.
    E.g. "Nguyễn Văn Anh B" -> ["Nguyễn", "Văn", "Anh", "B", "Nguyễn Văn", "Văn Anh", "Anh B", "Nguyễn Văn Anh", "Văn Anh B"]
    E.g. "Donald Trump" -> ["Donald", "Trump"]
    """
    words = text.split()
    subwords = []

    for i in range(len(words)):
        for j in range(i + 1, len(words) + 1):
            subwords.append(" ".join(words[i:j]))

    # Remove the text itself
    subwords.remove(text)

    return subwords


def is_valid_entity(entity: Entity) -> bool:
    """
    Check if an entity is valid based on certain criteria.
    """
    return (entity.name[0].isalnum()) and (len(entity.name) > 1)
