# Implement Myers' generative network model inspired by refactoring.
# Source: Myers, Christopher R. "Software Systems as Complex Networks: Structure, Function, and Evolvability of
#   Software Collaboration Graphs." Physical Review. E (2007)

import random
import math
from typing import Optional

import networkx as nx

# 1) functions that are excessively long tend to be decomposed into a set of smaller functions
# 2) functions that already exist are used by others, rather than having duplicated versions of the same function
#    within the system
# 3) some functions that are deemed to support "excessive indirection" are removed, with appropriate rerouting of the
#    call graph.

TEMPERATURE = 10000

def generate_network(N0: int = 50, L0: int = 1000, p: float = 0.7, l0: int = 4, T: float = 1.0) -> nx.DiGraph:
    G = generate_initial_network(N0, L0)
    temperature = TEMPERATURE
    while temperature > 0:
        G_before = G.copy()
        rand = random.random()
        if rand < p:
            node_to_split = choose_node_for_splitting(G, l0, T)
            if node_to_split is not None:
                split_node(G, node_to_split)
        else:
            node_to_remove = choose_node_for_removal(G)
            if node_to_remove is not None:
                remove_node(G, node_to_remove)
        if G.number_of_nodes() == G_before.number_of_nodes():
            temperature -= 1
            print('.', end='', flush=True)
        else:
            temperature = TEMPERATURE
            print("\nNumber of nodes:", G.number_of_nodes(), end='', flush=True)
    print()
    return G

# split a previously chosen node
def split_node(G: nx.DiGraph, node: str) -> None:
    # short-circuit if the node is not long enough to split
    if len(node) < 2:
        return

    # select a random breakpoint
    breakpoint = random.randint(1, len(node) - 1)
    # split the node into two subnodes
    subnodes = [node[:breakpoint], node[breakpoint:]]
    for subnode in subnodes:
        if subnode not in G:
            G.add_node(subnode)
        G.add_edge(node, subnode)

def splitting_probability_distribution(length: int, l0: int, T: float) -> float:
    return 1 / (1 + math.exp(-(length - l0) / T))

def choose_node_for_splitting(G: nx.DiGraph, l0: int, T: float) -> Optional[str]:
    split_candidates = [node for node in G.nodes if G.out_degree(node) == 0]

    if len(split_candidates) == 0:
        return None

    # initial interpretation of the model:
    # select a random node
    node = random.choice(split_candidates)
    # calculate the probability of splitting the node
    probability = 1 / (1 + math.exp(-(len(node) - l0) / T))
    # decide whether to split the node
    if random.random() < probability:
        return node
    else:
        return None

    # new interpretation of the model:
    # # sample a random node from the graph according to the splitting probability distribution
    # probabilities = [splitting_probability_distribution(len(node), l0, T) for node in split_candidates]
    # node = random.choices(split_candidates, probabilities)[0]
    # return node

# 3) In detail:
# The final refactoring process (removing "excessive indirection") is carried out with probability 1-p. Specifically
# targeted are the nodes in the call graph that have only one parent (i.e., are called by only one other function) and
# only two children; I will refer to such nodes as "one-off functions". One such node from the set of eligible nodes is
# chosen at random, and is removed from the system, such that its one parent node is linked directly to its two child
# nodes.

def remove_node(G: nx.DiGraph, node: str) -> None:
    # get the parents and children of the node
    parents = list(G.predecessors(node))
    children = list(G.successors(node))
    # remove the node
    G.remove_node(node)
    # add edges from the parents to the children
    for parent in parents:
        for child in children:
            G.add_edge(parent, child)

def choose_node_for_removal(G: nx.DiGraph) -> Optional[str]:
    # choose a random node that has exactly one parent and two children
    candidate_nodes = [node for node in G.nodes if G.in_degree(node) == 1 and G.out_degree(node) == 2]
    if len(candidate_nodes) == 0:
        return None
    else:
        return random.choice(candidate_nodes)

def generate_initial_network(N0: int, L0: int) -> nx.DiGraph:
    G = nx.DiGraph()
    for _ in range(N0):
        G.add_node(generate_random_bitstring(L0))
    return G

def generate_random_bitstring(length: int) -> str:
    return ''.join(random.choice('01') for _ in range(length))
