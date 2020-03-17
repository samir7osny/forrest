from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import matplotlib.pyplot as plt
from math import sin, cos, radians

class Cuboid(object):
    def __init__(self, size, angle_x=0, angle_y=0, angle_z=0, position=(0, 0, 0), parent=None, CoM=None, mass=None):
        self.size = size
        def shift(p): return p[0] - (p[1] / 2)
        self.correction = (-size[0] / 2, -size[1] / 2, -size[2] / 2)
        self.position = position
        self.mass = size[0] * size[1] * size[2] * 0.01 if mass is None else mass
        self.transform_matrices = []
        self.transformed_vertices = self.vertices

        if CoM is None:
            self.oCoM = (0, 0, 0)
        else:
            self.oCoM = CoM
        self.transformed_CoM = self.oCoM

        self.rotate_x(angle_x)
        self.rotate_y(angle_y)
        self.rotate_z(angle_z)
        self.move(self.position)
        self.set_parent(parent)

    def set_parent(self, parent):
        self.parent = parent

    def rotate_x(self, angle):
        angle = radians(angle)
        self.transform_matrices.append(
            [[1, 0, 0, 0], 
             [0, cos(angle), -sin(angle), 0],
             [0, sin(angle), cos(angle), 0],
             [0, 0, 0, 1]
            ])

    def rotate_y(self, angle):
        angle = radians(angle)
        self.transform_matrices.append(
            [[cos(angle), 0, sin(angle), 0], 
             [0, 1, 0, 0],
             [-sin(angle), 0, cos(angle), 0],
             [0, 0, 0, 1]
            ])

    def rotate_z(self, angle):
        angle = radians(angle)
        self.transform_matrices.append(
            [[cos(angle), -sin(angle), 0, 0],
             [sin(angle), cos(angle), 0, 0], 
             [0, 0, 1, 0],
             [0, 0, 0, 1]
            ])

    def move(self, dmove):
        self.transform_matrices.append(
            [[1, 0, 0, dmove[0]],
             [0, 1, 0, dmove[1]],
             [0, 0, 1, dmove[2]],
             [0, 0, 0, 1]
            ])
    
    @property
    def transformation(self):
        if self.parent is None or not isinstance(self.parent, Cuboid):
            return self.transform_matrices
        else:
            return self.transform_matrices + self.parent.transformation

    def inverse(self, matrix):
        return np.linalg.inv(matrix)

    def remove_transform(self):
        self.transformed_vertices = self.vertices
        self.transformed_CoM = self.oCoM

    # def inverse_transform(self):
    #     for matrix in reversed(self.transformation):
    #         for surface_id, surface in enumerate(self.transformed_vertices):
    #             for vertix_id, vertix in enumerate(surface):
    #                 self.transformed_vertices[surface_id, vertix_id] = np.transpose(np.matmul(self.inverse(matrix), np.transpose(list(self.transformed_vertices[surface_id, vertix_id]) + [1]))[: -1])

    def transform(self):
        self.remove_transform()
        for matrix in self.transformation:
            self.transformed_CoM = np.transpose(np.matmul(matrix, np.transpose(list(self.transformed_CoM) + [1]))[: -1])
            for surface_id, surface in enumerate(self.transformed_vertices):
                for vertix_id, vertix in enumerate(surface):
                    self.transformed_vertices[surface_id, vertix_id] = np.transpose(np.matmul(matrix, np.transpose(list(self.transformed_vertices[surface_id, vertix_id]) + [1]))[: -1])

    @property
    def CoM(self):
        # print(self.transformed_CoM)
        return self.transformed_CoM

    # @property
    # def center(self):
    #     center = [0, 0, 0]
    #     count = 0
    #     for surface in self.transformed_vertices:
    #         for vertix in surface:
    #             center += np.array(vertix)
    #             count += 1
    #     center /= count
    #     return center

    @property
    def vertices(self):
        X = [[[0, 1, 0], [0, 0, 0], [1, 0, 0], [1, 1, 0]],
             [[0, 0, 0], [0, 0, 1], [1, 0, 1], [1, 0, 0]],
             [[1, 0, 1], [1, 0, 0], [1, 1, 0], [1, 1, 1]],
             [[0, 0, 1], [0, 0, 0], [0, 1, 0], [0, 1, 1]],
             [[0, 1, 0], [0, 1, 1], [1, 1, 1], [1, 1, 0]],
             [[0, 1, 1], [0, 0, 1], [1, 0, 1], [1, 1, 1]]]
        X = np.array(X).astype(float)
        for i in range(3):
            X[:, :, i] *= self.size[i]
        X += np.array(self.correction)
        return X

    def draw(self, ax):
        self.transform()
        pc = Poly3DCollection(self.transformed_vertices, edgecolor="k", facecolors=np.repeat("crimson", 6), alpha=0.1)
        ax.add_collection3d(pc)

        xs = [x for surface in self.transformed_vertices[:, :, 0] for x in surface]
        ys = [x for surface in self.transformed_vertices[:, :, 1] for x in surface]
        zs = [x for surface in self.transformed_vertices[:, :, 2] for x in surface]
        return ((min(xs), max(xs)), (min(ys), max(ys)), (min(zs), max(zs)))


def CoM_objects(objects):
    M = sum([obj.mass for obj in objects])
    return (
        sum([obj.mass * obj.CoM[0] for obj in objects]) / M,
        sum([obj.mass * obj.CoM[1] for obj in objects]) / M,
        sum([obj.mass * obj.CoM[2] for obj in objects]) / M
    )

