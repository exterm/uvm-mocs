import networkx as nx

# remove nodes representing inner classes
# load network from GraphML file, remove nodes, save as GraphML file

# Read in the graph
G = nx.read_graphml('data/guava.annotated.graphml')

# Remove the nodes
G.remove_nodes_from([n for n in G.nodes() if n.find('$') > -1])

# Save the graph as GraphML
nx.write_graphml(G, 'data/guava.annotated.filtered.graphml')
