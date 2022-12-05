import networkx as nx
from numpy.random import choice
import random
import numpy as np

def initialize_network() -> nx.DiGraph: # initializes a directed network with two nodes
    G = nx.DiGraph()
    G.add_node(0)
    G.add_node(1)
    G.add_edge(0,1)
    return G

def generate_network(N: int, C: int, v: float, m: int, alpha: float) -> nx.DiGraph:
    G = initialize_network()
    for step in range(len(G.nodes()), N): ## one step for each node to add, we already have 2 nodes (id 0 and 1)
        for _ in range(m): ## one step for each edge to add
            rand = random.random()
            if rand < alpha: ## do we add an edge from new to old?
                eligible_nodes = [node for node in G.nodes if G.has_edge(step, node) == False and step != node] ## only choose from nodes that aren't already connected in this direction
                in_degrees = [(G.in_degree(node) + C)*(step - node)**(-v) for node in eligible_nodes]
                if len(eligible_nodes) > 0:
                    node_choose = choice(eligible_nodes, 1, p=np.array(in_degrees)/sum(in_degrees))[0]
                    G.add_edge(step, node_choose)
            else:
                eligible_nodes = [node for node in G.nodes if G.has_edge(node, step) == False and step != node] ## only choose from nodes that aren't already connected in this direction
                out_degrees = [(G.out_degree(node) + C)*(step - node)**(-v) for node in eligible_nodes]
                if len(eligible_nodes) > 0:
                    node_choose = choice(eligible_nodes, 1, p=np.array(out_degrees)/sum(out_degrees))[0]
                    G.add_edge(node_choose, step)
    return G
