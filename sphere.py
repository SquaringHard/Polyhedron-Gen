import numpy
from scipy.spatial import ConvexHull
from matplotlib import pyplot
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def generate_convex_polyhedron(n, a = 10, b = 10, c = 10):
    # generate z coordinates and theta
    points = numpy.zeros((n, 3))
    points[:, 2] = numpy.random.rand(n) * 2 - 1
    theta = numpy.random.rand(n) * 2 * numpy.pi

    # calculate x, y and z coordinates
    points[:, 0] = points[:, 1] = numpy.sqrt(1 - points[:, 2] ** 2)
    points[:, 0] *= numpy.cos(theta) * a
    points[:, 1] *= numpy.sin(theta) * b
    points[:, 2] *= c

    # triangulate the points
    poly = ConvexHull(points).simplices

    # write the polyhedron to file
    with open('sphere{}.geom'.format(n), 'w') as file:
        f = len(poly)
        file.write(f"{n} {f} {n + f - 2}\n")
        for i in points:
            file.write(f"{i[0]} {i[1]} {i[2]}\n")
        for i in poly:
            file.write(f"3 {i[0]} {i[1]} {i[2]}\n")

    # plot the polyhedron
    fig = pyplot.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.add_collection3d(Poly3DCollection([points[i] for i in poly], edgecolors='k', facecolors='paleturquoise', alpha=.8))
    pyplot.show()

generate_convex_polyhedron(100)