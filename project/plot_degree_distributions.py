# load dependency graph from a graphml file and plot the following:
# - in-degree distribution
# - out-degree distribution
# - in-degree distribution over out-degree distribution

import argparse

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

args = argparse.ArgumentParser()
args.add_argument('input', help='input graphml file')

args = args.parse_args()

G = nx.read_graphml(args.input)

# remove outliers (nodes with very high in-or out-degree)
# this is done to make the plots more readable
G.remove_nodes_from([n for n, d in G.in_degree() if d > 50])
G.remove_nodes_from([n for n, d in G.out_degree() if d > 50])

in_degrees = [G.in_degree(n) for n in G.nodes()]
out_degrees = [G.out_degree(n) for n in G.nodes()]

# in-degree distribution as zipf-rank loglog plot
# create a dataframe with the in-degree and the rank of the in-degree
df = pd.DataFrame({'in_degree': in_degrees})
df['rank'] = df['in_degree'].rank(ascending=False)
# create a loglog plot
plt.figure()
plt.title('In-degree distribution')
plt.xlabel('In-degree')
plt.ylabel('Rank')
plt.loglog(df['in_degree'], df['rank'], 'o')
plt.draw()

# out-degree distribution as zipf-rank loglog plot
# create a dataframe with the out-degree and the rank of the out-degree
df = pd.DataFrame({'out_degree': out_degrees})
df['rank'] = df['out_degree'].rank(ascending=False)
# create a loglog plot
plt.figure()
plt.title('Out-degree distribution')
plt.xlabel('Out-degree')
plt.ylabel('Rank')
plt.loglog(df['out_degree'], df['rank'], 'o')
plt.draw()

# in-degree over out-degree.
# Multiple nodes will have the same in-degree/out-degree combination.
# emphasize the number of nodes with the same in-degree/out-degree combination
# by using a log scale for the color
plt.figure()
plt.scatter(out_degrees, in_degrees, s=2, c='k', alpha=0.3)
plt.title('in-degree distribution over out-degree distribution')
plt.xlabel('out-degree')
plt.ylabel('in-degree')
plt.xscale('log')
plt.yscale('log')
plt.draw()

plt.show()
