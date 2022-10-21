import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import matplotlib.colors as clrs
import sys
import matplotlib.pyplot as plt

sys.path.append('../1/lib')

from post_stats import (get_fractal_dimension,plot_fractal_dimension)

# Diffusion-limited aggregation

S_EMPTY = 0
S_AGGREGATE = 1
S_WALKER = 2

def get_neighbor_coords(world, row, column):
    # Periodic boundary condition
    rowup = (row - 1) % SIZE
    rowdown = (row + 1) % SIZE
    colleft = (column - 1) % SIZE
    colright = (column + 1) % SIZE
    # Moore neighborhood
    # return np.array([
    #     (rowup, colleft),
    #     (rowup, column),
    #     (rowup, colright),
    #     (row, colleft),
    #     (row, colright),
    #     (rowdown, colleft),
    #     (rowdown, column),
    #     (rowdown, colright)
    # ])
    # Von Neumann neighborhood
    return np.array([
        (rowup, column),
        (row, colleft),
        (row, colright),
        (rowdown, column)
    ])

def blank_world() -> np.ndarray:
    return np.zeros((SIZE, SIZE))


def animate_history(history: list[np.ndarray], plot):
    def animate(i):
        plot.set_data(history[i])
        return [plot]
    return animate

def render_animation(history: list[np.ndarray], write_video=False):
    fig = plt.figure()
    ax = fig.add_subplot()
    plt.tight_layout(pad=0)
    ax.axis(False)
    colors = clrs.ListedColormap(['white', 'black', 'gray']) # type: ignore
    worldplot = ax.imshow(blank_world(),
                          cmap=colors,
                          aspect='equal',
                          interpolation='none',
                          vmin=0,
                          vmax=2)

    print("Animation starting...")
    anim = ani.FuncAnimation(fig,
                             animate_history(history, worldplot),
                             len(history),
                             interval=ANIM_INTERVAL_MS,
                             blit=True,
                             repeat=False)
    if write_video:
        print("Writing video...")
        anim.save('dla.mp4', fps=1000//ANIM_INTERVAL_MS)
    print("Showing animation...")
    plt.show()

def step(world):
    '''
    Move all walkers one step, and add new walkers if necessary.
    - Walkers stop moving (become aggregate) if next to an aggregate cell.
    - Two walkers never move to the same cell.
    - Make sure there are always NUM_WALKERS walkers in the world by spawning new ones in random empty cells.
    '''
    new_world = world.copy()
    walkers = np.argwhere(world == S_WALKER)
    for row, column in walkers:
        neighbor_coords = get_neighbor_coords(world, row, column)

        if np.any(world[neighbor_coords[:, 0], neighbor_coords[:, 1]] == S_AGGREGATE):
            new_world[row, column] = S_AGGREGATE
        else:
            # move walker to an empty neighboring cell
            if BIAS_MOVEMENT:
                # Make walkers prefer moves towards the center of the world
                # so that they're twice as likely to move towards the center as away from it
                center = SIZE // 2
                # sort neighbors by distance from center
                neighbor_coords = neighbor_coords[np.argsort(np.linalg.norm(neighbor_coords - np.array([center, center]), axis=1))]
                # duplicate the first half of the neighbors
                neighbor_coords = np.concatenate((neighbor_coords[:len(neighbor_coords)//4*3], neighbor_coords))
            empty_neighbors = neighbor_coords[world[neighbor_coords[:, 0], neighbor_coords[:, 1]] == S_EMPTY]
            if len(empty_neighbors) > 0:
                new_row, new_column = empty_neighbors[np.random.randint(len(empty_neighbors))]
                new_world[new_row, new_column] = S_WALKER
                new_world[row, column] = S_EMPTY
    # Add new walkers at the outer edge of the world
    # (so that they can't immediately aggregate)
    num_new_walkers = NUM_WALKERS - np.count_nonzero(new_world == S_WALKER)
    if num_new_walkers > 0:
        # Choose random empty cells on the outer edge of the world
        # (so that they can't immediately aggregate)
        empty_cells = np.argwhere(new_world == S_EMPTY)
        outer_edge = np.logical_or(
            np.logical_or(empty_cells[:, 0] == 0, empty_cells[:, 0] == SIZE - 1),
            np.logical_or(empty_cells[:, 1] == 0, empty_cells[:, 1] == SIZE - 1)
        )
        outer_edge_cells = empty_cells[outer_edge]
        if len(outer_edge_cells) > 0:
            new_walkers = outer_edge_cells[np.random.randint(len(outer_edge_cells), size=num_new_walkers)]
            new_world[new_walkers[:, 0], new_walkers[:, 1]] = S_WALKER
    return new_world

SIZE = 125
STEPS = 8000
NUM_WALKERS = SIZE
BIAS_MOVEMENT = False
ANIM_INTERVAL_MS = 1000

# if file is run directly, not imported
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description='Diffusion-limited aggregation')
    parser.add_argument('--size', type=int, default=SIZE,
                        help='Size of the world')
    parser.add_argument('--steps', type=int, default=STEPS,
                        help='Number of steps to run')
    parser.add_argument('--num-walkers', type=int,
                        default=NUM_WALKERS, help='Number of walkers')
    parser.add_argument('--anim-interval', type=int,
                        default=ANIM_INTERVAL_MS, help='Animation interval in ms')
    parser.add_argument('--bias-movement', action='store_true',
                        help='Bias movement towards the center of the world')
    parser.add_argument('--write-video', action='store_true',
                        help='Write video to file')
    args = parser.parse_args()
    SIZE = args.size
    STEPS = args.steps
    NUM_WALKERS = args.num_walkers
    BIAS_MOVEMENT = args.bias_movement
    ANIM_INTERVAL_MS = args.anim_interval

    # initial state with a single fixed particle at the center
    initial_state = blank_world()
    initial_state[SIZE // 2][SIZE // 2] = S_AGGREGATE

    print("Simulation starting...")
    history = [initial_state]
    for i in range(STEPS):
        history.append(step(history[-1]))

    agg_cells = history[-1].copy()
    agg_cells[agg_cells == S_WALKER] = 0

    fig, ax = plt.subplots()
    ax.matshow(agg_cells, cmap='Greens')
    ax.axis('off')

    fig = plt.gcf()

    fractal_dimension_final_state, box_size_df = get_fractal_dimension(agg_cells)

    plot_fractal_dimension(box_size_df)

    print(f'Fractal dimension of final state: {fractal_dimension_final_state}')


    plt.show()

    # render
    #render_animation(history, args.write_video)
