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
parser.add_argument('--dump-graphs', action='store_true', help='Dump the graphs to graphml files. Skips metrics calculation.')
args = parser.parse_args()

networks = []
NUMBER_SAMPLES = 100

# examples that we have found to roughly replicate the graphs from our data
duplicate_rewire_wagtail_latest = {'m0': 10, 'k0': 2, 'N': 849, 'beta': 0.42, 'delta': 0.68}

# actual params to use
duplicate_rewire_params = duplicate_rewire_wagtail_latest

if args.dump_graphs:
    NUMBER_SAMPLES = 1
if args.model == 'refactoring':
    with Timer('Generating Myers refactoring graph'):
        networks.append(mrm.generate_network())

    if args.dump_graphs:
        with Timer("export to graphml"):
            nx.write_graphml(networks[0], "myers_refactoring_model.graphml")
else:
    with Timer(f'Generating {NUMBER_SAMPLES} duplicate rewire graphs'):
        for i in range(NUMBER_SAMPLES):
            networks.append(drm.generate_network(**duplicate_rewire_params, dump_graphs=args.dump_graphs))

if not args.dump_graphs:
    adg.print_metrics(networks)

    adg.print_regression_results(networks)
