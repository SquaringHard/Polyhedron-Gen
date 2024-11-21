import numpy
from scipy.spatial import Delaunay
from matplotlib import pyplot
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def generate_convex_polyhedron(n, a = 10, b = 10, c = 10):
    # calculate number of points on each face excluding the corners
    n -= 8
    n //= 6

    # generate points
    points = numpy.zeros((n * 6 + 8, 3), dtype=numpy.float64)
    points[:n * 2, 1:] = numpy.random.rand(n * 2, 2)
    points[n * 2:n * 4, :2] = numpy.random.rand(n * 2, 2)
    points[n * 4:-8, [0, 2]] = numpy.random.rand(n * 2, 2)
    points[:n, 0] = points[n * 2:n * 3, 2] = points[n * 4:n * 5, 1] = 1
    points[-8:] = [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]]

    # triangulate faces
    dummy_points = [[0, 0], [0, 1], [1, 0], [1, 1]]
    poly1 = Delaunay(numpy.concatenate([points[:n, 1:], dummy_points])).simplices
    poly2 = Delaunay(numpy.concatenate([points[n:n * 2, 1:], dummy_points])).simplices
    poly3 = Delaunay(numpy.concatenate([points[n * 2:n * 3, :2], dummy_points])).simplices
    poly4 = Delaunay(numpy.concatenate([points[n * 3:n * 4, :2], dummy_points])).simplices
    poly5 = Delaunay(numpy.concatenate([points[n * 4:n * 5, [0, 2]], dummy_points])).simplices
    poly6 = Delaunay(numpy.concatenate([points[n * 5:n * 6, [0, 2]], dummy_points])).simplices
    points *= [a, b, c]

    # adjust corner indices
    poly1[poly1 >= n] += n * 5 + 4  # n + i -> 6n + 4 + i
    poly2[poly2 >= n] += n * 4      # n + i -> 5n + i
    mask = poly3 >= n
    poly3[mask] += n
    poly3[mask] *= 2
    poly3[mask] += 1                # n + i -> 4n + i * 2 + 1
    mask = poly4 >= n
    poly4[mask] *= 2
    poly4[mask] += n                # n + i -> 3n + i * 2
    poly5[poly5 >= n + 2] += 2
    poly5[poly5 >= n] += n + 2      # n + i -> 2n + i + 2 + i // 2 * 2
    poly6[poly6 >= n + 2] += 2      # n + i -> n + i + i // 2 * 2

    # adjust all indices and concatenate
    poly2 += n
    poly3 += n * 2
    poly4 += n * 3
    poly5 += n * 4
    poly6 += n * 5
    polys = numpy.concatenate([poly1, poly2, poly3, poly4, poly5, poly6])

    # plot the polyhedron
    fig = pyplot.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.add_collection3d(Poly3DCollection([points[i] for i in polys], edgecolors='k', facecolors='paleturquoise', alpha=.8))
    pyplot.show()
    
    # # write the polyhedron to file
    # v = len(points)
    # f = len(polys)
    # with open('cube{}.geom'.format(v), 'w') as file:
    #     file.write(f"{v} {f} {v + f - 2}\n")
    #     for i in points:
    #         file.write(f"{i[0]} {i[1]} {i[2]}\n")
    #     for i in polys:
    #         file.write(f"3 {i[0]} {i[1]} {i[2]}\n")

generate_convex_polyhedron(100)