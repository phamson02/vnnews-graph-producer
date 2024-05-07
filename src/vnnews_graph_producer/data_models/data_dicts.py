from typing import TypedDict


class NodeData(TypedDict):
    key: str
    label: str
    tag: str
    x: str
    y: str
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


class GraphData(TypedDict):
    nodes: list[NodeData]
    edges: list[EdgeData]
