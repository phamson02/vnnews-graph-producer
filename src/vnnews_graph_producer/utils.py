from datetime import datetime

from vnnews_graph_producer.data_models.entity import Entity
from vnnews_graph_producer.sanitize_text import remove_accents


def date_from_str(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%Y-%m-%d-%H-%M")


def date_to_str(date: datetime) -> str:
    return date.strftime("%Y-%m-%d-%H-%M")


def hash_entity(entity: Entity) -> int:
    return hash((remove_accents(entity.name.lower()), entity.type))
