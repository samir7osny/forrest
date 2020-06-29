from controllers._controller import _controller

class BaseController(_controller):
    def __init__(self, accuracy=1):
        super().__init__(accuracy)

        self.name = 'BaseController'

    def get_step(self):
        # self.current_time += self.accuracy
        
        return {
            'ik': {
                'left_foot_z_value': 10,
                'left_foot_x_value': 0,
                'right_foot_z_value': 10,
                'right_foot_x_value': 0,
                'pelvis_x_value': 0,
                'pelvis_y_value': 0
            }
        }

    @property
    def is_finished(self):
        return False