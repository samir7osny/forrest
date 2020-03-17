import numpy as np
from math import sin, cos, radians

class Obj(object):
    def __init__(self, position):
        self.position = position
        self.transform_matrices = []
        self.childs = [] if self.childs is None else self.childs 
    
        self.move(self.position)


    @property
    def mass(self):
        return sum([child.mass for child in self.childs])

    @property
    def CoM(self):
        CoM_ = self.position
        total_mass = 0
        for child in self.childs:
            current_CoM = child.CoM
            CoM_ += np.array([current_CoM[0] * child.mass, current_CoM[1] * child.mass, current_CoM[2] * child.mass])
            total_mass += child.mass
        CoM_ = [ele / total_mass for ele in CoM_]
        # print('CoM', CoM_)
        return CoM_

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
        return self.transform_matrices

    def inverse(self, matrix):
        return np.linalg.inv(matrix)

    def draw(self, ax):
        xs = []
        ys = []
        zs = []
        for child in self.childs:
            info = child.draw(ax)
            xs.append(info[0][0])
            xs.append(info[0][1])
            ys.append(info[1][0])
            ys.append(info[1][1])
            zs.append(info[2][0])
            zs.append(info[2][1])
        return ((min(xs), max(xs)), (min(ys), max(ys)), (min(zs), max(zs)))
