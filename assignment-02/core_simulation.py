import itertools
import numpy as np
from itertools import repeat

class forestSimulation:

    def __init__(self, params):
        self.width = params["width"]
        self.height = params["height"]
        self.steps = params["steps"]
        self.p_tree = params["p_tree"]  # probability of a cell initially containing a tree
        self.p_sprout = params["p_sprout"] # likelihood of an empty cell sprouting a tree each step
        self.p_propogate = params["p_propogate"]  # likelihood of a tree propagating to a neighboring empty cell
        self.p_lightening = params["p_lightening"] # likelihood of a tree catching fire each step
        self.s_empty = params["s_empty"]
        self.s_tree = params["s_tree"]
        self.s_burning = params["s_burning"]
        self.rng = np.random.RandomState(params["seed"])
        self.allCells = list(itertools.product(range(self.height),range(self.width)))
        self.currentState = []
        self.history = []
        self.stats = []

    def blank_world(self):
        return np.zeros((self.height, self.width))
    
    def random_world(self):
        return self.rng.choice([1, 0], size=(self.height, self.width), p=[self.p_tree, 1 - self.p_tree])

    def step(self):
        next_state = self.blank_world()
        for row in range(len(next_state)):
            for col in range(len(next_state[row])):
                next_state[row][col] = self.step_one_cell(row, col)
        return next_state

    def step_one_cell(self, row, col):
        next_state = 0
        if self.currentState[row][col] == self.s_tree:
            if self.rng.random() < self.p_lightening:
                next_state = self.s_burning
            else:
                next_state = self.catch_fire(row, col)
        elif self.currentState[row][col] == self.s_burning:
            next_state = self.s_empty
        else:
            # empty
            if self.rng.random() < self.p_sprout:
                next_state = self.s_tree
            else:
                next_state = self.propagate(row, col)
        return next_state

    def catch_fire(self, row, column):
        neighbors = self.get_neighbors(row, column)
        burning_neighbor = any(neighbors[neighbors == self.s_burning])
        if burning_neighbor:
            return self.s_burning
        else:
            return self.s_tree

    def propagate(self, row, column):
        rand = self.rng.random()
        if rand > self.p_propogate * 8:
        # short-circuit if there's no way to propagate
            return self.s_empty
        neighbors = self.get_neighbors(row, column)
        number_of_tree_neighbors = neighbors[neighbors == self.s_tree].size
        if rand < self.p_propogate * number_of_tree_neighbors:
            return self.s_tree
        return self.s_tree

    def get_neighbors(self, row, column):
        # Moore neighborhood and periodic bundary condition
        rowup = (row - 1) % self.height
        rowdown = (row + 1) % self.height
        colleft = (column - 1) % self.width
        colright = (column + 1) % self.width
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
            if cell == self.s_burning:
                burning += 1
            elif cell == self.s_tree:
                trees += 1
        return (burning / len(cells), trees / len(cells))

    def simulate(self,):
        self.currentState = self.random_world()
        for i in range(self.steps):
            if i%50 == 0:
                print(f"Step {i}/{self.steps}")
            stats = self.analyze()
            world = self.step()
            self.history += [world]
            self.stats += [stats]
        return self.stats
        

    def print_stats(self):
        largest_fire = np.max([h[1][0] for h in self.history]) * self.height * self.width
        highest_tree_density = np.max([h[1][1] for h in self.history])
        print("Statistics:")
        print(f" Largest fire: {largest_fire}")
        print(f" Highest tree density: {highest_tree_density}")