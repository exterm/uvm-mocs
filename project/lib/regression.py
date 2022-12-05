from typing import List

import scipy.stats as stats
import numpy as np

def regression_confidence(percent, sample_size, regression_result):
  # we only have a sample, know nothing about the population, so we should use
  #  the t-statistic
  tinv = lambda p, df: abs(stats.t.ppf(p/2, df))
  ts = tinv(1-(percent/100.), sample_size-2)
  print(f"slope ({percent}%): {regression_result.slope:.6f} +/- {ts*regression_result.stderr:.6f}")
  print(f"intercept ({percent}%): {regression_result.intercept:.6f}"
        f" +/- {ts*regression_result.intercept_stderr:.6f}")

def compute_linear_regression(x: List[float], y: List[float]):
    result = stats.linregress(np.log10(x), np.log10(y))
    # print(f"R squared: {result.rvalue**2}")
    return result
