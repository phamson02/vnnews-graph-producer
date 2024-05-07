from dataclasses import dataclass
from typing import Optional

from vnnews_graph_producer.data_models.article import Article
from vnnews_graph_producer.data_models.data_dicts import ArticleData, EdgeData
from vnnews_graph_producer.data_models.link import Link
from .entity import Entity


class SubNewsGraph:
    def __init__(
        self, nodes: list[Entity], links: Optional[dict[Link, set[Article]]] = None
    ):
        self.nodes = nodes
        self.links = links or {}

    @classmethod
    def full_graph_from_article(
        cls, nodes: list[Entity], article: Article
    ) -> "SubNewsGraph":
        assert len(nodes) == len(set(nodes)), "Nodes must be unique"
        links = {}
        for i, source in enumerate(nodes):
            for target in nodes[i + 1 :]:
                link = Link(source=source, target=target)
                links[link] = {article}
        return cls(nodes=nodes, links=links)

    def __add__(self, other: "SubNewsGraph") -> "SubNewsGraph":
        new_nodes = list(set(self.nodes + other.nodes))
        new_links = self.links.copy()

        for link, articles in other.links.items():
            if link in new_links:
                new_links[link] |= articles
            else:
                new_links[link] = articles

        return SubNewsGraph(nodes=new_nodes, links=new_links)

    def __repr__(self) -> str:
        return f"SubNewsGraph(\n\tnodes={self.nodes},\n\tlinks={self.links}\n)"


@dataclass(frozen=True)
class NewsGraph:
    nodes: list[Entity]
    links: list[EdgeData]

    @classmethod
    def from_subgraph(
        cls,
        sub_graph: SubNewsGraph,
        edge_size_threshold: int = 3,
    ) -> "NewsGraph":
        # Filter out edges with less than edge_size_threshold articles
        links = []
        node_set: set[Entity] = set()
        for link, articles in sub_graph.links.items():
            if len(articles) >= edge_size_threshold:
                key = (link.source.name + link.target.name).replace(" ", "-").lower()
                articles = [
                    ArticleData(
                        key=article.url,
                        title=article.title,
                        url=article.url,
                        date=article.published_date.strftime("%Y-%m-%d-%H-%M"),
                    )
                    for article in articles
                ]
                links.append(
                    EdgeData(
                        key=key,
                        source=link.source.name,
                        target=link.target.name,
                        size=len(articles),
                        articles=articles,
                    )
                )
                node_set.add(link.source)
                node_set.add(link.target)

        nodes = list(node_set)

        return cls(nodes=nodes, links=links)
