from lib import convert_pydeps_json

def test_convert():
    # read example json string from file
    with open('tests/pydeps_example.json') as f:
        pydeps = f.read()
    # convert to networkx graph
    G = convert_pydeps_json.convert(pydeps)

    # assert "wagtail" node has an edge to "wagtail.utils" and no other outgoing edges
    assert G.has_edge("wagtail", "wagtail.utils")
    assert len(G.out_edges("wagtail")) == 1

    # assert "wagtail.utils" node has no outgoing edges
    assert G.has_edge("wagtail.utils", "wagtail.actions")
    assert len(G.out_edges("wagtail.utils")) == 1

    # assert "wagtail.actions" node has no outgoing edges
    assert len(G.out_edges("wagtail.actions")) == 0

    # check that the graph has the expected number of nodes and edges
    assert len(G.nodes) == 3
    assert len(G.edges) == 2
