import networkx as nx
from community import community_louvain
from fa2_modified import ForceAtlas2

from vnnews_graph_producer.data_models.graph import NewsGraph


def create_networkx_graph(graph: NewsGraph) -> nx.Graph:
    G = nx.Graph()

    for link in graph.links:
        G.add_edge(
            link["source"],
            link["target"],
            weight=link["size"] / 10,
        )

    return G


def create_positions(G: nx.Graph) -> dict[str, tuple[float, float]]:
    forceatlas2 = ForceAtlas2(
        # Behavior alternatives
        outboundAttractionDistribution=True,  # Dissuade hubs
        linLogMode=False,  # NOT IMPLEMENTED
        adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
        edgeWeightInfluence=1.0,
        # Performance
        jitterTolerance=1.0,  # Tolerance
        barnesHutOptimize=True,
        barnesHutTheta=1,
        multiThreaded=False,  # NOT IMPLEMENTED
        # Tuning
        scalingRatio=10.0,
        strongGravityMode=False,
        gravity=1.0,
        # Log
        verbose=True,
    )

    positions: dict[str, tuple[float, float]] = forceatlas2.forceatlas2_networkx_layout(
        G, pos=None, iterations=800, weight_attr="weight"
    )

    return positions


def get_positions(G: nx.Graph) -> dict[str, tuple[float, float]]:
    positions = create_positions(G)

    return positions


def get_eigenvector_centrality(G: nx.Graph) -> dict[str, float]:
    scores: dict[str, float] = nx.eigenvector_centrality(
        G, max_iter=1000, weight="weight"
    )  # type: ignore

    return scores


def get_community(G: nx.Graph) -> dict[str, int]:
    partition = community_louvain.best_partition(G)
    return partition
