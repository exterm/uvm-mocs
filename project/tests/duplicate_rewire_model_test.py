import lib.duplicate_rewire_model as drm

def test_generate_initial_network():
    m0 = 10
    k0 = 2
    G = drm.generate_initial_network(m0, k0)

    assert len(G.nodes) == m0
    nodelist = list(G.nodes)
    assert G.out_degree(nodelist[0]) == 0
    assert G.out_degree(nodelist[1]) == 1
    assert all(G.out_degree(node) == k0 for node in nodelist[2:])


def test_generate_network():
    G = drm.generate_network(m0=10, k0=2, N=100, beta=0.5, delta=0.5)
    assert len(G.nodes) == 100
    assert len(G.edges) > 0

