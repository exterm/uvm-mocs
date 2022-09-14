from pylab import *
import numpy as np
import pandas as pd

prey_growth = 0.5
prey_limit = 100
predator_decay = 0.5

kill_rate = 0.01
nourish_rate = 0.015

state = [100., 100.]
result = [state]


def observe(result, state):
    return result + [state]


def update(state):
    prey, predators = state

    killed = (1 - 1 / (kill_rate * predators + 1)) * prey
    predators_born = nourish_rate * predators * prey

    new_prey = prey + prey_growth * prey * (1 - prey / prey_limit) - killed
    new_predators = predators - predator_decay * predators + predators_born
    return [new_prey, new_predators]


for t in range(250):
    state = update(state)
    result = observe(result, state)

result = pd.DataFrame(result)
result.columns = ["prey", "predators"]

if False:
    # time series
    ax = result.plot(y="prey")
    result.plot(y="predators", ax=ax)
else:
    # phase space
    prey_s, predators_s = np.array(result).T
    plot(prey_s, predators_s)

show()
