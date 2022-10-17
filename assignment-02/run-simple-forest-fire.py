from core_simulation import (forestSimulation, forestConfig)
from plots_from_simulation import (plots)
import time
import cProfile

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
# - each empty cell fills with a tree with probability P_SPROUT
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
STEPS = 25
RENDER_INTERVAL = 25
P_TREE = 0.01 # probability of a cell initially containing a tree
P_SPROUT = 0.0005 # likelihood of an empty cell sprouting a tree each step
P_PROPAGATE = 0.001 # likelihood of a tree propagating to a neighboring empty cell
P_LIGHTNING = 0.00001  # likelihood of a tree catching fire each step

print("Simulating...")
startTime = time.time()
config = forestConfig(WIDTH, HEIGHT, P_TREE, P_SPROUT, P_PROPAGATE, P_LIGHTNING, 17)
sim = forestSimulation(config)
# profiler = cProfile.Profile()
# profiler.run('sim.simulate()')
# profiler.dump_stats("profile.out")
sim.simulate(steps=STEPS)
executionTime = (time.time() - startTime)
print('Simulation Execution time in seconds: ' + str(executionTime))
sim.print_stats()

plots(sim, anim_interval_ms=RENDER_INTERVAL)
