import matplotlib.pyplot as plt
import matplotlib.animation as ani
import matplotlib.colors as clrs
import numpy as np

def plots(sim, anim_interval_ms: int | None = None, video_filename: str | None = None, image_filename: str | None = None):
    def animate(i):
        worldplot.set_data(sim.history[i])
        return [worldplot]

    config = sim.config

    if anim_interval_ms:
        fig = plt.figure()
        ax = fig.add_subplot()
        plt.tight_layout(pad=0)
        ax.axis(False)
        colors = clrs.ListedColormap(['white', 'green', 'red'])  # type: ignore
        worldplot = ax.imshow(np.zeros((config.height, config.width)),
                                cmap=colors,
                                aspect='equal',
                                interpolation='none',
                                vmin=0,
                                vmax=2)

        print("Animation starting...")
        anim = ani.FuncAnimation(fig,
                                animate,
                                len(sim.history),
                                interval=anim_interval_ms,
                                blit=True,
                                repeat=False)

        if video_filename:
            print("Writing video...")
            writervideo = ani.FFMpegWriter(fps=1000 // anim_interval_ms)
            anim.save('output/' + video_filename, writer=writervideo)

    print("Plotting...")
    num_cells = config.width * config.height
    fig, ax1 = plt.subplots()
    burn_history = [s[0] / num_cells for s in sim.stats]
    burnline, = ax1.plot(
        burn_history, label="Fraction of cells burning", color="red")
    ax1.set_ylabel("Fraction of cells burning")
    ax1.set_ylim(ymin=0)
    max_fire = np.max(burn_history)
    max_fire_line = ax1.axhline(y=max_fire,  color='red', linestyle='dotted',
                                label=f'Largest fire: ${round(max_fire * 100, 2)}\\%$')

    ax2 = ax1.twinx()
    density_history = [s[1] / num_cells for s in sim.stats]
    treeline, = ax2.plot(density_history, label="Tree density")
    percolation_threshold = 0.4
    percolation_threshold_line = ax2.axhline(y=percolation_threshold,  color='blue', linestyle='dotted',
                                   label=f'Percolation threshold: ${round(percolation_threshold * 100, 2)}\\%$')
    min_trees = np.min(density_history)
    min_trees_line = ax2.axhline(y=min_trees,  color='green', linestyle='dotted',
                                      label=f'Minimum tree density: ${round(min_trees * 100, 2)}\\%$')
    ax2.set_ylabel("Fraction of cells with trees")
    ax2.set_ylim(ymin=0)
    plt.legend(handles=[burnline, treeline,
               max_fire_line, percolation_threshold_line, min_trees_line])
    plt.xlabel("Step")
    plt.title("Forest fire simulation")

    if image_filename:
        print("Writing image...")
        plt.savefig('output/' + image_filename, dpi=600)

    print("Show!")
    plt.show()
