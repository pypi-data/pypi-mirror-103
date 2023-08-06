# weighted-delaunay
A packaged used to calculate the weighted delaunay triangulation in N-dimensions

# Usage

## WeightedDelaunay(points, weights)
### Paramesters
- points: ndarray with all the points
- weights: a list of weights that matches the index of the points
### Returns
A weighted Delaunay datastructure

## triangulation()
### Returns
A list of the simplexes for the triangulation

## add_point(point, weight)
### Paramesters
- point: the point to add
- weight: the weight of that point
### Returns
N/A