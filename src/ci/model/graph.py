#!/usr/bin/env python3

import networkx as nx
import logging
from multiprocessing import Pool
from typing import List, Callable, Any

from ci.model.stage import Stage

StageVisitor = Callable[[str, Any], None]


class StageGraph:
    graph: nx.DiGraph
    stages: List[Stage]

    def __init__(self, graph: nx.DiGraph) -> None:
        self.graph = graph

    def graph(self) -> nx.DiGraph:
        return self.graph

    def walk_groups(self, visitor: StageVisitor, **kwargs) -> None:
        """Calls the visitor for every node that has 0 outgoing edges.
        Afterwards the edges are removed and the visitor is called for the next group."""
        pool = Pool()  # ThreadPool()
        graph_copy = nx.DiGraph.copy(self.graph)

        logging.debug("Nodes in graph: %d", len(graph_copy))
        while len(graph_copy):
            nodes = [n for n in graph_copy if graph_copy.out_degree(n) == 0]

            logging.debug("Queueing %s", nodes)

            args = [(graph_copy.nodes[node]["stage"], kwargs) for node in nodes]
            pool.starmap(visitor, args)

            for node in nodes:
                logging.debug("Removing node %s", node)
                graph_copy.remove_node(node)

        pool.close()
        pool.join()
