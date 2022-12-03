import networkx as nx

import lib.myers_refactoring_model as mrm

def test_generate_random_bitstring():
    assert len(mrm.generate_random_bitstring(10)) == 10

def test_split_node_simple():
    G = nx.DiGraph()
    G.add_node('101')
    previous_node_count = G.number_of_nodes()
    mrm.split_node(G, '101')
    assert G.number_of_nodes() == previous_node_count + 2
    assert G.number_of_edges() == 2

def test_split_node_existing_child():
    G = nx.DiGraph()
    G.add_node('101')
    G.add_node('1')
    previous_node_count = G.number_of_nodes()
    mrm.split_node(G, '101')
    assert G.number_of_nodes() == previous_node_count + 1
    assert G.number_of_edges() == 2

def test_split_node_existing_children():
    # all possible child nodes exist already
    G = nx.DiGraph()
    G.add_node('101')
    G.add_node('1')
    G.add_node('10')
    G.add_node('01')
    previous_node_count = G.number_of_nodes()
    mrm.split_node(G, '101')
    assert G.number_of_nodes() == previous_node_count
    assert G.number_of_edges() == 2

def test_remove_node():
    G = nx.DiGraph()
    G.add_node('101')
    G.add_node('1')
    G.add_node('10')
    G.add_edge('101', '1')
    G.add_edge('101', '10')
    G.add_node('11')
    G.add_node('00')
    G.add_edge('10', '11')
    G.add_edge('10', '00')
    previous_node_count = G.number_of_nodes()
    previous_edge_count = G.number_of_edges()
    mrm.remove_node(G, '10')
    assert G.number_of_nodes() == previous_node_count - 1
    assert G.number_of_edges() == previous_edge_count - 1

def test_choose_node_for_removal():
    G = nx.DiGraph()
    assert mrm.choose_node_for_removal(G) == None

    G.add_node('101')
    G.add_node('1')
    G.add_node('10')
    G.add_edge('101', '1')
    G.add_edge('101', '10')
    G.add_node('11')
    G.add_node('00')
    G.add_edge('10', '11')
    G.add_edge('10', '00')
    assert mrm.choose_node_for_removal(G) in ['10']

def test_choose_node_for_splitting():
    # don't split nodes with children
    G = nx.DiGraph()
    G.add_node('10')
    G.add_node('1')
    G.add_node('0')

    G.add_edge('10', '1')
    G.add_edge('10', '0')

    assert mrm.choose_node_for_splitting(G, 1, 1) == None
