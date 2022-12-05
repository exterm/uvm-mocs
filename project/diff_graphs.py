# read two graphs from graphml files and render out the diff-graph into a new graphml file

import argparse

import networkx as nx
import matplotlib.pyplot as plt

import lib.graph_diff as gd

args = argparse.ArgumentParser()
args.add_argument('graph1', help='path to "before" graphml file')
args.add_argument('graph2', help='path to "after" graphml file')
args.add_argument('-o', '--output', help='path to output graphml file')
args.add_argument('-d', '--dot-layout', action='store_true', help='use dot layout')
args.add_argument('-s', '--show', action='store_true', help='show the graph')

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

if args.dot_layout or args.show:
    # render the graph and show it
    # highlight added and removed nodes and edges in green and red respectively

    # set node colors
    node_colors = []
    for node in annotated_graph.nodes:
        if annotated_graph.nodes[node]['diff-status'] == 'added':
            node_colors.append('green')
        elif annotated_graph.nodes[node]['diff-status'] == 'removed':
            node_colors.append('red')
        else:
            node_colors.append('gray')

    # set edge colors
    edge_colors = []
    for edge in annotated_graph.edges:
        if annotated_graph.edges[edge]['diff-status'] == 'added':
            edge_colors.append('green')
        elif annotated_graph.edges[edge]['diff-status'] == 'removed':
            edge_colors.append('red')
        else:
            edge_colors.append('gray')

    # draw the graph
    if args.dot_layout:
        pos = nx.nx_agraph.graphviz_layout(annotated_graph, prog='dot', args='-GTBbalance=min -Grankdir=BT')
    else:
        pos = nx.random_layout(annotated_graph)
    nx.draw(
        annotated_graph,
        pos,
        with_labels=False,
        node_color=node_colors,
        edge_color=edge_colors,
        node_size=50,
        width=0.3,
        alpha=0.7,
    )
    plt.show()
