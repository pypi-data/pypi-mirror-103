import unittest
from weightedDelaunay import WeightedDelaunay
import numpy as np


class TestWeightedDelaunay(unittest.TestCase):
    def test_no_weight(self):
        weights = [0]*10
        points = np.array([[3, 4], [5, 12], [10, 24], [24, 7], [12, 0], [3, 2], [2, 11], [5, 13], [21, 3], [1, 0]])
        wd = WeightedDelaunay(points, weights)
        self.assertListEqual(wd.tiangulation(), [[6, 0, 9], [5, 0, 9], [5, 4, 9], [5, 4, 0], [7, 2, 3], [7, 6, 2],
                                                 [1, 8, 3], [1, 7, 3], [1, 8, 4], [1, 4, 0], [1, 6, 0], [1, 7, 6]])

    def test_weights(self):
        points = np.array([[3, 4], [5, 12], [10, 24], [24, 7], [12, 0], [3, 2], [2, 11], [5, 13], [21, 3], [1, 0]])
        weights = [1, 2, 3, 2, 2, 3, 4, 3, 1, 0, 3]
        wd = WeightedDelaunay(points, weights)
        self.assertListEqual(wd.tiangulation(), [[6, 0, 9], [5, 0, 9], [5, 4, 9], [5, 4, 0], [7, 2, 3], [7, 6, 2],
                                                 [7, 8, 3], [1, 8, 4], [1, 7, 8], [1, 4, 0], [1, 6, 0], [1, 7, 6]])

    def test_weights2(self):
        points = np.array([[1, 4], [5, 2], [13, 2], [2, 7], [22, 0], [3, 3], [2, 1], [5, 3], [1, 3], [1, 9]])
        weights = [3, 2, 1, 3, 2, 3, 3, 3, 1, 1]
        wd2 = WeightedDelaunay(points, weights)
        self.assertListEqual(wd2.tiangulation(), [[2, 9, 4], [2, 6, 4], [1, 2, 6], [1, 7, 6], [1, 7, 2], [0, 8, 6],
                                                   [5, 7, 6], [5, 0, 6], [3, 0, 9], [3, 5, 0], [3, 5, 7], [3, 2, 9],
                                                   [3, 7, 2]])
        self.assertListEqual(wd2.tiangulation(), [[2, 9, 4], [2, 6, 4], [1, 2, 6], [1, 7, 6], [1, 7, 2], [0, 8, 6],
                                                  [5, 7, 6], [5, 0, 6], [3, 0, 9], [3, 5, 0], [3, 5, 7], [3, 2, 9],
                                                  [3, 7, 2]])

    def test_add_point(self):
        points = np.array([[1, 4], [5, 2], [13, 2], [2, 7], [22, 0], [3, 3], [2, 1], [5, 3], [1, 3]])
        weights = [3, 2, 1, 3, 2, 3, 3, 3, 1]
        wd3 = WeightedDelaunay(points, weights)
        self.assertListEqual(wd3.tiangulation(), [[2, 3, 4], [2, 6, 4], [7, 2, 3], [8, 0, 6], [1, 2, 6], [1, 7, 6],
                                                  [1, 7, 2], [5, 0, 6], [5, 7, 6], [5, 0, 3], [5, 7, 3]])
        wd3.add_point([1, 9], 1)
        self.assertListEqual(wd3.tiangulation(), [[2, 9, 4], [2, 6, 4], [1, 2, 6], [1, 7, 6], [1, 7, 2], [0, 8, 6],
                                                  [5, 7, 6], [5, 0, 6], [3, 0, 9], [3, 5, 0], [3, 5, 7], [3, 2, 9],
                                                  [3, 7, 2]])



if __name__ == '__main__':
    unittest.main()
