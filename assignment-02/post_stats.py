## provides post-processing statistical extraction based on a list of 2d arrays, representing history of states

from percolation import *
import numpy as np

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
