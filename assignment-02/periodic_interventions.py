from lib.core_simulation import (forestSimulation, forestConfig)
from lib.plots_from_simulation import (plots)

# Run the forest fire model repeatedly with different periodic interventions.
# Measure the resulting average tree cover.
# This measurement might not be easy because the system may not stabilize or may aexhibit a limit cycle.
# So for now I'll just run a few simulations and visualize the results.

WIDTH = 120
HEIGHT = 100
STEPS = 400
P_TREE = 0.01  # probability of a cell initially containing a tree
P_SPROUT = 0.0005  # likelihood of an empty cell sprouting a tree each step
P_PROPAGATE = 0.001  # likelihood of a tree propagating to a neighboring empty cell
P_LIGHTNING = 0  # likelihood of a tree catching fire each step

INTERVENTION_EVERY=40

config = forestConfig(WIDTH, HEIGHT, P_TREE, P_SPROUT, P_PROPAGATE, P_LIGHTNING, 0)
sim = forestSimulation(config)

sim.simulate(steps=INTERVENTION_EVERY)

while len(sim.history) < STEPS:
    sim.spark_fire()
    sim.continue_simulation(steps=INTERVENTION_EVERY)

plots(sim, image_filename="periodic-interventions-40-step.png")
