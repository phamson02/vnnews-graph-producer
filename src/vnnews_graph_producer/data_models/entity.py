from dataclasses import dataclass
from enum import Enum

from vnnews_graph_producer.sanitize_text import remove_accents


class EntityType(Enum):
    Person = "PERSON"
    Organization = "ORGANIZATION"


@dataclass(frozen=True)
class Entity:
    name: str
    type: EntityType

    def __repr__(self) -> str:
        return f"Entity(\n\tname={self.name},\n\ttype={self.type}\n)"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Entity):
            return False

        return (
            remove_accents(self.name.lower()) == remove_accents(other.name.lower())
            and self.type == other.type
        )
