from dataclasses import dataclass
from enum import Enum

from vnnews_graph_producer.sanitize_text import remove_accents


class EntityType(Enum):
    Person = "PERSON"
    Organization = "ORGANIZATION"


@dataclass(frozen=True, order=True)
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

    def __hash__(self) -> int:
        return hash((remove_accents(self.name.lower()), self.type))

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "Entity":
        return cls(
            name=data["name"],
            type=EntityType(data["type"]),
        )

    def to_dict(self) -> dict[str, str]:
        return {
            "name": self.name,
            "type": self.type.value,
        }


@dataclass(frozen=True)
class EntityNode(Entity):
    name: str
    type: EntityType
    tag: str
    cluster: str
    score: float
