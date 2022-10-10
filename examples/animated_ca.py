import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani


def rule_index(triplet):
    """
    Returns the index of the rule that generated the triplet.
    """
    L, C, R = triplet
    index = 7 - (4 * L + 2 * C + R)
    return int(index)


def CA_step(current_state, rule_number):
    rule_string = np.binary_repr(rule_number, 8)
    rule = np.array([int(bit) for bit in rule_string])

    all_triplets = np.stack([
        np.roll(current_state, 1),
        current_state,
        np.roll(current_state, -1),
    ])

    return rule[np.apply_along_axis(rule_index, 0, all_triplets)]


fig = plt.figure()
ax = fig.add_subplot()
ax.axis(False)

WIDTH = 300
STEPS = 150
RULE_NUMBER = 30

rng = np.random.RandomState(0)

blank = lambda: np.zeros((STEPS, WIDTH))

history = blank()
stateplot = ax.imshow(blank(), cmap='binary', aspect='equal', vmin=0, vmax=1)


def animate(i):
    global history
    if i == 0:
        history = blank()
        history[0] = rng.randint(0, 2, WIDTH)
    else:
        history[i] = CA_step(history[i - 1], RULE_NUMBER)

    stateplot.set_data(history)
    return [stateplot]


render_interval = 50
anim = ani.FuncAnimation(fig,
                         animate,
                         STEPS,
                         interval=render_interval,
                         blit=True,
                         repeat=False)
writervideo = ani.FFMpegWriter(fps=1000 / render_interval)
anim.save('output/animated_ca.mp4', writer=writervideo)
plt.savefig('output/animated_ca.png', dpi=600)
plt.show()
