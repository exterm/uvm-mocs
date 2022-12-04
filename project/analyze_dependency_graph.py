# load dependency graph from a graphml file and plot the following:
# - in-degree distribution
# - out-degree distribution
# - in-degree distribution over out-degree distribution

from itertools import chain
from typing import List

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_distributions(g: nx.DiGraph):
    # remove outliers (nodes with very high in-or out-degree)
    # this is done to make the plots more readable
    # g.remove_nodes_from([n for n, d in g.in_degree() if d > 50])
    # g.remove_nodes_from([n for n, d in g.out_degree() if d > 50])

    in_degrees = [g.in_degree(n) for n in g.nodes()]
    out_degrees = [g.out_degree(n) for n in g.nodes()]

    # in-degree distribution as zipf-rank loglog plot
    # create a dataframe with the in-degree and the rank of the in-degree
    df = pd.DataFrame({'in_degree': in_degrees})
    df['rank'] = df['in_degree'].rank(ascending=False)
    # create a loglog plot
    plt.figure()
    plt.title('In-degree distribution')
    plt.xlabel('In-degree')
    plt.ylabel('Rank')
    plt.loglog(df['in_degree'], df['rank'], 'o')
    plt.draw()

    # out-degree distribution as zipf-rank loglog plot
    # create a dataframe with the out-degree and the rank of the out-degree
    df = pd.DataFrame({'out_degree': out_degrees})
    df['rank'] = df['out_degree'].rank(ascending=False)
    # create a loglog plot
    plt.figure()
    plt.title('Out-degree distribution')
    plt.xlabel('Out-degree')
    plt.ylabel('Rank')
    plt.loglog(df['out_degree'], df['rank'], 'o')
    plt.draw()

    # in-degree over out-degree.
    # Multiple nodes will have the same in-degree/out-degree combination.
    # emphasize the number of nodes with the same in-degree/out-degree combination
    # by using a log scale for the color
    plt.figure()
    plt.scatter(out_degrees, in_degrees, s=5, c='k', alpha=0.1)
    plt.title('in-degree distribution over out-degree distribution')
    plt.xlabel('out-degree')
    plt.ylabel('in-degree')
    # plt.xscale('log')
    # plt.yscale('log')
    plt.draw()

def print_metrics(gs: List[nx.DiGraph]):
    node_numbers = [g.number_of_nodes() for g in gs]
    print("Number of nodes:", np.mean(node_numbers), "+/-", np.std(node_numbers))

    edge_numbers = [g.number_of_edges() for g in gs]
    print("Number of edges:", np.mean(edge_numbers), "+/-", np.std(edge_numbers))

    edges_per_node = [g.number_of_edges() / g.number_of_nodes() for g in gs]
    print("Edges per node:", np.mean(edges_per_node), "+/-", np.std(edges_per_node))

    clustering_coefficients = [nx.average_clustering(g) for g in gs]
    print("Clustering coefficient:", np.mean(clustering_coefficients), "+/-", np.std(clustering_coefficients))

    assortativity_coefficients = [nx.degree_assortativity_coefficient(g) for g in gs]
    print("Degree assortativity coefficient:", np.mean(assortativity_coefficients), "+/-", np.std(assortativity_coefficients))

    modularities = [nx.algorithms.community.modularity(g, nx.algorithms.community.greedy_modularity_communities(g)) for g in gs]
    print("Modularity:", np.mean(modularities), "+/-", np.std(modularities))

    giant_components = [max(nx.connected_components(g), key=len) for g in gs]
    giant_component_sizes = [len(giant_component) for giant_component in giant_components]
    print("Giant component size:", np.mean(giant_component_sizes), "+/-", np.std(giant_component_sizes))

    average_shortest_paths = [nx.average_shortest_path_length(g) for g in gs]
    print("Average shortest path length:", np.mean(average_shortest_paths), "+/-", np.std(average_shortest_paths))

    cycle_node_counts = [len(list(nx.simple_cycles(g))) for g in gs]
    print("Number of cycles:", np.mean(cycle_node_counts), "+/-", np.std(cycle_node_counts))

if __name__ == '__main__':
    import argparse

    args = argparse.ArgumentParser()
    args.add_argument('input', help='input graphml file')
    args.add_argument('--no-show', action='store_true', help='do not show the plots')

    args = args.parse_args()

    G: nx.DiGraph = nx.read_graphml(args.input)

    print_metrics([G])

    if not args.no_show:
        plot_distributions(G)
        plt.show()
