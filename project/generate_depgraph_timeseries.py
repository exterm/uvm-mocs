# Generate timeseries for various interesting metrics of the dependency graph
#
# Takes a list of filenames as input, and, for now, displays plots.
# Assumes the files are in graphml format, with the filename satisfying the following format:
# <date>_<sha>.networkx.graphml (for example, 2016-12-31_abcdef123456.networkx.graphml)

import sys
from itertools import chain

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.ticker as mpt

# Read in the graphml files and remember the month and year
graphs = []
for filepath in sys.argv[1:]:
    # extract filename from path
    filename = filepath.split('/')[-1]
    year, month, _ = filename.split('-')
    year_month = year + '-' + month
    graphs.append((nx.read_graphml(filepath), year_month))

# metrics:
# - number of nodes
# - number of edges
# - number of strongly connected components
# - number of weakly connected components
# - average in-degree
# - average out-degree
# - clustering coefficient
# - degree assortativity coefficient
# - modularity
# - number of nodes in cycles

def draw_metric(graphs: list[nx.DiGraph], metric, title: str):
    print("Calculating", title, end='')
    values = []
    months = []
    for graph, month in graphs:
        print('.', end='', flush=True)
        try:
            values.append(metric(graph))
        except (ZeroDivisionError):
            values.append(0)
            print(sys.exc_info()[0].__name__, 'for metric', title, 'in month', month) # type: ignore
        except KeyboardInterrupt:
            print("Interrupted in month", month)
            raise KeyboardInterrupt
        months.append(month)
    print()

    print("Drawing", title)
    plt.figure(constrained_layout=True)
    plt.title(title)
    plt.xlabel('Month')
    plt.ylabel(title)
    plt.plot(months, values)
    if min(values) > 0:
        plt.gca().set_ylim(bottom=0)
    if max(values) < 0:
        plt.gca().set_ylim(top=0)
    # rotate x labels
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
    # sample x labels so they don't overlap
    plt.gca().xaxis.set_major_locator(mpt.MaxNLocator(20))
    filename = title.replace(' ', '_').replace('/', '_').lower()
    plt.savefig(filename + '.pdf', bbox_inches='tight')
    plt.draw()

giant_components = []
for graph, month in graphs:
    giant_components.append(max(nx.weakly_connected_components(graph), key=len))
just_graphs = [g for g, _ in graphs]

draw_metric(graphs, lambda g: g.number_of_nodes(), 'Number of nodes')
draw_metric(graphs, lambda g: g.number_of_edges(), 'Number of edges')
draw_metric(graphs, lambda g: g.number_of_edges() / g.number_of_nodes(), 'Edges/nodes ratio')
draw_metric(graphs, lambda g: sum(nx.betweenness_centrality(g).values()) / g.number_of_nodes(), 'Average betweenness centrality')

draw_metric(graphs, lambda g: nx.number_strongly_connected_components(g), 'Number of strongly connected components')
draw_metric(graphs, lambda g: nx.number_weakly_connected_components(g), 'Number of weakly connected components')
draw_metric(graphs, lambda g: sum([t[1] for t in g.in_degree()]) / g.number_of_nodes(), 'Average in-degree')
draw_metric(graphs, lambda g: sum([t[1] for t in g.out_degree()]) / g.number_of_nodes(), 'Average out-degree')
draw_metric(graphs, lambda g: nx.average_clustering(g), 'Average clustering coefficient')
draw_metric(graphs, lambda g: nx.degree_assortativity_coefficient(g), 'Degree assortativity coefficient')
draw_metric(graphs, lambda g: nx.algorithms.community.modularity(g, nx.algorithms.community.greedy_modularity_communities(g)), 'Modularity')

# based on giant components
draw_metric(graphs, lambda g: len(giant_components[just_graphs.index(g)]), 'Giant component size by number of nodes')
draw_metric(graphs, lambda g: nx.average_shortest_path_length(g.subgraph(giant_components[just_graphs.index(g)])), 'Average shortest path length in giant component')

# seemingly goes into infinite loop on some graphs...
draw_metric(graphs, lambda g: len(set(chain(*nx.simple_cycles(g)))), 'Number of nodes in cycles')

# finally, show all plots
plt.show()
