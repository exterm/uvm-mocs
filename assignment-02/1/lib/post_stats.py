## provides post-processing statistical extraction based on a list of 2d arrays, representing history of states

import numpy as np
import pandas as pd
import math
import statsmodels.api as sm
import matplotlib.pyplot as plt

def get_box_sum(row_start, row_end, col_start, col_end, mat):
    sub_mat = mat[row_start:row_end, col_start:col_end]
    return np.sum(sub_mat)  > 0

def get_fractal_dimension(hist):
    box_sizes = np.arange(1, min(hist.shape)//4, 1)
    coverage_results = []

    for size in box_sizes:
        col_starts = np.append([np.arange(0, hist.shape[1], size)], hist.shape[1])
        row_starts = np.append([np.arange(0, hist.shape[0], size)], hist.shape[0])
        size_count = 0
        for i in range(len(col_starts) -1):
            for j in range(len(row_starts)- 1):
                size_count += get_box_sum(int(row_starts[j]), int(row_starts[j+1]), int(col_starts[i]), int(col_starts[i + 1]), hist)
        coverage_results.append((size, size_count))

    coverage_results_df = pd.DataFrame(coverage_results, columns = ["size", "size_count"])
    coverage_results_df["size"] = coverage_results_df["size"].map(lambda x: math.log10(x))
    coverage_results_df["size_count"] = coverage_results_df["size_count"].map(lambda x: math.log10(x))
    mod = sm.OLS(coverage_results_df[["size_count"]], coverage_results_df[["size"]])
    res = mod.fit()
    return ( (res.params[0], res.conf_int(0.05)), coverage_results_df)

def plot_fractal_dimension(box_df, write_plots, steps, size, bias):
    fig, ax = plt.subplots()
    plt.xlabel("Box Size (Log10)")
    plt.ylabel("Number of Boxes (Log10)")
    plt.scatter(box_df["size"], box_df["size_count"])
    fig.suptitle(f"Box Size vs Number of Boxes: Fractal Dimension \n Steps: {steps} Dimension Size: {size}")
    fig.show()
    if write_plots:
        fig.savefig(f"Output/fractal_dim_steps{steps}_size{size}_bias_{bias}.png")

def plot_final_state(agg_cells, write_plots, steps, size, bias):
    fig, ax = plt.subplots()
    ax.matshow(agg_cells, cmap='Greens')
    ax.axis('off')
    fig = plt.gcf()
    fig.suptitle(f"Final State of Simulation \n Steps: {steps} Dimension Size: {size}")
    fig.show()
    if write_plots:
        fig.savefig(f"Output/final_state_steps{steps}_size{size}_bias_{bias}.png")


recoded_vals = {1:1, 0:0, 2: 0}

def recode_array(hist, recoded_vals): ## takes a single history 2d array as input (1 step)
    rows, cols = hist.shape
    hist_flat = hist.flatten()
    hist_recoded = [recoded_vals[obs]  for obs in hist_flat]
    hist_array = np.array(hist_recoded).reshape(-1, cols)
    return hist_array

def detect_spanning(hist):
    recoded_arr = recode_array(hist, recoded_vals)
    return percolates(recoded_arr)

def analyze(hist, S_BURNING = 2, S_TREE = 1):
    '''
    Return statistics about the current state of the world. For now:
    - fractions of cells that are burning
    - fractions of cells that have trees on them
    '''
    cells = hist.flatten()
    burning = 0
    trees = 0
    for cell in cells:
        if cell == S_BURNING:
            burning += 1
        elif cell == S_TREE:
            trees += 1
    return (burning, trees)
