import matplotlib.pyplot as plt
import matplotlib.animation as ani
import matplotlib.colors as clrs
import numpy as np

def plots(sim, anim_interval_ms=50, video_filename=None, image_filename=None):
  def animate(i):
      worldplot.set_data(sim.history[i])
      return [worldplot]

  config = sim.config

  print("Initializing plot..")
  fig = plt.figure()
  ax = fig.add_subplot()
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
  plt.tight_layout(pad=0)

  if video_filename:
    print("Writing video...")
    writervideo = ani.FFMpegWriter(fps=1000 // anim_interval_ms)
    print("Writing video...")
    anim.save('output/video_filename', writer=writervideo)

  if image_filename:
    print("Writing image...")
    plt.savefig('output/animated_2d_ca.png', dpi=600)

  num_cells = config.width * config.height
  fig, ax1 = plt.subplots()
  burn_history = [s[0] / num_cells for s in sim.stats]
  burnline, = ax1.plot(
      burn_history, label="Fraction of cells burning", color="red")
  ax1.set_ylabel("Fraction of cells burning")
  ax1.set_ylim(ymin=0)
  max_fire = np.max(burn_history)
  max_fire_line = ax1.axhline(y=max_fire,  color='k', linestyle='dotted', lw=2,
                              label=f'Largest fire: ${round(max_fire * 100, 2)}\\%$')

  ax2 = ax1.twinx()
  treeline, = ax2.plot([s[1] / num_cells
                      for s in sim.stats], label="Tree density")
  ax2.set_ylabel("Fraction of cells with trees")
  ax2.set_ylim(ymin=0)
  plt.legend(handles=[burnline, treeline, max_fire_line])
  plt.xlabel("Step")
  plt.title("Forest fire simulation")
  print("Show!")
  plt.show()
