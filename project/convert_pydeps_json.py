# import pydeps' json format into networkx
#
# The data can be generated with `pydeps --no-output --show-deps --nodot wagtail > dependencies.json`

# Run this script on a collection of pydeps json files with
#  find data/wagtail/dependencies/ -name "*.json" -exec poetry run python convert_pydeps_json.py '{}' \;

import sys
import argparse

import json
import networkx as nx
import matplotlib.pyplot as plt

from lib import convert_pydeps_json

args = argparse.ArgumentParser()
args.add_argument("input_file", help="input file")

args = args.parse_args()

with open(args.input_file) as f:
    g = convert_pydeps_json.convert(f.read())

# remove file extension from input file name
output_prefix = args.input_file.rsplit('.', 1)[0]

# export to graphml for use in Gephi
nx.write_graphml(g, f"{output_prefix}.networkx.graphml")

# for d3.js, export to json
json_data = json.dumps(nx.node_link_data(g))
with open(f"{output_prefix}.networkx.json", "w") as f:
    f.write(json_data)
