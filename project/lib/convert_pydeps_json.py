# convert from a JSON string in pydeps format to a networkx graph

import json
import networkx as nx

def convert(pydeps: str) -> nx.DiGraph:
    data = json.loads(pydeps)
    G = nx.DiGraph()

    # remove artificial main node
    data = [node for node in data.values() if node["name"] != "__main__"]

    for node in data:
        G.add_node(node['name'])

    for node in data:
        # if the node has a key called 'imports', it has outgoing edges
        if 'imports' in node:
            for imported in node['imports']:
                # unless it's a self-import, add an edge to the graph
                if imported != node['name']:
                    G.add_edge(node['name'], imported)

    return G
