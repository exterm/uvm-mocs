import networkx as nx

# Annotate nodes with their top-level package name.
# - Read graph from GraphML file
# - Loop over nodes to generate map of node name to package name
# - Use map to set node attributes
# - Save annotated graph as GraphML file

# Read in the graph
G = nx.read_graphml('data/guava.graphml')

# Loop over nodes to generate map of node name to package name
node_map = {}
for node in G.nodes():
    # We define top level package as the first four parts of the name
    # e.g. com.google.common.collect.Synchronized$SynchronizedRandomAccessList
    #      ^^^^^^^^^^^^^^^^^^^^^^^^^
    #      top level package
    node_map[node] = '.'.join(node.split('.')[0:4])

# Use map to set node attributes
nx.set_node_attributes(G, node_map, 'top-level package')

# Save the graph as GraphML
nx.write_graphml(G, 'data/guava.annotated.graphml')

