from itertools import chain

import networkx as nx
import matplotlib.pyplot as plt

import lib.myers_refactoring_model as mrm
import plot_degree_distributions as pdd
from lib.timed_execution import Timer

with Timer('Generating Myers refactoring graph'):
    network: nx.DiGraph = mrm.generate_network()

with Timer("export to graphml"):
    nx.write_graphml(network, "myers_refactoring_model.graphml")

print("Number of nodes:", network.number_of_nodes())
print("Number of edges:", network.number_of_edges())

# more metrics:
# - clustering coefficient
# - degree assortativity coefficient
# - modularity
# - number of nodes in cycles
# - average shortest path length

print("Clustering coefficient:", nx.average_clustering(network))
print("Degree assortativity coefficient:", nx.degree_assortativity_coefficient(network))
print("Modularity:", nx.algorithms.community.modularity(network, nx.algorithms.community.greedy_modularity_communities(network)))
print("Number of nodes in cycles:", len(set(chain(*nx.simple_cycles(network)))))
print("Average shortest path length:", nx.average_shortest_path_length(network))

pdd.plot_distributions(network)

plt.show()
