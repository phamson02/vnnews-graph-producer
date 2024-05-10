from typing import TypedDict
from color_generator import generate


class NodeData(TypedDict):
    key: str
    label: str
    tag: str
    cluster: str
    score: float


class ArticleData(TypedDict):
    key: str
    title: str
    url: str
    date: str


class EdgeData(TypedDict):
    key: str
    source: str
    target: str
    size: int
    articles: list[ArticleData]


class ClusterData(TypedDict):
    key: str
    color: str
    clusterLabel: str


class Cluster:
    def __init__(self, label: str):
        self.key: str = str(hash(label))
        self.color: str = generate("no-mono").hex
        self.clusterLabel: str = label

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Cluster):
            return False

        return self.key == value.key

    def __hash__(self) -> int:
        return int(self.key)

    def to_dict(self) -> ClusterData:
        return ClusterData(
            key=self.key,
            color=self.color,
            clusterLabel=self.clusterLabel,
        )


class Tag(TypedDict):
    key: str
    image: str


class GraphData(TypedDict):
    date: str
    nodes: list[NodeData]
    edges: list[EdgeData]
    clusters: list[ClusterData]
    tags: list[Tag]
