from controllers._controller import _controller
import numpy as np

class BalanceController(_controller):
    def __init__(self, accuracy=1):
        super().__init__(accuracy)

        self.tilt_angles = np.array([0, 0, 0])

    def get_step(self, sensors):
        
        self.tilt_angles = self.tilt_angles + np.degrees(np.array([sensors['gyro'][0], sensors['gyro'][1], sensors['gyro'][2]]) * (self.accuracy / 1000))

        return {
            'angles': {
                'AnkleL': -self.tilt_angles[1],
                'AnkleR': self.tilt_angles[1]
            }
        }

    @property
    def is_finished(self):
        return False