from pylab import *
import numpy as np

state = 1.
result = [state]
limit = 10000


def observe(result, state):
    return result + [state]


def update(state):
    x = state
    return x + x*(1-x/limit)


for t in range(30):
    state = update(state)
    result = observe(result, state)

plot(result)
show()