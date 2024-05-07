from dataclasses import dataclass

from .entity import Entity


@dataclass(frozen=True)
class Link:
    """Undirected link between two entities in the graph"""

    source: Entity
    target: Entity

    def __repr__(self) -> str:
        return f"Link(\n\tsource={self.source},\n\ttarget={self.target}\n)"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Link):
            return False

        return (self.source == other.source and self.target == other.target) or (
            self.source == other.target and self.target == other.source
        )

    def __hash__(self) -> int:
        # Sort the entities to ensure that the hash is the same for both directions
        entities = [self.source, self.target]
        entities.sort(key=lambda x: x.name)

        return hash((entities[0], entities[1]))
