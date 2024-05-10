from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from vnnews_graph_producer.analytics import AnalyticsGraph
from vnnews_graph_producer.data_models.article import Article
from vnnews_graph_producer.data_models.data_dicts import (
    ArticleData,
    EdgeData,
    GraphData,
    NodeData,
    Tag,
)
from vnnews_graph_producer.data_models.link import Link, WeightedLink
from vnnews_graph_producer.utils import date_to_str, hash_entity
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
    links: list[WeightedLink]
    date: datetime

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
                links.append(
                    WeightedLink(
                        source=link.source,
                        target=link.target,
                        size=len(articles),
                        articles=list(articles),
                    )
                )
                node_set.add(link.source)
                node_set.add(link.target)

        nodes = list(node_set)

        date = datetime.now()

        return cls(nodes=nodes, links=links, date=date)

    def to_graph_data(self) -> GraphData:
        analytics_graph = AnalyticsGraph(graph_links=self.links)

        nodes = [
            NodeData(
                key=str(hash_entity(node)),
                label=node.name,
                tag=node.type.value,
                cluster=node.cluster,
                score=node.score,
            )
            for node in analytics_graph.entity_nodes
        ]

        edges = [
            EdgeData(
                key=str(hash(link)),
                source=str(hash_entity(link.source)),
                target=str(hash_entity(link.target)),
                size=link.size,
                articles=[
                    ArticleData(
                        key=str(hash(article)),
                        title=article.title,
                        url=article.url,
                        date=date_to_str(article.published_date),
                    )
                    for article in link.articles
                ],
            )
            for link in self.links
        ]

        clusters = [cluster.to_dict() for cluster in analytics_graph.clusters]

        tags = [
            Tag(key="PERSON", image="person.svg"),
            Tag(key="ORGANIZATION", image="organization.svg"),
        ]

        return GraphData(
            date=date_to_str(self.date),
            nodes=nodes,
            edges=edges,
            clusters=clusters,
            tags=tags,
        )
