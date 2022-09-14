from pylab import *
import numpy as np

a = 0.5
b = -0.5
state = [1., 1.]
result = [state]


def observe(result, state):
    return result + [state]


def update(state):
    x, y = state
    return [a * x + y, b * x + y]


for t in range(30):
    state = update(state)
    result = observe(result, state)

xs, ys = np.array(result).T
plot(xs, ys)
# plot(result)
show()