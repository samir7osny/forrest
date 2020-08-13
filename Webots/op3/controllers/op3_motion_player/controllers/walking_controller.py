from controllers._controller import _controller
import walking_pattern_generator
from walking_pattern_generator import PatternGenerator
from controllers.path_controller import PathController
import numpy as np
import matplotlib.pyplot as plt

class WalkingController(_controller):
    def __init__(self, accuracy=1, path=None):
        super().__init__(accuracy)

        path = path if path is not None else {'path_str': 'M 300 100 C 100 100 200 200 200 300 L 250 350 L 220 300', 'width': 500, 'height': 500}

        self.pattern_generator = PatternGenerator()

        self.data = {
            't': [],
            'left_foot_z_values': [],
            'left_foot_x_values': [],
            'foot_rotation': [],
            'pelvis_x_values': [],
            'right_foot_z_values': [],
            'right_foot_x_values': [],
            'pelvis_y_values': [],
            'right_yaw': [],
            'left_yaw': [],
        }
        self.name = 'WalkingController'

        self.step_right = True
        self.stoping = False

        self.right_last_yaw = 0
        self.left_last_yaw = 0
        self.yaw_angle = 0
        self.last_d = None

        self.path_controller = PathController(path_str=path['path_str'], width=path['width'], height=path['height'])

    def accumulate(self, arr1, arr2):
        offset = arr1[-1] - arr2[0] if len(arr1) > 0 else 0
        # arr1 = np.array(arr1) - (arr1[0] if len(arr1) > 0 else 0)
        return list(arr1) + list(np.array(arr2) + offset)

    def fix_forward_values(self, right_foot_forward_displacement, left_foot_forward_displacement, pelvis_forward_displacement):
        # if len(self.data['t']) > 0: print(round(self.data['left_foot_x_values'][-1] - self.data['right_foot_x_values'][-1]))
        # if len(self.data['t']) == 0 or round(self.data['left_foot_x_values'][-1] - self.data['right_foot_x_values'][-1]) == 0:
        #     return np.clip(right_foot_forward_displacement, 0, None), np.clip(left_foot_forward_displacement, 0, None), np.clip(pelvis_forward_displacement, 0, None)
        # else: return right_foot_forward_displacement, left_foot_forward_displacement, pelvis_forward_displacement

        return np.clip(right_foot_forward_displacement, 0, None), np.clip(left_foot_forward_displacement, 0, None), np.clip(pelvis_forward_displacement, 0, None)


    def get_step(self, d=None, draw=False):
        # if d is None: d = self.pattern_generator.d
        if self.stoping: d=self.last_d
        if self.current_time >= len(self.data['t']):
            angle_to_be = 0
            if self.step_right: 
                self.right_last_yaw = -self.yaw_angle
                angle_to_be = -self.right_last_yaw
                self.left_last_yaw = 0
            else:
                self.left_last_yaw = -self.yaw_angle
                angle_to_be = -self.left_last_yaw
                self.right_last_yaw = 0
            self.yaw_angle, d = self.path_controller.get_step(angle_to_be)
            d *= 10
            self.yaw_angle /= 2
            # print(self.yaw_angle, d)
            
            self.last_d = self.last_d if self.last_d is not None else d
            # self.yaw_angle = 0
            self.step_right = not self.step_right
            t, right_foot_height, left_foot_height, right_foot_rotation, left_foot_rotation,pelvis_side_displacement, right_foot_forward_displacement, left_foot_forward_displacement, pelvis_forward_displacement = self.pattern_generator.get_step(self.step_right, self.stoping, last_d=self.last_d, d=d)

            self.data['t'] = self.accumulate(self.data['t'], t)
            self.data['left_foot_z_values'] += list(left_foot_height)
            self.data['left_foot_x_values'] = self.accumulate(self.data['left_foot_x_values'], left_foot_forward_displacement)
            self.data['pelvis_x_values'] = self.accumulate(self.data['pelvis_x_values'], pelvis_forward_displacement)
            self.data['right_foot_z_values'] += list(right_foot_height)
            self.data['right_foot_x_values'] = self.accumulate(self.data['right_foot_x_values'], right_foot_forward_displacement)
            self.data['pelvis_y_values'] = self.accumulate(self.data['pelvis_y_values'], pelvis_side_displacement)
            self.data['right_yaw'] += list(right_foot_rotation)
            self.data['left_yaw'] += list(left_foot_rotation)

            self.data['right_foot_x_values'], self.data['left_foot_x_values'], self.data['pelvis_x_values'] = self.fix_forward_values(self.data['right_foot_x_values'], self.data['left_foot_x_values'], self.data['pelvis_x_values'])
            
            self.last_d = d

            pattern = [self.data['t'],
                        self.data['right_foot_z_values'], 
                        self.data['left_foot_z_values'],
                        self.data['right_yaw'],
                        self.data['left_yaw'],
                        self.data['pelvis_y_values'],
                        self.data['right_foot_x_values'],
                        self.data['left_foot_x_values'],
                        self.data['pelvis_x_values']]


            if draw:
                fig = plt.figure()
                ax = fig.add_subplot(1, 1, 1)

                max_of_first_3 = np.max([np.max(np.abs(pattern[idx])) for idx in range(1, 5)])
                max_of_second_3 = np.max([np.max(np.abs(pattern[idx])) for idx in range(5, 8)])
                divider = max_of_second_3 / max_of_first_3
                divider = 1
                
                labels = ['right_foot_height', 'left_foot_height','right_foot_rotation', 'left_foot_rotation', 'pelvis_side_displacement', 'right_foot_forward_displacement', 'left_foot_forward_displacement', 'pelvis_forward_displacement']
                [plt.plot(pattern[0], pattern[idx], label=labels[idx - 1]) if idx < 6 else plt.plot(pattern[0], np.array(pattern[idx]) / divider, label=labels[idx - 1]) for idx in range(1, len(pattern))]

                plt.legend()

                start, end = ax.get_xlim()
                x_ticks = np.arange(0, end + 1, int(np.ceil(self.pattern_generator.Tstride / 2)))
                start, end = ax.get_ylim()
                y_ticks = np.arange(0, end + 1, self.pattern_generator.d / divider)
                ax.set_xticks(x_ticks)
                ax.set_yticks(y_ticks)

                ax.grid()
                plt.show()


        if draw: return 0

        left_foot_z_value = self.data['left_foot_z_values'][self.current_time]
        left_foot_x_value = self.data['left_foot_x_values'][self.current_time]
        pelvis_x_value = self.data['pelvis_x_values'][self.current_time]
        right_foot_z_value = self.data['right_foot_z_values'][self.current_time]
        right_foot_x_value = self.data['right_foot_x_values'][self.current_time]
        pelvis_y_value = self.data['pelvis_y_values'][self.current_time]
        right_yaw = self.data['right_yaw'][self.current_time]
        left_yaw = self.data['left_yaw'][self.current_time]
        
        self.current_time += self.accuracy
        # print(f':::::::::::::::::::: {-self.yaw_angle * right_yaw if self.step_right else self.right_last_yaw * right_yaw} {-self.yaw_angle * left_yaw if not self.step_right else self.left_last_yaw * left_yaw}')
        
        return {
            'ik': {
                'left_foot_z_value': left_foot_z_value,
                'left_foot_x_value': left_foot_x_value,
                'right_foot_z_value': right_foot_z_value,
                'right_foot_x_value': right_foot_x_value,
                'pelvis_x_value': pelvis_x_value,
                'pelvis_y_value': pelvis_y_value
            },
            'angles': {
                'PelvYR': -self.yaw_angle * right_yaw if self.step_right else self.right_last_yaw * right_yaw,
                'PelvYL': -self.yaw_angle * left_yaw if not self.step_right else self.left_last_yaw * left_yaw,
            }
        }

    def attach(self, robot):
        super().attach(robot)
        self.path_controller.robot = robot
    
    def flush_buffer(self):
        data = self.buffer + self.path_controller.flush_buffer()
        self.buffer = []
        return data

    @property
    def is_finished(self):
        return self.path_controller.is_finished