import networkx as nx

# import edgelist and node name map.
# Combine by relabeling the nodes using data from the map.
# Save as GraphML file.

# Read in the edgelist as a digraph
G = nx.read_edgelist('data/guava.edges.csv', create_using=nx.MultiDiGraph())

# Read in the node name map
node_map = {}
with open('data/guava.map.csv') as f:
    for line in f:
        (name, id) = line.split()
        node_map[id] = name

# Relabel the nodes
G = nx.relabel_nodes(G, node_map)

# add nodes that are not in the edgelist
G.add_nodes_from(node_map.values())

def add_unique_edge_ids(G):
    """Add a unique id to each edge in the graph G.
    The id is added as an attribute to the edge.
    """
    for i, edge in enumerate(G.edges(data=True)):
        edge[2]['id'] = i
    return G

G = add_unique_edge_ids(G)

# Save the graph as GraphML where no two edges have the same id
nx.write_graphml(G, 'data/guava.graphml', edge_id_from_attribute='id')
