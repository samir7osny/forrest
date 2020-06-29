from controllers._controller import _controller
from utils.pid_controller import PID
import numpy as np
import copy

class InclinationRollController(_controller):
    def __init__(self, accuracy=1):
        super().__init__(accuracy)

        self.tilt_angles = np.array([0, 0, 0])
        self.last_tilt_angles = []
        self.angle_controller = PID(Kp=1.5, Ki=2, Kd=0.8, guard=(-60, 60))
        self.leg_controller = PID(Kp=1, Ki=2, Kd=1.2, guard=(-20, 20))
        # self.right_leg_controller = copy.deepcopy(self.left_leg_controller)
        self.angle_control_value = 0
        self.left_leg_control_value = 0
        self.right_leg_control_value = 0
        self.name = 'InclinationRollController'

        # open('roll.txt', 'w').close()

    def update(self, sensors):
        self.last_tilt_angles.append(self.tilt_angles)
        if len(self.last_tilt_angles) > 10: self.last_tilt_angles.pop(0)
        
        self.tilt_angles = self.tilt_angles + np.degrees(np.array([sensors['gyro'][0], sensors['gyro'][1], sensors['gyro'][2]]) * (self.accuracy / 1000))

    def get_step(self):

        error = self.tilt_angles[0]

        current_angle_control_value = self.angle_controller(error)
        current_left_leg_control_value = self.leg_controller(error)
        current_right_leg_control_value = -current_left_leg_control_value

        # file = open('roll.txt', 'a')
        # file.write(str([error, self.leg_controller.value, self.leg_controller.I, self.leg_controller.D]))
        # file.write('\n')
        # file.close()
        # print(error)
        # print(self.leg_controller.value, self.leg_controller.I, self.leg_controller.D)
        ########################################################################################### graphs
        # print(current_angle_control_value)
        # print(current_left_leg_control_value, current_right_leg_control_value)

        if self.active:
            self.angle_control_value = current_angle_control_value
            self.left_leg_control_value = current_left_leg_control_value
            self.right_leg_control_value = current_right_leg_control_value

        return {
            'ik': {
                'left_foot_z_value': self.left_leg_control_value,
                'right_foot_z_value': self.right_leg_control_value,
            },
            'angles': {
                'FootL': self.angle_control_value,
                'FootR': self.angle_control_value
            },
        }

    def check_stability(self):
        # print(round(abs(self.tilt_angles[0]), 1))
        return (round(abs(self.tilt_angles[0]), 1) < 5 and round(np.max([abs(angles[1] - self.tilt_angles[0]) for angles in self.last_tilt_angles]), 1) == 0)

    @property
    def is_finished(self):
        # return abs(self.tilt_angles[0]) > 25 or (round(abs(self.tilt_angles[0]), 1) < 0.2 and round(np.max([abs(angles[1] - self.tilt_angles[0]) for angles in self.last_tilt_angles]), 1) == 0)
        return False