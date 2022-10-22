## provides post-processing statistical extraction based on a list of 2d arrays, representing history of states

import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import scipy.stats as stats

def get_box_sum(row_start, row_end, col_start, col_end, mat):
    sub_mat = mat[row_start:row_end, col_start:col_end]
    return np.sum(sub_mat)  > 0

def regression_confidence(percent, sample_size, regression_result):
  # we only have a sample, know nothing about the population, so we should use
  #  the t-statistic
  def tinv(p, df): return abs(stats.t.ppf(p/2, df))
  ts = tinv(1-(percent/100.), sample_size-2)
  print(
      f"slope ({percent}%): {regression_result.slope:.6f} +/- {ts*regression_result.stderr:.6f}")
  print(f"intercept ({percent}%): {regression_result.intercept:.6f}"
        f" +/- {ts*regression_result.intercept_stderr:.6f}")

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
    regression = stats.linregress(coverage_results_df["size"], coverage_results_df["size_count"])
    regression_confidence(95, len(coverage_results_df), regression)
    return ( (regression.slope, regression.intercept), coverage_results_df)

def plot_fractal_dimension(box_df, write_plots, steps, size, bias, regression_params):
    slope, intercept = regression_params
    fig, ax = plt.subplots(layout='constrained')
    plt.xlabel("Box Size (Log10)")
    plt.ylabel("Number of Boxes (Log10)")
    plt.scatter(box_df["size"], box_df["size_count"])
    # plot regression line
    x = np.linspace(box_df["size"].min(), box_df["size"].max(), 100)
    y = slope * x + intercept
    plt.plot(x, y, color='red')
    fig.suptitle(f"Box Size vs Number of Boxes: Fractal Dimension \n Steps: {steps} Dimension Size: {size}")
    fig.show()
    if write_plots:
        fig.savefig(f"output/fractal_dim_steps{steps}_size{size}_bias_{bias}.png", dpi=600)

def plot_final_state(agg_cells, write_plots, steps, size, bias):
    fig, ax = plt.subplots(layout='constrained')
    ax.matshow(agg_cells, cmap='Greens')
    ax.axis('off')
    fig = plt.gcf()
    fig.suptitle(f"Final State of Simulation \n Steps: {steps} Dimension Size: {size}")
    fig.show()
    if write_plots:
        fig.savefig(f"output/final_state_steps{steps}_size{size}_bias_{bias}.png", dpi=600)


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
