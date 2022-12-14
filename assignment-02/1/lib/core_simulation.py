import numpy as np
import sys
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
        if config.seed != None:
            self.rng = np.random.RandomState(config.seed)
        else:
            self.rng = np.random.RandomState()
        self.currentState = np.ndarray((0, 0))
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
        return self.S_EMPTY

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

    def analyze_current_state(self):
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

    def simulate(self, initial_state: np.ndarray | None = None, steps=None, stop_when_no_burning=False):
        if initial_state is None:
            self.currentState = self.random_world()
        else:
            self.currentState = initial_state
        self.history = []
        self.stats = []

        return self.continue_simulation(steps, stop_when_no_burning)


    def continue_simulation(self, steps=None, stop_when_no_burning=False):
        if steps != None:
            for i in range(steps):
                if i % 50 == 0:
                    print(f"Step {i}/{steps}")
                stats = self.analyze_current_state()
                world = self.step()
                self.currentState = world
                self.history += [world]
                self.stats += [stats]
        elif stop_when_no_burning:
            i = 0
            while True:
                if i % 10 == 0:
                  print(f"Step {i}")
                stats = self.analyze_current_state()
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
        return self.history

    def spark_fire(self):
        print("Finding best spot to spark fire")
        # set fire to the largest cluster of trees
        oldlimit = sys.getrecursionlimit()
        sys.setrecursionlimit(self.config.height * self.config.width + 100)
        row, col = self.largest_cluster()
        sys.setrecursionlimit(oldlimit)
        print(f"Sparking fire at {row}, {col}")
        self.currentState[row][col] = self.S_BURNING

    def largest_cluster(self):
        '''
        Returns the position of a cell in the largest cluster of trees.
        '''
        height = self.config.height
        width = self.config.width
        largest_cluster = 0
        largest_cluster_pos = (0, 0)
        visited = np.zeros((height, width))
        for row in range(height):
            for col in range(width):
                if visited[row][col] == 0 and self.currentState[row][col] == self.S_TREE:
                    cluster_size = self.cluster_size_helper(row, col, visited)
                    if cluster_size > largest_cluster:
                        largest_cluster = cluster_size
                        largest_cluster_pos = (row, col)
        return largest_cluster_pos

    def cluster_size_helper(self, row, col, visited):
        '''
        Helper function that calculates the size of a cluster of trees.
        '''
        height = self.config.height
        width = self.config.width
        if visited[row][col] == 1:
            return 0
        visited[row][col] = 1
        if self.currentState[row][col] != self.S_TREE:
            return 0
        size = 1
        rowup = (row - 1) % height
        rowdown = (row + 1) % height
        colleft = (col - 1) % width
        colright = (col + 1) % width
        size += self.cluster_size_helper(rowup, colleft, visited)
        size += self.cluster_size_helper(rowup, col, visited)
        size += self.cluster_size_helper(rowup, colright, visited)
        size += self.cluster_size_helper(row, colleft, visited)
        size += self.cluster_size_helper(row, colright, visited)
        size += self.cluster_size_helper(rowdown, colleft, visited)
        size += self.cluster_size_helper(rowdown, col, visited)
        size += self.cluster_size_helper(rowdown, colright, visited)
        return size

    def print_stats(self):
        largest_fire = np.max([s[0] for s in self.stats])
        highest_tree_density = np.max([s[1] for s in self.stats]) / self.config.height * self.config.width
        print("Statistics:")
        print(f" Largest fire: {largest_fire}")
        print(f" Highest tree density: {highest_tree_density}")
