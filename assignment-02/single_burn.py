from core_simulation import (forestSimulation, ForestConfig)
from plots_from_simulation import (plots)

# 1. Prepare an initial state
# 2. Set a random cell on fire
# 3. Run the simulation until no cells are burning
# 4. Repeat 1-3 for n times and record the total number of cells burned

REPETITIONS = 10
INITIAL_DENSITY = 0.4

config = ForestConfig(width=100, height=100, p_tree=INITIAL_DENSITY,
                      p_sprout=0, p_propagate=0, p_lightning=0, seed=17)

sim = forestSimulation(config)
def prepare_initial_state():
    # initial state with one random burning cell
    initial_state = sim.random_world()
    initial_state[sim.rng.randint(0, config.height), sim.rng.randint(0, config.width)] = 2
    return initial_state

total_burned_results = []
for i in range(REPETITIONS):
    sim.simulate(stop_when_no_burning=True, initial_state=prepare_initial_state())
    total_burned_results += [sum([frame[0] for frame in sim.stats])]

print(total_burned_results)
