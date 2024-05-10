import networkx as nx
from community import community_louvain
from networkx import Graph

from vnnews_graph_producer.data_models.data_dicts import Cluster
from vnnews_graph_producer.data_models.entity import Entity, EntityNode
from vnnews_graph_producer.data_models.link import WeightedLink


class AnalyticsGraph:
    def __init__(self, graph_links: list[WeightedLink]):
        G = nx.Graph()
        for link in graph_links:
            G.add_edge(
                link.source,
                link.target,
                weight=link.size // 10,
            )
        self.graph: Graph = G

        eigenvector_centrality_map = self.get_eigenvector_centrality()
        cluster_map = self.get_community(eigenvector_centrality_map)

        self.clusters = list(set(e for e in cluster_map.values()))

        self.entity_nodes = [
            EntityNode(
                name=entity.name,
                type=entity.type,
                tag=entity.type.value,
                cluster=cluster_map[entity].key,
                score=eigenvector_centrality_map[entity],
            )
            for entity in self.graph.nodes
        ]

    def get_eigenvector_centrality(self) -> dict[Entity, float]:
        scores: dict[Entity, float] = nx.eigenvector_centrality(
            self.graph, max_iter=1000, weight="weight"
        )  # type: ignore

        return scores

    def get_community(
        self, score_map: dict[Entity, float], method: str = "greedy_modularity"
    ) -> dict[Entity, Cluster]:
        if method == "louvain":
            cluster_idx_map: dict[Entity, int] = community_louvain.best_partition(
                self.graph
            )

            cluster_to_largest_entity: dict[int, Entity] = {}
            for entity, score in score_map.items():
                cluster_idx = cluster_idx_map[entity]
                if cluster_idx not in cluster_to_largest_entity:
                    cluster_to_largest_entity[cluster_idx] = entity
                elif score > score_map[cluster_to_largest_entity[cluster_idx]]:
                    cluster_to_largest_entity[cluster_idx] = entity

            clusters = [
                Cluster(label=entity.name)
                for entity in cluster_to_largest_entity.values()
            ]

            entity_cluster_map: dict[Entity, Cluster] = {
                entity: clusters[cluster_idx_map[entity]] for entity in self.graph.nodes
            }

        elif method == "greedy_modularity":
            clusters_of_entities: list[set[Entity]] = (
                nx.algorithms.community.modularity_max.greedy_modularity_communities(
                    self.graph, weight="weight"
                )
            )  # type: ignore
            cluster_labels: dict[int, str] = {
                i: max(cluster, key=lambda entity: score_map[entity]).name
                for i, cluster in enumerate(clusters_of_entities)
            }

            clusters = [
                Cluster(label=cluster_labels[i])
                for i, cluster in enumerate(clusters_of_entities)
            ]

            entity_cluster_map: dict[Entity, Cluster] = {
                entity: clusters[i]
                for i, cluster in enumerate(clusters_of_entities)
                for entity in cluster
            }

        else:
            raise ValueError(f"Invalid community detection method: {method}")

        return entity_cluster_map
