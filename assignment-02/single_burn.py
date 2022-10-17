import matplotlib.pyplot as plt
import numpy as np

from lib.core_simulation import (forestSimulation, forestConfig)
from lib.plots_from_simulation import (plots)

# 1. Prepare an initial state
# 2. Set a random cell on fire
# 3. Run the simulation until no cells are burning
# 4. Repeat 1-3 for n times and record the total number of cells burned

REPETITIONS = 10
INITIAL_DENSITIES = np.arange(0.28, 0.65, 0.02)

def prepare_initial_state():
    # initial state with one random burning cell
    initial_state = sim.random_world()
    initial_state[sim.rng.randint(0, config.height), sim.rng.randint(0, config.width)] = 2
    return initial_state

results = []

for density in INITIAL_DENSITIES:
  print(f"Running simulations for density {round(density, 3)}")
  config = forestConfig(width=100, height=100, p_tree=density,
                        p_sprout=0, p_propagate=0, p_lightning=0, seed=17)

  sim = forestSimulation(config)

  total_burned_results = []
  for i in range(REPETITIONS):
      sim.simulate(stop_when_no_burning=True, initial_state=prepare_initial_state())
      results += [[density, sum([frame[0] for frame in sim.stats]), len(sim.stats)]]

print(results)

fig = plt.figure()
ax1 = fig.add_subplot()
# plot the number of burned cells per density
burned_scatter = ax1.scatter([result[0] for result in results], [result[1] for result in results], label="number of burned cells")
ax1.set_ylabel("number of burned cells")
ax1.set_ylim(ymin=0)

# ax2 = ax1.twinx()
# # plot the number of steps per density
# steps_scatter = ax2.scatter([result[0] for result in results], [result[2]
#            for result in results], label="number of steps", color="gray")
# ax2.set_ylabel("number of steps")
# ax2.set_ylim(ymin=0)

plt.xlabel("initial density")
plt.legend(handles=[burned_scatter])
plt.show()
