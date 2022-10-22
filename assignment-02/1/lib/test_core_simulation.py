import unittest
import numpy as np
from core_simulation import (forestConfig, forestSimulation)

# Unit tests
class TestSimulation(unittest.TestCase):

    # these are low-effort tests and should not be used as an example for what good tests look like.
    # Better tests would be more thorough and would test the individual methods of the simulation class.
    # if we're testing small, fast things we can also use property-based testing (e.g. Hypothesis)
    # for much more concise tests.

    def test_basic_properties(self):
        steps = 10
        config = forestConfig(
            height=10,
            width=10,
            p_tree=0.5,
            p_lightning=0.1,
            p_sprout=0.1,
            p_propagate=0.1,
            seed=0
        )
        sim = forestSimulation(config)
        sim.simulate(steps=steps)

        self.assertEqual(len(sim.history), steps)
        self.assertEqual(len(sim.stats), steps)

        np.testing.assert_array_equal(sim.history[-1], sim.currentState)

    def test_golden_samples(self):
        config = forestConfig(
            height=10,
            width=10,
            p_tree=0.5,
            p_lightning=0.1,
            p_sprout=0.1,
            p_propagate=0.1,
            seed=0
        )
        sim = forestSimulation(config)
        sim.simulate(steps=10)
        # golden sample (brittle, but will do for now)
        expected = np.array([[2., 0., 0., 1., 0., 0., 0., 0., 0., 0.],
                             [2., 2., 0., 1., 0., 0., 0., 0., 2., 0.],
                             [0., 2., 1., 0., 0., 1., 1., 0., 2., 2.],
                             [2., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                             [0., 0., 2., 0., 0., 0., 0., 0., 0., 1.],
                             [1., 0., 0., 0., 0., 2., 0., 2., 0., 2.],
                             [1., 0., 1., 0., 0., 0., 1., 0., 0., 0.],
                             [1., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                             [0., 0., 0., 0., 2., 0., 0., 1., 0., 0.],
                             [2., 0., 1., 0., 0., 0., 1., 0., 1., 1.], ])
        np.testing.assert_array_equal(sim.currentState, expected)

    def test_spark_fire(self):
        config = forestConfig(
            height=10,
            width=10,
            p_tree=1,
            p_lightning=0,
            p_sprout=0,
            p_propagate=0,
            seed=0
        )
        sim = forestSimulation(config)
        sim.simulate(steps=0)
        sim.spark_fire()
        sim.continue_simulation(steps=max(config.height, config.width))

        # world should be empty
        expected = np.zeros((config.height, config.width))
        np.testing.assert_array_equal(sim.currentState, expected)
