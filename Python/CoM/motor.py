from CoM.cuboid import *
# import numpy as np

class Motor(Cuboid):
    def __init__(self, size, angle_x=0, angle_y=0, angle_z=0, position=(0, 0, 0), parent=None, rotation_axis_direction=(0, 1, 0), rotation_axis_position=(0, 0, -1), CoM=None, mode=0, mass=None):
        self.rotation_axis_direction = rotation_axis_direction
        self.rotation_axis_position = rotation_axis_position
        self.rotation_axis_position_transformed = list(self.rotation_axis_position)
        self.rotation_axis_position_transformed[2] = -self.rotation_axis_position_transformed[2]
        self.rotation_axis_position_transformed[1] = self.rotation_axis_position_transformed[1] - (size[1] / 2)
        self.motor_transfomation_matrices = []
        self.angle = 0
        self.mode = mode
        super().__init__(size, angle_x=angle_x, angle_y=angle_y, angle_z=angle_z, position=position, CoM=CoM, mass=mass)
        self.set_parent(parent)

    def rotate(self, angle):
        self.angle = angle % 360
        angle = radians(self.angle)
        
        translate_to_axis = [[1, 0, 0, self.rotation_axis_position[0]],
             [0, 1, 0, self.rotation_axis_position[1]],
             [0, 0, 1, self.rotation_axis_position[2]],
             [0, 0, 0, 1]
            ]
            
        if self.rotation_axis_direction[0] == 1:
            rotate_around_axis = [
             [1, 0, 0, 0], 
             [0, cos(angle), -sin(angle), 0],
             [0, sin(angle), cos(angle), 0],
             [0, 0, 0, 1]
            ]
        if self.rotation_axis_direction[1] == 1:
            rotate_around_axis = [
             [cos(angle), 0, sin(angle), 0], 
             [0, 1, 0, 0],
             [-sin(angle), 0, cos(angle), 0],
             [0, 0, 0, 1]
            ]
        if self.rotation_axis_direction[2] == 1:
            rotate_around_axis = [
             [cos(angle), -sin(angle), 0, 0],
             [sin(angle), cos(angle), 0, 0], 
             [0, 0, 1, 0],
             [0, 0, 0, 1]
            ]
        self.motor_transfomation_matrices = [translate_to_axis, rotate_around_axis, self.inverse(translate_to_axis)]

    @property
    def transformation(self):
        if self.parent is None or not isinstance(self.parent, Cuboid):
            return self.motor_transfomation_matrices + self.transform_matrices
        else:
            return self.motor_transfomation_matrices + self.transform_matrices + self.parent.transformation

    
    def transform(self):
        self.remove_transform()
        self.rotation_axis_position_transformed = list(self.rotation_axis_position)
        self.rotation_axis_position_transformed[2] = -self.rotation_axis_position_transformed[2]
        self.rotation_axis_position_transformed[1] = self.rotation_axis_position_transformed[1] - (self.size[1] / 2)
        if self.mode == 0:
            transformation = self.transformation
        else:
            if self.parent is None or not isinstance(self.parent, Cuboid):
                transformation = self.transform_matrices
            else:
                transformation = self.transform_matrices + self.parent.transformation
        for matrix in transformation:
            self.rotation_axis_position_transformed = np.transpose(np.matmul(matrix, np.transpose(list(self.rotation_axis_position_transformed) + [1]))[: -1])
            self.transformed_CoM = np.transpose(np.matmul(matrix, np.transpose(list(self.transformed_CoM) + [1]))[: -1])
            for surface_id, surface in enumerate(self.transformed_vertices):
                for vertix_id, vertix in enumerate(surface):
                    self.transformed_vertices[surface_id, vertix_id] = np.transpose(np.matmul(matrix, np.transpose(list(self.transformed_vertices[surface_id, vertix_id]) + [1]))[: -1])

    def draw(self, ax):
        self.transform()
        pc = Poly3DCollection(self.transformed_vertices, edgecolor="k", facecolors=np.repeat("crimson", 6), alpha=0.1)
        ax.add_collection3d(pc)
        ax.scatter([self.rotation_axis_position_transformed[0]], [self.rotation_axis_position_transformed[1]], [self.rotation_axis_position_transformed[2]], c=[20])

        xs = [x for surface in self.transformed_vertices[:, :, 0] for x in surface]
        ys = [x for surface in self.transformed_vertices[:, :, 1] for x in surface]
        zs = [x for surface in self.transformed_vertices[:, :, 2] for x in surface]
        return ((min(xs), max(xs)), (min(ys), max(ys)), (min(zs), max(zs)))