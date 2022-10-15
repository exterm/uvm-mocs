print("Importing libraries...")
#
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import matplotlib.colors as clrs
import numpy as np
from enum import Enum
print("Done.")

# Model forest fires in a way that demonstrates the following:
# - repeated controlled burns can reduce the maximum size of a fire
#
# Minimal setup:
# - 2D grid of cells
# - each cell is either empty or contains a tree
# - each cell has 8 neighbors
# - each tree cell has a probability of catching fire spontaneously from lightning
# - each tree cell catches fire if any of its neighbors are on fire
# - each tree cell burns for exactly one time step
# - each empty cell fills with a tree with probability P_TREE
#
# States: 0 = empty, 1 = tree, 2 = burning
#
# We want to measure the distribution of the maximum size of a fire with and without controlled burns.
#
# We can later expand this model to include:
# - wind
# - trees age and die
# - different types of trees

WIDTH = 120
HEIGHT = 100
STEPS = 750
RENDER_INTERVAL = 25
P_TREE = 0.01 # probability of a cell initially containing a tree
P_SPROUT = 0.0005 # likelihood of an empty cell sprouting a tree each step
P_PROPAGATE = 0.001 # likelihood of a tree propagating to a neighboring empty cell
P_LIGHTNING = 0.00005 # likelihood of a tree catching fire each step

S_EMPTY = 0
S_TREE = 1
S_BURNING = 2

print("Initializing random state..")
rng = np.random.RandomState()


def blank_world():
    return np.zeros((HEIGHT, WIDTH))


def random_world():
    return rng.choice([1, 0], size=(HEIGHT, WIDTH), p=[P_TREE, 1 - P_TREE])

def step(current_state):
    next_state = blank_world()
    for row in range(len(next_state)):
        for col in range(len(next_state[row])):
            if current_state[row][col] == S_TREE:
                if rng.random() < P_LIGHTNING:
                    next_state[row][col] = S_BURNING
                else:
                    next_state[row][col] = catch_fire(row, col, current_state)
            elif current_state[row][col] == S_BURNING:
                next_state[row][col] = S_EMPTY
            else:
                # empty
                if rng.random() < P_SPROUT:
                    next_state[row][col] = S_TREE
                else:
                    next_state[row][col] = propagate(row, col, current_state)
    return next_state


def catch_fire(row, column, current_state):
    neighbors = get_neighbors(row, column, current_state)
    burning_neighbor = any(neighbors[neighbors == S_BURNING])
    if burning_neighbor:
        return S_BURNING
    else:
        return S_TREE

def propagate(row, column, current_state):
    neighbors = get_neighbors(row, column, current_state)
    number_of_tree_neighbors = neighbors[neighbors == S_TREE].size
    if rng.random() < P_PROPAGATE * number_of_tree_neighbors:
        return S_TREE
    return S_EMPTY


def get_neighbors(row, column, current_state):
    # Moore neighborhood and periodic bundary condition
    rowup = (row - 1) % HEIGHT
    rowdown = (row + 1) % HEIGHT
    colleft = (column - 1) % WIDTH
    colright = (column + 1) % WIDTH
    return np.array([
        current_state[rowup][colleft],
        current_state[rowup][column],
        current_state[rowup][colright],
        current_state[row][colleft],
        current_state[row][colright],
        current_state[rowdown][colleft],
        current_state[rowdown][column],
        current_state[rowdown][colright]
    ])

def simulate(steps):
  world = random_world()
  history = []
  for i in range(steps):
    if i%50 == 0:
      print(f"Step {i}/{steps}")
    stats = analyze(world)
    world = step(world)
    history += [(world, stats)]
  return history


def analyze(current_state):
  '''
  Return statistics about the current state of the world. For now:
  - fractions of cells that are burning
  - fractions of cells that have trees on them
  '''
  cells = current_state.flatten()
  burning = 0
  trees = 0
  for cell in cells:
    if cell == S_BURNING:
      burning += 1
    elif cell == S_TREE:
      trees += 1
  return (burning / len(cells), trees / len(cells))

def print_stats(history):
  largest_fire = np.max([h[1][0] for h in history]) * HEIGHT * WIDTH
  highest_tree_density = np.max([h[1][1] for h in history])
  print("Statistics:")
  print(f" Largest fire: {largest_fire}")
  print(f" Highest tree density: {highest_tree_density}")

print("Simulating...")
history = simulate(STEPS)
print_stats(history)

def animate(i):
    worldplot.set_data(history[i][0])
    return [worldplot]

print("Initializing plot..")
fig = plt.figure()
ax = fig.add_subplot()
ax.axis(False)

colors = clrs.ListedColormap(['white', 'green', 'red'])  # type: ignore
worldplot = ax.imshow(blank_world(),
                      cmap=colors,
                      aspect='equal',
                      vmin=0,
                      vmax=2)

print("Animation starting...")
anim = ani.FuncAnimation(fig,
                         animate,
                         STEPS,
                         interval=RENDER_INTERVAL,
                         blit=True,
                         repeat=False)
plt.tight_layout(pad=0)
# writervideo = ani.FFMpegWriter(fps=1000 / RENDER_INTERVAL)
# print("Writing video...")
# anim.save('output/trees.mp4', writer=writervideo)
# print("Writing image...")
# plt.savefig('output/animated_2d_ca.png', dpi=600)
print("Show!")
plt.show()
print(history)
