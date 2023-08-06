from scipy.spatial import ConvexHull, Delaunay
import numpy as np


class WeightedDelaunay:
    def __init__(self, points, weights):
        self.points = points
        self.weights = weights
        self.complete = False
        self.tri = None

    def triangulation(self):
        if not self.complete:
            num, dim = np.shape(self.points)
            lifted = np.zeros((num, dim + 1))
            for i in range(num):
                p = self.points[i, :]
                lifted[i, :] = np.append(p, np.sum(p ** 2) - self.weights[i] ** 2)
            lifted = np.vstack((lifted, np.append(np.zeros((1, dim)), 1e12)))
            hull = ConvexHull(lifted)
            delaunay = []
            for simplex in hull.simplices:
                if num not in simplex:
                    delaunay.append(simplex.tolist())
            self.tri = delaunay
            self.complete = True
        return self.tri

    def add_point(self, point, weight):
        num, dim = np.shape(self.points)
        tmp = np.ndarray((num + 1, dim))
        for i in range(num):
            tmp[i] = self.points[i]
        tmp[num] = point
        self.points = tmp
        self.weights.append(weight)
        self.complete = False
