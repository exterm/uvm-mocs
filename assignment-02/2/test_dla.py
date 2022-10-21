import numpy as np
import dla
from hypothesis import given
# import hypothesis.extra.numpy as hnp
import hypothesis.strategies as st

# unit tests for dla.py using hypothesis
# https://hypothesis.readthedocs.io/en/latest/

# test that get_neighbor_coords returns a list of the correct length
# with all coordinates within the world
@given(st.integers(0, dla.SIZE - 1), st.integers(0, dla.SIZE - 1))
def test_get_neighbor_coords(row, column):
    world = dla.blank_world()
    neighbors = dla.get_neighbor_coords(world, row, column)
    assert len(neighbors) == 4
    for neighbor in neighbors:
        assert 0 <= neighbor[0] < dla.SIZE
        assert 0 <= neighbor[1] < dla.SIZE

# test that blank_world returns a world of the correct size
def test_blank_world():
    world = dla.blank_world()
    assert world.shape == (dla.SIZE, dla.SIZE)

# test that animate_history returns a function
def test_animate_history():
    history = [dla.blank_world() for _ in range(dla.STEPS)]
    plot = None
    assert callable(dla.animate_history(history, plot))
