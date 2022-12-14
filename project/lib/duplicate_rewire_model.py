import random

import networkx as nx

# First, an initial random network of m0 < N nodes is created. This random graph is generated by the addition of nodes
# with degree k0 = 2, every link pointing to a random target node.

def generate_initial_network(m0: int, k0: int) -> nx.DiGraph:
    G = nx.DiGraph()
    for i in range(m0):
        G.add_node(i)
        children = random.sample(range(i), min(k0, i))
        for child in children:
            G.add_edge(i, child)
    return G

# Starting from this backbone, we apply the following rules at each iteration of the model.
# i) Duplication. A randomly chosen target node v is cloned, and the new node w attaches to all the neighbors of
#    the target node.
# ii) Divergence. For each pair of original and redundant links remove one of them with probability \delta.
# iii) Cross linking. In addition, the target and new node are linked (w -> v) with probability \beta. This rule is
# important in order to generate triads or 3-subgraphs.

def generate_network(m0: int, k0: int, N: int, beta: float, delta: float, dump_graphs: bool = False) -> nx.DiGraph:
    G = generate_initial_network(m0, k0)
    steps = 0
    while len(G.nodes) < N:
        i = len(G.nodes)
        G.add_node(i)
        v = random.choice(list(G.nodes))
        for parent in G.predecessors(v):
            if random.random() > delta:
                G.add_edge(parent, i)
        for child in list(G.successors(v)):
            if random.random() > delta:
                G.add_edge(i, child)
        if G.out_degree(i) == 0 or G.in_degree(i) == 0:
            G.remove_node(i)
        else:
            if random.random() < beta:
                G.add_edge(i, v)
        if dump_graphs and steps % 20 == 0:
            nx.write_graphml(G, f"step{steps:04d}-node{i:04d}-duplicate_rewire.graphml")
        steps += 1
    return G
