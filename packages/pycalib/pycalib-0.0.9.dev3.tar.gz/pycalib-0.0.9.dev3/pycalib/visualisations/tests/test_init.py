import unittest
import matplotlib.pyplot as plt
import numpy as np

from pycalib.visualisations import plot_reliability_diagram


class TestVisualisations(unittest.TestCase):
    def test_plot_reliability_diagram(self):
        n_c1 = n_c2 = 500
        p = np.concatenate((np.random.beta(2, 5, n_c1),
                            np.random.beta(4, 3, n_c2)))

        y = np.concatenate((np.zeros(n_c1), np.ones(n_c2)))

        s1 = 1/(1 + np.exp(-3*(p - 0.5)))
        s2 = 1/(1 + np.exp(-8*(p - 0.5)))

        p = np.vstack((1 - p, p)).T
        s1 = np.vstack((1 - s1, s1)).T
        s2 = np.vstack((1 - s2, s2)).T

        fig = plot_reliability_diagram(labels=y, scores=[s1, s2])
        self.assertIsInstance(fig, plt.Figure)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
