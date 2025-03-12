from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
import os

def display(filename):
    vertices = []
    faces = []
    with open(filename, 'r') as file:
        v, f, _ = map(int, file.readline().split())
        for _ in range(v):
            vertices.append(list(map(float, file.readline().split())))
        for _ in range(f):
            _, *face = map(int, file.readline().split())
            faces.append([vertices[i] for i in face])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.add_collection3d(Poly3DCollection(faces, edgecolors='k', facecolors='paleturquoise', alpha=.8))
    ax.set_title(filename)
    plt.show()

# display('filename.geom')