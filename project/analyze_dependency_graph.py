# load dependency graph from a graphml file and plot the following:
# - in-degree distribution
# - out-degree distribution
# - in-degree distribution over out-degree distribution

from itertools import chain

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

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

if __name__ == '__main__':
    import argparse

    args = argparse.ArgumentParser()
    args.add_argument('input', help='input graphml file')
    args.add_argument('--no-show', action='store_true', help='do not show the plots')

    args = args.parse_args()

    G: nx.DiGraph = nx.read_graphml(args.input)

    print("Number of nodes:", G.number_of_nodes())
    print("Number of edges:", G.number_of_edges())

    print("Clustering coefficient:", nx.average_clustering(G))
    print("Degree assortativity coefficient:", nx.degree_assortativity_coefficient(G))
    print("Modularity:", nx.algorithms.community.modularity(G, nx.algorithms.community.greedy_modularity_communities(G)))

    giant_component = max(nx.weakly_connected_components(G), key=len)
    print("Average shortest path length:", nx.average_shortest_path_length(G.subgraph(giant_component)))
    print("Number of nodes in cycles:", len(set(chain(*nx.simple_cycles(G)))))

    if not args.no_show:
        plot_distributions(G)
        plt.show()
