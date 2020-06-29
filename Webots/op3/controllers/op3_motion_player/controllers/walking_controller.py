from controllers._controller import _controller
import walking_pattern_generator
from walking_pattern_generator import PatternGenerator

class WalkingController(_controller):
    def __init__(self, accuracy=1):
        super().__init__(accuracy)

        pattern_generator = PatternGenerator()

        t, right_foot_height, left_foot_height, pelvis_side_displacement, right_foot_forward_displacement, left_foot_forward_displacement, pelvis_forward_displacement = pattern_generator.generate_full_pattern(number_of_steps=25)

        self.data = {
            't': t,
            'left_foot_z_values': left_foot_height,
            'left_foot_x_values': left_foot_forward_displacement,
            'pelvis_x_values': pelvis_forward_displacement,
            'right_foot_z_values': right_foot_height,
            'right_foot_x_values': right_foot_forward_displacement,
            'pelvis_y_values': pelvis_side_displacement
        }

        # print(len(self.data['t']))
        # print(len(self.data['left_foot_z_values']))
        self.name = 'WalkingController'

    def get_step(self):
        left_foot_z_value = self.data['left_foot_z_values'][self.current_time]
        left_foot_x_value = self.data['left_foot_x_values'][self.current_time]
        pelvis_x_value = self.data['pelvis_x_values'][self.current_time]
        right_foot_z_value = self.data['right_foot_z_values'][self.current_time]
        right_foot_x_value = self.data['right_foot_x_values'][self.current_time]
        pelvis_y_value = self.data['pelvis_y_values'][self.current_time]
        
        self.current_time += self.accuracy
        
        return {
            'ik': {
                'left_foot_z_value': left_foot_z_value,
                'left_foot_x_value': left_foot_x_value,
                'right_foot_z_value': right_foot_z_value,
                'right_foot_x_value': right_foot_x_value,
                'pelvis_x_value': pelvis_x_value,
                'pelvis_y_value': pelvis_y_value
            }
        }

    @property
    def is_finished(self):
        return self.current_time >= len(self.data['t'])