from controllers._controller import _controller
import walking_pattern_generator

class WalkingController(_controller):
    def __init__(self, accuracy=1):
        super().__init__(accuracy)

        self.data = walking_pattern_generator.get_pattern()

    def get_step(self, sensors):
        left_foot_z_value = self.data['left_foot_z_values'][self.current_time]
        left_foot_x_value = self.data['left_foot_x_values'][self.current_time]
        left_theta = self.data['left_theta_values'][self.current_time]
        pelvis_x_value = self.data['pelvis_x_values'][self.current_time]
        right_foot_z_value = self.data['right_foot_z_values'][self.current_time]
        right_foot_x_value = self.data['right_foot_x_values'][self.current_time]
        right_theta = self.data['right_theta_values'][self.current_time]
        pelvis_y_value = self.data['pelvis_y_values'][self.current_time]
        
        self.current_time += self.accuracy
        
        return {
            'ik': {
                'left_foot_z_value': left_foot_z_value,
                'left_foot_x_value': left_foot_x_value,
                'right_foot_z_value': right_foot_z_value,
                'right_foot_x_value': right_foot_x_value,
                'pelvis_x_value': pelvis_x_value,
                'pelvis_y_value': pelvis_y_value,
                'left_theta': left_theta,
                'right_theta': right_theta
            }
        }

    @property
    def is_finished(self):
        return self.current_time >= len(self.data['t'])