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


def ner(text: str, lowercase: bool, threshold: float) -> list[dict[str, Any]]:
    nlp = pipeline("ner", model=model, tokenizer=tokenizer, config=config)

    if lowercase:
        text = text.lower()
    ner_results = nlp(text)

    assert isinstance(ner_results, list)

    # Filter out entities with confidence below the threshold
    ner_results = [e for e in ner_results if e["score"] >= threshold]

    for e in ner_results:
        e["word"] = text[e["start"] : e["end"]]

    return ner_results


def get_entities_from_text(
    text: str,
    lowercase: bool = False,
    threshold: float = 0.9,
) -> list[Entity]:
    """
    Extract Named Entity Recognition (NER) data from the text.
    """
    entities: set[Entity] = set()  # Use set to ensure unique entities

    try:
        ner_results = ner(text, lowercase, threshold)
        new_entities = process_entities(ner_results, text)
        entities.update(new_entities)
    except Exception as e:
        print(f"Error in NER processing: {e}")

    return list(entities)


def process_entities(ner_results: list[dict[str, Any]], text: str) -> list[Entity]:
    """
    Process NER results to filter, combine entities, and extract unique entities.
    """
    combined_entities: list[Entity] = []
    current_entity_span: tuple[int, int] = (0, 0)
    current_type = None

    excluded_words: set[str] = set()

    extracted_types = [e.value for e in EntityType]

    for res_token in ner_results:
        start_idx = res_token["start"]
        end_idx = res_token["end"]
        entity_type: str = res_token["entity"]

        if entity_type.split("-")[1] in extracted_types:
            if (
                entity_type.startswith("B-")
                or current_type != entity_type.split("-")[1]
            ):
                finalize_current_entity(
                    combined_entities,
                    current_entity_span,
                    current_type,
                    excluded_words,
                    text,
                )
                current_entity_span = (start_idx, end_idx)
                current_type = entity_type.split("-")[1]
            elif (
                entity_type.startswith("I-")
                and current_type == entity_type.split("-")[1]
            ):
                current_entity_span = (current_entity_span[0], end_idx)
        else:
            # Finalize the current entity if the current token is not part of an entity
            finalize_current_entity(
                combined_entities,
                current_entity_span,
                current_type,
                excluded_words,
                text,
            )

    # Finalize the last entity if present
    finalize_current_entity(
        combined_entities, current_entity_span, current_type, excluded_words, text
    )

    return [
        entity
        for entity in combined_entities
        if (entity.name not in excluded_words) and is_valid_entity(entity)
    ]


def finalize_current_entity(
    combined_entities: list[Entity],
    current_entity_span: tuple[int, int],
    current_type: str | None,
    excluded_words: set[str],
    text: str,
):
    """
    Finalize the current entity and add it to the list of combined entities.
    """
    if ((current_entity_span[1] - current_entity_span[0]) > 0) and current_type:
        entity = text[current_entity_span[0] : current_entity_span[1]]
        entity = " ".join(entity.split())  # Remove extra spaces
        entity_type = current_type
        combined_entities.append(Entity(name=entity, type=EntityType(entity_type)))

        # Add subwords to the list of excluded words (e.g. "Nguyễn Văn A" -> "Nguyễn", "Văn", "A", "Nguyễn Văn", "Văn A")
        subwords = get_subwords(entity)
        excluded_words.update(subwords)

        # Clear current entity and type for the next one
        current_entity_span = (0, 0)
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
    if ", " in entity.name:
        return False

    return (entity.name[0].isalnum()) and (len(entity.name) > 1)
