from controllers._controller import _controller
from svgpathtools import parse_path
import numpy as np
from matplotlib import pyplot as plt

class PathController(_controller):
    def __init__(self, path_str='M 300 100 C 100 100 200 200 200 300 L 250 350 L 220 300', width=500, height=500):
        super().__init__(1)

        # path_str = 'm 0 0 l 500 0'
        # path_str = 'm 0 0 c 0 0 250 50 500 0'
        self.name = 'PathController'
        print(path_str)
        path = parse_path(path_str)

        SAMPLES_PER_PX = 1

        self.points = []
        path_length = path.length()
        num_samples = int(path_length * SAMPLES_PER_PX)
        for i in range(num_samples):
            point = path.point(path.ilength(path_length * i / (num_samples-1)))
            self.points.append([point.real, height-point.imag])

        self.points = np.array(self.points)
        self.points -= self.points[0]
        self.current_point_idx = 0
        
        # get vectos
        unit_vectors = (self.points[1:] - self.points[:-1]) / np.sqrt(np.sum((self.points[1:] - self.points[:-1]) ** 2, axis=1, keepdims=True))

        # get vectors' orientations
        self.get_vector_degree = lambda unit_vector: np.degrees(np.arctan2(unit_vector[1], unit_vector[0]))
        self.get_vector = lambda angle: np.array([np.cos(np.radians(angle)), np.sin(np.radians(angle))])

        degrees = np.array([0] + [self.get_vector_degree(unit_vectors[idx]) - self.get_vector_degree(unit_vectors[idx + 1]) for idx in range(len(unit_vectors) - 1)] + [0])

        # find checkpoints
        self.checkpoints = np.abs(degrees) > 0.5
        self.checkpoints[-1] = True
        self.stopped = False


        # reduce the checkpoints
        for idx in range(len(self.checkpoints)):
            self.checkpoints[idx] = self.checkpoints[idx] and sum(self.checkpoints[idx - 20: idx]) == 0

        self.drawd = False
        self.done_points = np.array([[0,0]])

    def update_plot(self):

        if not self.drawd: 
            self.drawd = True
            plt.ion()
            self.fig = plt.figure()
            self.ax = self.fig.add_subplot(111)

        self.ax.cla()
        x, y = self.points.T
        self.ax.scatter(x,y, s=1)

        [self.ax.scatter(x[idx], y[idx], color='red', s=20) if ele else None for idx, ele in enumerate(self.checkpoints)]
        x, y = self.done_points.T
        self.ax.scatter(x,y, s=1, color='red')
        self.ax.quiver(*self.robot_position, *self.robot_vector, width=0.003, color='black')
        self.ax.quiver(*self.robot_position, *self.move_vector, width=0.003, color='green')
        self.ax.scatter(*self.target_point, color='yellow', s=20)
        self.ax.scatter(*self.robot_position, color='green', s=20)

        self.ax.axis('equal')
        self.fig.canvas.draw()

    def get_distance(self, point1 ,point2):
        return np.sqrt(np.sum((point1 - point2) ** 2))

    def get_step(self, angle_to_be=0, draw=True):

        if len(self.points) == 0 and not self.stopped:
            self.stopped = True
            return 0, 0
        elif len(self.points) == 0: return 0, 0

        # TODO: get the current xy position from robot
        self.robot_position = np.array([self.robot.actual_position[-1][0], self.robot.actual_position[-1][1]]) * 100
        robot_z_tilt = np.degrees(self.robot.tilt_angles[-1][2]) + angle_to_be
        # self.robot_position = np.array([0, 0])
        # robot_z_tilt = 0
        self.robot_vector = self.get_vector(robot_z_tilt)
        max_angle = 20
        max_d = 5

        # TODO: find the next target point
        if len(self.points) == 0: return 0, 0
        distances = np.array([self.get_distance(self.robot_position, self.points[idx]) if self.checkpoints[idx] or not any(self.checkpoints[: idx + 1]) else 9999 for idx in range(len(self.points))])
        # print(self.checkpoints[0:10])
        # print(distances[0:10])
        
        # print(len(self.done_points))
        if any(self.checkpoints) and distances[np.where(self.checkpoints)[0][0]] < 5: self.checkpoints[np.where(self.checkpoints)[0][0]] = False
        if any(self.checkpoints): next_point = min(np.where(self.checkpoints)[0][0], np.argmin(np.abs(distances - max_d*5)))
        else: next_point = np.argmin(np.abs(distances - max_d*5))
        if len(self.points) == 1 and distances[0] < 5: next_point = 1
        self.done_points = np.concatenate([self.done_points, self.points[: next_point]])
        self.points = self.points[next_point: ]
        self.checkpoints = self.checkpoints[next_point: ]
        if len(self.points) == 0: return 0, 0
        self.target_point = self.points[0]
        
        # TODO: get the vector to move and get its angle
        self.move_vector = (self.target_point - self.robot_position) / np.sqrt(np.sum((self.target_point - self.robot_position) ** 2))
        if np.degrees(np.arccos(np.dot(self.robot_vector, self.move_vector) / (np.linalg.norm(self.robot_vector) * np.linalg.norm(self.move_vector)))) > max_angle:
            δ = self.robot_vector[0] * self.move_vector[1] - self.robot_vector[1] * self.move_vector[0]
            δ = δ / np.abs(δ) if δ != 0 else 1
            self.move_vector = self.get_vector(robot_z_tilt + δ * max_angle)
            angle = δ * max_angle
            move_d = 0
        else:
            δ = self.robot_vector[0] * self.move_vector[1] - self.robot_vector[1] * self.move_vector[0]
            angle = δ * np.degrees(np.arccos(np.dot(self.robot_vector, self.move_vector) / (np.linalg.norm(self.robot_vector) * np.linalg.norm(self.move_vector))))
            move_d = min(max_d, self.get_distance(self.robot_position, self.target_point))

        # print('robot_position', self.robot_position, 'robot_z_tilt', robot_z_tilt, 'angle', angle, 'point', len(self.done_points) + next_point)
        # if draw: self.update_plot()
        return angle, move_d

    @property
    def is_finished(self):
        return len(self.points) == 0 and self.stopped