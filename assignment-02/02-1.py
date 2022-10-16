from core_simulation import (forestSimulation, ForestConfig)
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import matplotlib.colors as clrs
import numpy as np
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
STEPS = 250
RENDER_INTERVAL = 25
P_TREE = 0.01 # probability of a cell initially containing a tree
P_SPROUT = 0.0005 # likelihood of an empty cell sprouting a tree each step
P_PROPAGATE = 0.001 # likelihood of a tree propagating to a neighboring empty cell
P_LIGHTNING = 0.00001  # likelihood of a tree catching fire each step

S_EMPTY = 0
S_TREE = 1
S_BURNING = 2


print("Simulating...")
startTime = time.time()
config = ForestConfig(WIDTH, HEIGHT, STEPS, P_TREE, P_SPROUT, P_PROPAGATE, P_LIGHTNING, 17)
sim = forestSimulation(config)
# profiler = cProfile.Profile()
# profiler.run('sim.simulate()')
# profiler.dump_stats("profile.out")
sim.simulate()
executionTime = (time.time() - startTime)
print('Simulation Execution time in seconds: ' + str(executionTime))
sim.print_stats()

def animate(i):
    worldplot.set_data(sim.history[i])
    return [worldplot]

print("Initializing plot..")
fig = plt.figure()
ax = fig.add_subplot()
ax.axis(False)

colors = clrs.ListedColormap(['white', 'green', 'red'])  # type: ignore
worldplot = ax.imshow(np.zeros((config.height, config.width)),
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

# writervideo = ani.FFMpegWriter(fps=1000 // RENDER_INTERVAL)
# print("Writing video...")
# anim.save('output/forest_fire.mp4', writer=writervideo)

# print("Writing image...")
# plt.savefig('output/animated_2d_ca.png', dpi=600)

fig, ax1 = plt.subplots()
burn_history = [s[0] for s in sim.stats]
burnline, = ax1.plot(burn_history, label="Fraction of cells burning", color="red")
ax1.set_ylabel("Fraction of cells burning")
# ax1.set_ylim(ymin=0)
max_fire = np.max(burn_history)
max_fire_line = ax1.axhline(y=max_fire,  color='k', linestyle='dotted', lw=2,
            label=f'Largest fire: ${round(max_fire * 100, 2)}\\%$')

ax2 = ax1.twinx()
# ax2.tick_params(axis='y', labelcolor='blue')
treeline, = ax2.plot([s[1] for s in sim.stats], label="Tree density")
ax2.set_ylabel("Fraction of cells with trees")
plt.legend(handles=[burnline, treeline, max_fire_line])
plt.xlabel("Step")
plt.title("Forest fire simulation")
print("Show!")
plt.show()
