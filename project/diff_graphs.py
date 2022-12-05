# read two graphs from graphml files and render out the diff-graph into a new graphml file

import argparse

import networkx as nx

import lib.graph_diff as gd

args = argparse.ArgumentParser()
args.add_argument('graph1', help='path to "before" graphml file')
args.add_argument('graph2', help='path to "after" graphml file')
args.add_argument('-o', '--output', help='path to output graphml file')

args = args.parse_args()

graph1 = nx.read_graphml(args.graph1)
graph2 = nx.read_graphml(args.graph2)

annotated_graph = gd.get_annotated_graph(graph1, graph2)

# print number of added and removed nodes and edges
print('Added nodes: {}'.format(len([n for n in annotated_graph.nodes if annotated_graph.nodes[n]['diff-status'] == 'added'])))
print('Removed nodes: {}'.format(len([n for n in annotated_graph.nodes if annotated_graph.nodes[n]['diff-status'] == 'removed'])))
print('Added edges: {}'.format(len([e for e in annotated_graph.edges if annotated_graph.edges[e]['diff-status'] == 'added'])))
print('Removed edges: {}'.format(len([e for e in annotated_graph.edges if annotated_graph.edges[e]['diff-status'] == 'removed'])))

if args.output:
    nx.write_graphml(annotated_graph, args.output)
else:
    print('No output file specified')
