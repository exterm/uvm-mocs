# import pydeps' json format into networkx
#
# The data can be generated with `pydeps --no-output --show-deps --nodot wagtail > dependencies.json`

import sys

import json
import networkx as nx
import matplotlib.pyplot as plt

from lib import convert_pydeps_json

def main():
    if len(sys.argv) != 2:
        print("Usage: python convert_pydeps_json.py pydeps.json")
        sys.exit(1)

    input_file = sys.argv[1]
    with open(input_file) as f:
        g = convert_pydeps_json.convert(f.read())

    # remove file extension from input file name
    output_prefix = input_file.rsplit('.', 1)[0]

    # export to graphml for use in Gephi
    nx.write_graphml(g, f"{output_prefix}.networkx.graphml")

    # for d3.js, export to json
    json_data = json.dumps(nx.node_link_data(g))
    with open(f"{output_prefix}.networkx.json", "w") as f:
        f.write(json_data)

if __name__ == "__main__":
    main()



