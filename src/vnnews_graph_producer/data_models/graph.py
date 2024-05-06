from typing import Optional
from .entity import Entity


class Graph:
    def __init__(
        self, nodes: list[Entity], graph: Optional[dict[Entity, list[Entity]]] = None
    ):
        self.nodes = nodes
        self.graph = graph or {node: [] for node in nodes}

    @staticmethod
    def full_graph(nodes: list[Entity]) -> "Graph":
        graph = {node: nodes.copy() for node in nodes}
        return Graph(nodes=nodes, graph=graph)

    def __add__(self, other: "Graph") -> "Graph":
        new_nodes = list(set(self.nodes + other.nodes))
        new_graph = self.graph.copy()

        for node, neighbors in other.graph.items():
            if node in new_graph:
                new_graph[node].extend(neighbors)
            else:
                new_graph[node] = neighbors

        return Graph(nodes=new_nodes, graph=new_graph)
