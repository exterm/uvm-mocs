from lib.core_simulation import (forestSimulation, forestConfig)
from lib.plots_from_simulation import (plots)
import argparse
# Run the forest fire model repeatedly with different periodic interventions.
# Measure the resulting average tree cover.
# This measurement might not be easy because the system may not stabilize or may aexhibit a limit cycle.
# So for now I'll just run a few simulations and visualize the results.

parser = argparse.ArgumentParser()
parser.add_argument("p_sprout", type=float)
parser.add_argument("intervene_every", type=int)
args = parser.parse_args()

WIDTH = 120
HEIGHT = 100
STEPS = 1000
P_TREE = 0.25  # probability of a cell initially containing a tree
P_SPROUT = args.p_sprout  # likelihood of an empty cell sprouting a tree each step
P_PROPAGATE = 0  # likelihood of a tree propagating to a neighboring empty cell
P_LIGHTNING = 0  # likelihood of a tree catching fire each step

INTERVENTION_EVERY=args.intervene_every

config = forestConfig(WIDTH, HEIGHT, P_TREE, P_SPROUT, P_PROPAGATE, P_LIGHTNING, 0)
sim = forestSimulation(config)
sim.simulate(steps=0)

while len(sim.history) < STEPS:
    print(f"{len(sim.history)}/{STEPS}")
    sim.spark_fire()
    sim.continue_simulation(steps=INTERVENTION_EVERY)

plots(
    sim,
    image_filename=f'PIs_PT{P_TREE}_PS{P_SPROUT}_Ev{INTERVENTION_EVERY}.png',
    # anim_interval_ms=25,
    # video_filename=f'PIs_PT{P_TREE}_PS{P_SPROUT}_Ev{INTERVENTION_EVERY}.mp4',
    )
