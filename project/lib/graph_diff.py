# Investigate the differences between two graphs

from typing import Tuple

import networkx as nx

# take two graphs and compute the added and removed nodes and edges.
def get_graph_diffs(graph1: nx.DiGraph, graph2: nx.DiGraph):
    added_nodes = graph2.nodes() - graph1.nodes()
    removed_nodes = graph1.nodes() - graph2.nodes()
    added_edges = set(graph2.edges()) - set(graph1.edges())
    removed_edges = set(graph1.edges()) - set(graph2.edges())
    return added_nodes, added_edges, removed_nodes, removed_edges

# take two graphs and generate a new one in which differences are annotated
# include the superset of all edges and nodes
def get_annotated_graph(graph1: nx.DiGraph, graph2: nx.DiGraph) -> nx.DiGraph:
    added_nodes, added_edges, removed_nodes, removed_edges = get_graph_diffs(graph1, graph2)
    annotated_graph = nx.DiGraph()
    annotated_graph.add_nodes_from(graph1)
    annotated_graph.add_nodes_from(graph2)
    annotated_graph.add_edges_from(graph1.edges())
    annotated_graph.add_edges_from(graph2.edges())
    for node in annotated_graph.nodes():
        if node in added_nodes:
            annotated_graph.nodes[node]['diff-status'] = 'added'
        elif node in removed_nodes:
            annotated_graph.nodes[node]['diff-status'] = 'removed'
        else:
            annotated_graph.nodes[node]['diff-status'] = 'unchanged'
    for edge in annotated_graph.edges():
        if edge in added_edges:
            annotated_graph.edges[edge]['diff-status'] = 'added'
        elif edge in removed_edges:
            annotated_graph.edges[edge]['diff-status'] = 'removed'
        else:
            annotated_graph.edges[edge]['diff-status'] = 'unchanged'
    return annotated_graph
