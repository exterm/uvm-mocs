import networkx as nx

import lib.graph_diff as gd

def test_get_graph_diffs_simple():
    graph1 = nx.DiGraph()
    graph1.add_edges_from([(1, 2), (1, 3)])

    graph2 = nx.DiGraph()
    graph2.add_edges_from([(1, 2), (1, 4)])

    added_nodes, added_edges, removed_nodes, removed_edges = gd.get_graph_diffs(graph1, graph2)

    assert added_nodes == {4}
    assert added_edges == {(1, 4)}

    assert removed_nodes == {3}
    assert removed_edges == {(1, 3)}

def test_get_graph_diffs_changed_direction():
    graph1 = nx.DiGraph()
    graph1.add_edges_from([(1, 2)])

    graph2 = nx.DiGraph()
    graph2.add_edges_from([(2, 1)])

    added_nodes, added_edges, removed_nodes, removed_edges = gd.get_graph_diffs(graph1, graph2)

    assert added_nodes == set()
    assert added_edges == {(2, 1)}

    assert removed_nodes == set()
    assert removed_edges == {(1, 2)}

def test_get_annotated_graph():
    graph1 = nx.DiGraph()
    graph1.add_edges_from([(1, 2), (1, 3)])

    graph2 = nx.DiGraph()
    graph2.add_edges_from([(1, 2), (1, 4)])

    annotated_graph = gd.get_annotated_graph(graph1, graph2)

    assert annotated_graph.nodes[1]['diff-status'] == 'unchanged'
    assert annotated_graph.nodes[2]['diff-status'] == 'unchanged'
    assert annotated_graph.nodes[3]['diff-status'] == 'removed'
    assert annotated_graph.nodes[4]['diff-status'] == 'added'

    assert annotated_graph.edges[(1, 2)]['diff-status'] == 'unchanged'
    assert annotated_graph.edges[(1, 3)]['diff-status'] == 'removed'
    assert annotated_graph.edges[(1, 4)]['diff-status'] == 'added'
