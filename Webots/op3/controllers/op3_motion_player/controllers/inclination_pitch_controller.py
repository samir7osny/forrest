from controllers._controller import _controller
from utils.pid_controller import PID
import numpy as np

class InclinationPitchController(_controller):
    def __init__(self, accuracy=1):
        super().__init__(accuracy)

        self.tilt_angles = np.array([0, 0, 0])
        self.last_tilt_angles = []
        self.angle_controller = PID(Kp=1, Ki=7, Kd=0.8, guard=(-60, 60))
        self.control_value = 0
        self.name = 'InclinationPitchController'

    def update(self, sensors):
        self.last_tilt_angles.append(self.tilt_angles)
        if len(self.last_tilt_angles) > 10: self.last_tilt_angles.pop(0)
        
        self.tilt_angles = self.tilt_angles + np.degrees(np.array([sensors['gyro'][0], sensors['gyro'][1], sensors['gyro'][2]]) * (self.accuracy / 1000))

    def get_step(self):

        error = self.tilt_angles[1]

        current_control_value = self.angle_controller(error)

        if self.active: self.control_value = current_control_value

        return {
            'angles': {
                'AnkleL': -self.control_value,
                'AnkleR': self.control_value
            }
        }

    def check_stability(self):
        # print(round(abs(self.tilt_angles[1]), 1))
        return (round(abs(self.tilt_angles[1]), 1) < 2 and round(np.max([abs(angles[1] - self.tilt_angles[1]) for angles in self.last_tilt_angles]), 1) == 0)

    @property
    def is_finished(self):
        # return abs(self.tilt_angles[1]) > 25 or (round(abs(self.tilt_angles[1]), 1) < 0.2 and round(np.max([abs(angles[1] - self.tilt_angles[1]) for angles in self.last_tilt_angles]), 1) == 0)
        return False