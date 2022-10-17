## provides post-processing statistical extraction based on a list of 2d arrays, representing history of states

from percolation import *
import numpy as np

recoded_vals = {1:1, 0:0, 2: 0}

def recode_array(hist): ## takes a single history 2d array as input (1 step)
    rows, cols = hist.shape
    hist_flat = hist.flatten()
    hist_recoded = [recoded_vals[obs]  for obs in hist_flat]
    hist_array = np.array(hist_recoded).reshape(-1, cols)
    return hist_array

def detect_spanning(hist):
    recoded_arr = recode_array(hist)
    return percolates(recoded_arr)
