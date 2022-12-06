# load dependency graph from a graphml file and plot the following:
# - in-degree distribution
# - out-degree distribution
# - in-degree distribution over out-degree distribution

from typing import List, Tuple
import pdb

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import lib.regression as reg

def get_zipf_distributions(g: nx.DiGraph) -> Tuple[pd.DataFrame, pd.DataFrame]:
    in_degrees: List[int] = [g.in_degree(n) for n in g.nodes()] # type: ignore
    out_degrees: List[int] = [g.out_degree(n) for n in g.nodes()] # type: ignore

    # in-degree distribution as zipf-rank loglog plot
    # create a dataframe with the in-degree and the rank of the in-degree
    in_df = pd.DataFrame({'in_degree': in_degrees})
    in_df['rank'] = in_df['in_degree'].rank(ascending=False)

    # out-degree distribution as zipf-rank loglog plot
    # create a dataframe with the out-degree and the rank of the out-degree
    out_df = pd.DataFrame({'out_degree': out_degrees})
    out_df['rank'] = out_df['out_degree'].rank(ascending=False)

    return in_df, out_df

def print_regression_results(gs: List[nx.DiGraph]):
    # compute slopes for each graph, then compute the mean and standard deviation
    in_slopes = []
    in_qualities = []
    out_slopes = []
    out_qualities = []
    for g in gs:
        in_df, out_df = get_zipf_distributions(g)
        # filter nodes with zero in-degree or out-degree
        in_df = in_df[in_df['in_degree'] > 0]
        out_df = out_df[out_df['out_degree'] > 0]
        in_regression_result = reg.compute_linear_regression(in_df['rank'], in_df['in_degree']) # type: ignore
        in_slopes.append(in_regression_result.slope) # type: ignore
        in_qualities.append(in_regression_result.rvalue**2) # type: ignore
        out_regression_result = reg.compute_linear_regression(out_df['rank'], out_df['out_degree']) # type: ignore
        out_slopes.append(out_regression_result.slope) # type: ignore
        out_qualities.append(out_regression_result.rvalue**2) # type: ignore
    print()
    print(f"mean in-degree zipf slope: {np.mean(in_slopes):.6f} +/- {np.std(in_slopes):.6f}")
    print(f"CCDF equivalent slope: {1/np.mean(in_slopes)-1:.6f}")
    print(f"mean in-degree quality of fit(r^2): {np.mean(in_qualities):.6f} +/- {np.std(in_qualities):.6f}")
    print(f"mean out-degree zipf slope: {np.mean(out_slopes):.6f} +/- {np.std(out_slopes):.6f}")
    print(f"CCDF equivalent slope: {1/np.mean(out_slopes)-1:.6f}")
    print(f"mean out-degree quality of fit(r^2): {np.mean(out_qualities):.6f} +/- {np.std(out_qualities):.6f}")

def plot_distributions(g: nx.DiGraph, dump: bool = False):
    # remove outliers (nodes with very high in-or out-degree)
    # this is done to make the plots more readable
    # g.remove_nodes_from([n for n, d in g.in_degree() if d > 50])
    # g.remove_nodes_from([n for n, d in g.out_degree() if d > 50])

    in_df, out_df = get_zipf_distributions(g)

    plt.figure()
    plt.title('In-degree distribution')
    plt.ylabel('In-degree')
    plt.xlabel('Rank')
    plt.loglog(in_df['rank'], in_df['in_degree'], 'o')
    if dump:
        plt.savefig('in_degree_distribution.pdf')
    plt.draw()

    plt.figure()
    plt.title('Out-degree distribution (semilog)')
    plt.ylabel('Out-degree')
    plt.xlabel('Rank')
    # only rank is logarithmic
    plt.semilogx(out_df['rank'], out_df['out_degree'], 'o')
    if dump:
        plt.savefig('out_degree_distribution-semilog.pdf')
    plt.draw()

    plt.figure()
    plt.title('Out-degree distribution (loglog)')
    plt.ylabel('Out-degree')
    plt.xlabel('Rank')
    plt.loglog(out_df['rank'], out_df['out_degree'], 'o')
    if dump:
        plt.savefig('out_degree_distribution-loglog.pdf')
    plt.draw()

    # in-degree over out-degree.
    # Multiple nodes will have the same in-degree/out-degree combination.
    # emphasize the number of nodes with the same in-degree/out-degree combination
    # by using a log scale for the color
    plt.figure()
    plt.scatter(out_df['out_degree'], in_df['in_degree'], s=5, c='k', alpha=0.1)
    plt.title('in-degree distribution over out-degree distribution')
    plt.xlabel('out-degree')
    plt.ylabel('in-degree')
    if dump:
        plt.savefig('in_degree_over_out_degree_distribution.pdf')
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

    giant_components = [max(nx.weakly_connected_components(g), key=len) for g in gs]
    giant_component_sizes = [len(giant_component) for giant_component in giant_components]
    print("Giant component size:", np.mean(giant_component_sizes), "+/-", np.std(giant_component_sizes))

    average_shortest_paths =\
        [nx.average_shortest_path_length(g.subgraph(gwcc)) for g, gwcc in zip(gs, giant_components)]
    print("Average shortest path length:", np.mean(average_shortest_paths), "+/-", np.std(average_shortest_paths))

    # cycle_node_counts = [len(list(nx.simple_cycles(g))) for g in gs]
    # print("Number of cycles:", np.mean(cycle_node_counts), "+/-", np.std(cycle_node_counts))

if __name__ == '__main__':
    import argparse

    args = argparse.ArgumentParser()
    args.add_argument('input', help='input graphml file')
    args.add_argument('--no-show', action='store_true', help='do not show the plots')
    args.add_argument('-w', '--write-plots', action='store_true', help='write the plots to files')

    args = args.parse_args()

    G: nx.DiGraph = nx.read_graphml(args.input)

    print_metrics([G])

    print_regression_results([G])

    if args.write_plots or not args.no_show:
        plot_distributions(G, dump=args.write_plots)
        if not args.no_show:
            plt.show()
