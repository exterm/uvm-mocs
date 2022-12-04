import argparse
from itertools import chain

import networkx as nx
import numpy as np
import pandas as pd

from lib.timed_execution import Timer
import lib.myers_refactoring_model as mrm
import lib.duplicate_rewire_model as drm

# the only argument is the model, which is one of 'refactoring' or 'duplicate_rewire'
parser = argparse.ArgumentParser()
parser.add_argument('model', choices=['refactoring', 'duplicate_rewire'])
args = parser.parse_args()

networks = []
NUMBER_SAMPLES = 100

# examples that we have found to roughly replicate the graphs from our data
duplicate_rewire_wagtail_latest = {'m0': 10, 'k0': 2, 'N': 849, 'beta': 0.5, 'delta': 0.7}

# actual params to use
duplicate_rewire_params = duplicate_rewire_wagtail_latest

if args.model == 'refactoring':
    with Timer('Generating Myers refactoring graph'):
        network: nx.DiGraph = mrm.generate_network()

    with Timer("export to graphml"):
        nx.write_graphml(network, "myers_refactoring_model.graphml")
else:
    with Timer('Generating duplicate rewire graphs'):
        for i in range(NUMBER_SAMPLES):
            networks.append(drm.generate_network(**duplicate_rewire_params))

    with Timer("export to graphml"):
        nx.write_graphml(networks[0], "duplicate_rewire_model.graphml")
    print(f"Results from {NUMBER_SAMPLES} samples:")

# for every metric, report the average and standard deviation
node_numbers = [len(network.nodes) for network in networks]
print("Number of nodes:", np.mean(node_numbers), "+/-", np.std(node_numbers))

edge_numbers = [len(network.edges) for network in networks]
print("Number of edges:", np.mean(edge_numbers), "+/-", np.std(edge_numbers))

clustering_coefficients = [nx.average_clustering(network) for network in networks]
print("Clustering coefficient:", np.mean(clustering_coefficients), "+/-", np.std(clustering_coefficients))

assortativity_coefficients = [nx.degree_assortativity_coefficient(network) for network in networks]
print("Degree Assortativity coefficient:", np.mean(assortativity_coefficients), "+/-", np.std(assortativity_coefficients))

modularities = [nx.algorithms.community.modularity(network, nx.algorithms.community.greedy_modularity_communities(network)) for network in networks]
print("Modularity:", np.mean(modularities), "+/-", np.std(modularities))

giant_components = [max(nx.weakly_connected_components(network), key=len) for network in networks]
average_shortest_path_lengths = [nx.average_shortest_path_length(network.subgraph(giant_component)) for network, giant_component in zip(networks, giant_components)]
print("Average shortest path length:", np.mean(average_shortest_path_lengths), "+/-", np.std(average_shortest_path_lengths))

cycle_node_counts = [len(set(chain(*nx.simple_cycles(network)))) for network in networks]
print("Number of nodes in cycles:", np.mean(cycle_node_counts), "+/-", np.std(cycle_node_counts))
