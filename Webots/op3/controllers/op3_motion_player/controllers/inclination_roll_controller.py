from controllers._controller import _controller
from utils.pid_controller import PID
import numpy as np
import copy

class InclinationRollController(_controller):
    def __init__(self, accuracy=1):
        super().__init__(accuracy)

        self.angle_controller = PID(Kp=1.5, Ki=2, Kd=0.8, guard=(-60, 60))
        self.leg_controller = PID(Kp=1, Ki=2, Kd=1.2, guard=(-20, 20))
        self.angle_control_value = 0
        self.left_leg_control_value = 0
        self.right_leg_control_value = 0
        self.name = 'InclinationRollController'

    def get_step(self):

        error = np.degrees(self.robot.tilt)[0]

        current_angle_control_value = self.angle_controller(error)
        current_left_leg_control_value = self.leg_controller(error)
        current_right_leg_control_value = -current_left_leg_control_value

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
        return (round(abs(self.robot.tilt[0]), 1) < 5)

    @property
    def is_finished(self):
        return True