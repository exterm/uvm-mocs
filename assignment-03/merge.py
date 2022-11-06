import networkx as nx

# import edgelist and node name map.
# Combine by relabeling the nodes using data from the map.
# Save as GraphML file.

# Read in the edgelist as a digraph
G = nx.read_edgelist('data/guava.edges.csv', create_using=nx.DiGraph())

# Read in the node name map
node_map = {}
with open('data/guava.map.csv') as f:
    for line in f:
        (name, id) = line.split()
        node_map[id] = name

print(node_map)

# Relabel the nodes
G = nx.relabel_nodes(G, node_map)

# Save the graph as GraphML
nx.write_graphml(G, 'data/guava.graphml')