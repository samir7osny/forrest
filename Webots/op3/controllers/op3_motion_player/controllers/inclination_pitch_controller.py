from controllers._controller import _controller
from utils.pid_controller import PID
import numpy as np

class InclinationPitchController(_controller):
    def __init__(self, accuracy=1):
        super().__init__(accuracy)

        self.angle_controller = PID(Kp=1, Ki=7, Kd=0.8, guard=(-60, 60))
        self.control_value = 0
        self.name = 'InclinationPitchController'

    def get_step(self):

        error = np.degrees(self.robot.tilt)[1]

        current_control_value = self.angle_controller(error)

        if self.active: self.control_value = current_control_value

        return {
            'angles': {
                'AnkleL': -self.control_value,
                'AnkleR': self.control_value
            }
        }

    def check_stability(self):
        return (round(abs(self.robot.tilt[1]), 1) < 2)

    @property
    def is_finished(self):
        return True