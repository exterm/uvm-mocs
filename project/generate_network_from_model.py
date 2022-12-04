import argparse
from itertools import chain

import networkx as nx
import numpy as np
import pandas as pd

from lib.timed_execution import Timer
import lib.myers_refactoring_model as mrm
import lib.duplicate_rewire_model as drm
import analyze_dependency_graph as adg

# the only argument is the model, which is one of 'refactoring' or 'duplicate_rewire'
parser = argparse.ArgumentParser()
parser.add_argument('model', choices=['refactoring', 'duplicate_rewire'])
args = parser.parse_args()

networks = []
NUMBER_SAMPLES = 100

# examples that we have found to roughly replicate the graphs from our data
duplicate_rewire_wagtail_latest = {'m0': 10, 'k0': 2, 'N': 849, 'beta': 0.42, 'delta': 0.68}

# actual params to use
duplicate_rewire_params = duplicate_rewire_wagtail_latest

if args.model == 'refactoring':
    with Timer('Generating Myers refactoring graph'):
        networks.append(mrm.generate_network())

    with Timer("export to graphml"):
        nx.write_graphml(networks[0], "myers_refactoring_model.graphml")
else:
    with Timer('Generating duplicate rewire graphs'):
        for i in range(NUMBER_SAMPLES):
            networks.append(drm.generate_network(**duplicate_rewire_params))

    with Timer("export to graphml"):
        nx.write_graphml(networks[0], "duplicate_rewire_model.graphml")
    print(f"Results from {NUMBER_SAMPLES} samples:")

adg.print_metrics(networks)
