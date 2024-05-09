from dataclasses import dataclass, field

from vnnews_graph_producer.data_models.article import Article

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
        return hash(hash(self.source) + hash(self.target))


@dataclass(frozen=True)
class WeightedLink(Link):
    source: Entity
    target: Entity
    size: int
    articles: list[Article] = field(hash=False)
