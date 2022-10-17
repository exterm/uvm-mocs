import unittest
import numpy as np
from collections import namedtuple

forestConfig = namedtuple('forestConfig', [
  'width',
  'height',
  'p_tree',  # probability of a cell initially containing a tree
  'p_sprout',  # probability of an empty cell sprouting a tree each step
  'p_propagate',  # probability of a tree propagating to a neighboring empty cell
  'p_lightning',  # probability of a tree catching fire each step
  'seed' # random seed
  ])

class forestSimulation:
    S_EMPTY = 0
    S_TREE = 1
    S_BURNING = 2

    def __init__(self, config):
        self.config = config
        self.rng = np.random.RandomState(config.seed)
        self.currentState = []
        self.history = []
        self.stats = []

    def blank_world(self):
        return np.zeros((self.config.height, self.config.width))

    def random_world(self):
        return self.rng.choice([1, 0], size=(self.config.height, self.config.width), p=[self.config.p_tree, 1 - self.config.p_tree])

    def step(self):
        next_state = self.blank_world()
        for row in range(len(next_state)):
            for col in range(len(next_state[row])):
                next_state[row][col] = self.step_one_cell(row, col)
        return next_state

    def step_one_cell(self, row, col):
        next_state = 0
        if self.currentState[row][col] == self.S_TREE:
            if self.rng.random() < self.config.p_lightning:
                next_state = self.S_BURNING
            else:
                next_state = self.catch_fire(row, col)
        elif self.currentState[row][col] == self.S_BURNING:
            next_state = self.S_EMPTY
        else:
            # empty
            if self.rng.random() < self.config.p_sprout:
                next_state = self.S_TREE
            else:
                next_state = self.propagate(row, col)
        return next_state

    def catch_fire(self, row, column):
        neighbors = self.get_neighbors(row, column)
        burning_neighbor = any(neighbors[neighbors == self.S_BURNING])
        if burning_neighbor:
            return self.S_BURNING
        else:
            return self.S_TREE

    def propagate(self, row, column):
        rand = self.rng.random()
        if rand > self.config.p_propagate * 8:
        # short-circuit if there's no way to propagate
            return self.S_EMPTY
        neighbors = self.get_neighbors(row, column)
        number_of_tree_neighbors = neighbors[neighbors == self.S_TREE].size
        if rand < self.config.p_propagate * number_of_tree_neighbors:
            return self.S_TREE
        return self.S_TREE

    def get_neighbors(self, row, column):
        # Periodic boundary condition
        rowup = (row - 1) % self.config.height
        rowdown = (row + 1) % self.config.height
        colleft = (column - 1) % self.config.width
        colright = (column + 1) % self.config.width
        # Moore neighborhood
        return np.array([
            self.currentState[rowup][colleft],
            self.currentState[rowup][column],
            self.currentState[rowup][colright],
            self.currentState[row][colleft],
            self.currentState[row][colright],
            self.currentState[rowdown][colleft],
            self.currentState[rowdown][column],
            self.currentState[rowdown][colright]
        ])
        # Von Neumann neighborhood
        # return np.array([
        #     self.currentState[rowup][column],
        #     self.currentState[row][colleft],
        #     self.currentState[row][colright],
        #     self.currentState[rowdown][column]
        # ])

    def analyze(self):
        '''
        Return statistics about the current state of the world. For now:
        - fractions of cells that are burning
        - fractions of cells that have trees on them
        '''
        cells = self.currentState.flatten()
        burning = 0
        trees = 0
        for cell in cells:
            if cell == self.S_BURNING:
                burning += 1
            elif cell == self.S_TREE:
                trees += 1
        return (burning, trees)

    def simulate(self, initial_state=None, steps=None, stop_when_no_burning=False):
        if initial_state is None:
            self.currentState = self.random_world()
        else:
            self.currentState = initial_state
        self.history = []
        self.stats = []

        if steps:
          for i in range(steps):
              if i % 50 == 0:
                  print(f"Step {i}/{steps}")
              stats = self.analyze()
              world = self.step()
              self.currentState = world
              self.history += [world]
              self.stats += [stats]
        elif stop_when_no_burning:
            i = 0
            while True:
                if i % 10 == 0:
                  print(f"Step {i}")
                stats = self.analyze()
                world = self.step()
                self.currentState = world
                self.history += [world]
                self.stats += [stats]
                if stats[0] == 0:
                    break
                i += 1
        else:
            raise RuntimeError("Invalid simulation parameters")
        print("Done!")
        return self.stats

    def print_stats(self):
        largest_fire = np.max([s[0] for s in self.stats])
        highest_tree_density = np.max([s[1] for s in self.stats]) / self.config.height * self.config.width
        print("Statistics:")
        print(f" Largest fire: {largest_fire}")
        print(f" Highest tree density: {highest_tree_density}")

# Unit tests
class TestSimulation(unittest.TestCase):

    # these are low-effort tests and should not be used as an example for what good tests look like.
    # Better tests would be more thorough and would test the individual methods of the simulation class.
    # if we're testing small, fast things we can also use property-based testing (e.g. Hypothesis)
    # for much more concise tests.

    def test_basic_properties(self):
        steps = 10
        config = forestConfig(
            height=10,
            width=10,
            p_tree=0.5,
            p_lightning=0.1,
            p_sprout=0.1,
            p_propagate=0.1,
            seed=0
        )
        sim = forestSimulation(config)
        sim.simulate(steps=steps)

        self.assertEqual(len(sim.history), steps)
        self.assertEqual(len(sim.stats), steps)

        np.testing.assert_array_equal(sim.history[-1], sim.currentState)

    def test_golden_samples(self):
        config = forestConfig(
            height=10,
            width=10,
            p_tree=0.5,
            p_lightning=0.1,
            p_sprout=0.1,
            p_propagate=0.1,
            seed=0
        )
        sim = forestSimulation(config)
        sim.simulate(steps=10)
        # golden sample (brittle, but will do for now)
        expected = np.array([[1., 0., 1., 0., 1., 0., 1., 0., 2., 1.,],
                             [1., 1., 2., 0., 1., 1., 0., 2., 2., 2.,],
                             [0., 1., 1., 2., 1., 2., 1., 0., 2., 1.,],
                             [2., 0., 1., 0., 0., 0., 2., 0., 2., 1.,],
                             [0., 0., 1., 0., 2., 2., 2., 2., 2., 1.,],
                             [0., 1., 1., 0., 2., 1., 1., 1., 1., 2.,],
                             [0., 2., 0., 0., 1., 1., 0., 0., 0., 2.,],
                             [2., 2., 0., 0., 2., 1., 1., 0., 1., 2.,],
                             [1., 0., 0., 0., 2., 2., 2., 1., 1., 1.,],
                             [1., 2., 2., 0., 0., 0., 0., 2., 2., 1.,],])
        np.testing.assert_array_equal(sim.currentState, expected)

if __name__ == '__main__':
    unittest.main()
