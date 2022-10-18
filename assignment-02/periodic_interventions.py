from lib.core_simulation import (forestSimulation, forestConfig)
from lib.plots_from_simulation import (plots)
import numpy as np
import matplotlib.pyplot as plt
import csv
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

SHA = ''

INTERVENTION_EVERY=args.intervene_every

config = forestConfig(WIDTH, HEIGHT, P_TREE, P_SPROUT,
                      P_PROPAGATE, P_LIGHTNING, 0)

def run_with_intervention(config, intervention_every, steps):
    sim = forestSimulation(config)
    sim.simulate(steps=0)

    while len(sim.history) < steps:
        print(f"{len(sim.history)}/{steps}")
        sim.spark_fire()
        sim.continue_simulation(steps=intervention_every)
    return sim

# sim = run_with_intervention(config, INTERVENTION_EVERY, STEPS)

# plots(
#     sim,
#     image_filename=f'{SHA}/PIs_PT{P_TREE}_PS{P_SPROUT}_Ev{INTERVENTION_EVERY}.png',
#     anim_interval_ms=25,
#     video_filename=f'{SHA}/PIs_PT{P_TREE}_PS{P_SPROUT}_Ev{INTERVENTION_EVERY}.mp4',
#     )

def sweep_frequency(config, intervention_every_values, steps, repetitions):
    '''
    Run the simulation with intervention and sweep the intervention frequency. Collect the results in a table.
    The table should record the average and mimimum tree cover for each intervention frequency.
    '''

    cell_count = config.width * config.height

    results = []
    for intervention_every in intervention_every_values:
        print(f"intervention_every={intervention_every}")
        for i in range(repetitions):
            sim = run_with_intervention(config, intervention_every, steps)
            tree_counts = np.array([s[1] for s in sim.stats])
            tree_cover = tree_counts / cell_count
            results.append((intervention_every, np.mean(tree_cover), np.min(tree_cover)))

    # dump the results to a CSV file
    with open(f'output/{SHA}/PIs_PT{P_TREE}_PS{P_SPROUT}_Sweep.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['intervention_every', 'mean_tree_cover', 'min_tree_cover'])
        writer.writerows(results)

    intervention_every = [r[0] for r in results]
    mean_tree_cover = [r[1] for r in results]
    min_tree_cover = [r[2] for r in results]

    fig, ax = plt.subplots()
    ax.scatter(intervention_every, mean_tree_cover, label='mean tree cover')
    ax.scatter(intervention_every, min_tree_cover, label='min tree cover')
    ax.set_xlabel('intervention frequency')
    ax.set_ylabel('tree cover')
    ax.legend()
    fig.savefig(f'output/{SHA}/PIs_PT{P_TREE}_PS{P_SPROUT}_Sweep.png')
    print(results)
    plt.show()

    return results


config = forestConfig(WIDTH, HEIGHT, P_TREE, P_SPROUT,
                      P_PROPAGATE, P_LIGHTNING, None)
# sweep_frequency(config, [1,2,3,4,5,7,10,15,30,50,100,200], 2000)
sweep_frequency(config, [1,2,5,10], 20, 3)
