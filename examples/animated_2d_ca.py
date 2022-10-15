print("Importing libraries...")
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani
print("Done.")

WIDTH = 120
HEIGHT = 100
STEPS = 750
RENDER_INTERVAL = 50
P1 = 0.2

print("Initializing random state..")
rng = np.random.RandomState()


def blank_world():
    return np.zeros((HEIGHT, WIDTH))


def random_world():
    return rng.choice([1, 0], size=(HEIGHT, WIDTH), p=[P1, 1 - P1])


def get_living_neighbors(column, row, state):
    # Moore neighborhood and periodic bundary condition
    rowup = (row - 1) % HEIGHT
    rowdown = (row + 1) % HEIGHT
    colleft = (column - 1) % WIDTH
    colright = (column + 1) % WIDTH
    return state[rowup][colleft] + state[rowup][column] + state[rowup][colright] +\
        state[row][colleft] + state[row][colright] +\
        state[rowdown][colleft] + state[rowdown][column] + state[rowdown][colright]


def step(current_state):
    next_state = blank_world()
    for row in range(len(next_state)):
        for col in range(len(next_state[row])):
            living_neighbors = get_living_neighbors(col, row, current_state)
            # Any live cell with two or three live neighbours survives.
            # Any dead cell with three live neighbours becomes a live cell.
            # All other live cells die in the next generation. Similarly, all other dead cells stay dead.
            currently_alive = current_state[row][col] == 1
            if currently_alive:
                if living_neighbors == 2 or living_neighbors == 3:
                    next_state[row][col] = 1
                else:
                    next_state[row][col] = 0
            else:
                if living_neighbors == 3:
                    next_state[row][col] = 1
                else:
                    next_state[row][col] = 0
    return next_state



print("Initializing plot..")
fig = plt.figure()
ax = fig.add_subplot()
ax.axis(False)

worldplot = ax.imshow(blank_world(),
                      cmap='binary',
                      aspect='equal',
                      vmin=0,
                      vmax=1)
world = blank_world()

def animate(i):
    global world
    if i == 0:
        # initialize
        # world = random_world()
        world = blank_world()

        # r-pentomino
        world[51][52] = 1
        world[51][53] = 1
        world[52][51] = 1
        world[52][52] = 1
        world[53][52] = 1
    else:
        world = step(world)
    worldplot.set_data(world)
    return [worldplot]

print("Animation starting...")
anim = ani.FuncAnimation(fig,
                         animate,
                         STEPS,
                         interval=RENDER_INTERVAL,
                         blit=True,
                         repeat=False)
plt.tight_layout(pad=0)
writervideo = ani.FFMpegWriter(fps=1000 // RENDER_INTERVAL)
print("Writing video...")
anim.save('output/animated_2d_ca.mp4', writer=writervideo)
# print("Writing image...")
# plt.savefig('output/animated_2d_ca.png', dpi=600)
print("Show!")
plt.show()
