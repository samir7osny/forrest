from controllers._controller import _controller
from utils.pid_controller import PID
import numpy as np

class LandingMomentumController(_controller):
    def __init__(self, accuracy=1):
        super().__init__(accuracy)

        self.foot_forces = {
            'RFR': [0, 0, 0],
            'RFL': [0, 0, 0],
            'RBR': [0, 0, 0],
            'RBL': [0, 0, 0],
            'LFR': [0, 0, 0],
            'LFL': [0, 0, 0],
            'LBR': [0, 0, 0],
            'LBL': [0, 0, 0],
        }
        self.left_foot_x_controller = PID(Kp=0.0000001, Ki=0.0000007, Kd=0.00000008, guard=(-60, 60))
        self.left_foot_y_controller = PID(Kp=0.0000001, Ki=0.0000007, Kd=0.00000008, guard=(-60, 60))
        self.right_foot_x_controller = PID(Kp=0.0000001, Ki=0.0000007, Kd=0.00000008, guard=(-60, 60))
        self.right_foot_y_controller = PID(Kp=0.0000001, Ki=0.0000007, Kd=0.00000008, guard=(-60, 60))
        self.left_x_control_value = 0
        self.right_t_control_value = 0
        self.left_y_control_value = 0
        self.right_t_control_value = 0
        self.name = 'LandingMomentumController'

    def update(self, sensors):
        self.foot_forces = sensors['touch_sensor']

    def get_step(self):
        
        left_x_error = ((self.foot_forces['LFR'][0] - self.foot_forces['LBR'][0]) + (self.foot_forces['LFL'][0] - self.foot_forces['LBL'][0])) / 2
        right_x_error = ((self.foot_forces['RFR'][0] - self.foot_forces['RBR'][0]) + (self.foot_forces['RFL'][0] - self.foot_forces['RBL'][0])) / 2
        
        left_y_error = ((self.foot_forces['LFR'][0] - self.foot_forces['LFL'][0]) + (self.foot_forces['LBR'][0] - self.foot_forces['LBL'][0])) / 2
        right_y_error = ((self.foot_forces['RFR'][0] - self.foot_forces['RFL'][0]) + (self.foot_forces['RBR'][0] - self.foot_forces['RBL'][0])) / 2

        left_x_current_control_value = self.left_foot_x_controller(left_x_error)
        right_x_current_control_value = self.right_foot_x_controller(right_x_error)
        left_y_current_control_value = self.left_foot_y_controller(left_y_error)
        right_y_current_control_value = self.right_foot_y_controller(right_y_error)

        if self.active:
            self.left_x_control_value = left_x_current_control_value
            self.right_x_control_value = right_x_current_control_value
            self.left_y_control_value = left_y_current_control_value
            self.right_y_control_value = right_y_current_control_value

        return {
            'angles': {
                'AnkleL': self.left_y_control_value,
                'AnkleR': self.right_y_control_value,
                'FootL': -self.left_x_control_value,
                'FootR': self.right_x_control_value,
            }
        }

    def check_stability(self):
        return True

    @property
    def is_finished(self):
        return False