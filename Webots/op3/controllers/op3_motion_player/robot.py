import math
import numpy as np
import controller as webots_controller
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Robot:
    def __init__(self, accuracy=1, real_time_plotting=False):
        
        self.robot = webots_controller.Robot()
        self.real_time_plotting = real_time_plotting
        self.accuracy = accuracy

        self.HipToGround = (0.25465 * 1000)
        self.LegToGround = (0.25465 * 1000)
        self.kneeToGround = (0.144015 * 1000)
        self.AnkleToGround = (0.0340148 * 1000)
        self.FootToGround = (0.0340148 * 1000)

        self.HipToGround = self.HipToGround
        self.HipToLeg = self.HipToGround - self.LegToGround
        self.LegToKnee = self.LegToGround - self.kneeToGround
        self.KneeToAnkle = self.kneeToGround - self.AnkleToGround
        self.AnkleToFoot = self.AnkleToGround - self.FootToGround
        self.FootToGround = self.FootToGround
        self.HipToLegH = self.HipToGround - self.LegToGround
        self.HipToFoot = self.HipToGround - self.FootToGround


        motors_names = [
            "ShoulderR",  # ID1
            "ShoulderL",  # ID2
            "ArmUpperR",  # ID3
            "ArmUpperL",  # ID4
            "ArmLowerR",  # ID5
            "ArmLowerL",  # ID6

            # "PelvYR",  # ID7
            # "PelvYL",  # ID8
            "PelvR",  # ID9
            "PelvL",  # ID10
            "LegUpperR",  # ID11
            "LegUpperL",  # ID12
            "LegLowerR",  # ID13
            "LegLowerL",  # ID14
            "AnkleR",  # ID15
            "AnkleL",  # ID16
            "FootR",  # ID17
            "FootL",  # ID18

            "Neck",  # ID19
            "Head"  # ID20
        ]


        self.gyro_values = [[0], [0], [0]]
        self.accelerometer_values = [[0], [0], [0]]

        if self.real_time_plotting:
            self.time = []

            plt.ion()
            self.gyro_fig = plt.figure()
            self.gyro_ax = self.gyro_fig.add_subplot(111)

            self.accelerometer_fig = plt.figure()
            self.accelerometer_ax = self.accelerometer_fig.add_subplot(111)
            
            plt.draw()
            plt.pause(0.001)

        self.motors = {}
        for motor_name in motors_names:
            self.motors[motor_name] = self.robot.getMotor(motor_name)

        self.accelerometer = self.robot.getAccelerometer('Accelerometer')
        self.gyro = self.robot.getGyro('Gyro')

        self.accelerometer.enable(1)
        self.gyro.enable(1)

        self.current_time = 0

        open('local-values.txt', 'w').close

    def reset(self):
        self.gyro_values = [[0], [0], [0]]
        self.accelerometer_values = [[0], [0], [0]]

        self.current_time = 0

    def flush_graphs(self):
        self.gyro_ax.clear()
        self.accelerometer_ax.clear()

        try:
            self.gyro_ax.plot(self.time, self.gyro_values[0], label='gyro x')
            self.gyro_ax.plot(self.time, self.gyro_values[1], label='gyro y')
            self.gyro_ax.plot(self.time, self.gyro_values[2], label='gyro z')
            self.gyro_ax.legend()

            self.accelerometer_ax.plot(self.time, self.accelerometer_values[0], label='accelerometer x')
            self.accelerometer_ax.plot(self.time, self.accelerometer_values[1], label='accelerometer y')
            self.accelerometer_ax.plot(self.time, self.accelerometer_values[2], label='accelerometer z')
            self.accelerometer_ax.legend()
        except:
            print('error')

        plt.draw()
        plt.pause(0.0001)

    def get_ik_angles(self, ik_values):

        left_foot_z_value = ik_values['left_foot_z_value']
        left_foot_x_value = ik_values['left_foot_x_value']
        right_foot_z_value = ik_values['right_foot_z_value']
        right_foot_x_value = ik_values['right_foot_x_value']
        pelvis_x_value = ik_values['pelvis_x_value']
        pelvis_y_value = ik_values['pelvis_y_value']

        angles = {}

        a = np.sqrt((self.HipToGround - left_foot_z_value) ** 2 - (-(left_foot_x_value - pelvis_x_value)) ** 2)
        angles['LegUpperL'], angles['LegLowerL'], angles['AnkleL'] = self.inverse_kinematic_xz(a, -(left_foot_x_value - pelvis_x_value))
        angles['AnkleL'] = -angles['AnkleL']
        
        a = np.sqrt((self.HipToGround - right_foot_z_value) ** 2 - (-(right_foot_x_value - pelvis_x_value)) ** 2)
        angles['LegUpperR'], angles['LegLowerR'], angles['AnkleR'] = self.inverse_kinematic_xz(a, -(right_foot_x_value - pelvis_x_value))
        angles['LegUpperR'], angles['LegLowerR'] = -angles['LegUpperR'], -angles['LegLowerR']

        a = self.HipToLeg + self.LegToKnee * np.cos(np.radians(angles['LegUpperL'])) + self.KneeToAnkle * np.cos(np.radians(angles['LegLowerL']))  + self.AnkleToFoot * np.cos(np.radians(angles['AnkleL']))
        angles['PelvL'], angles['FootL'] = self.inverse_kinematic_y(pelvis_y_value, a)
        a = self.HipToLeg + self.LegToKnee * np.cos(np.radians(angles['LegUpperR'])) + self.KneeToAnkle * np.cos(np.radians(angles['LegLowerR']))  + self.AnkleToFoot * np.cos(np.radians(angles['AnkleR']))
        angles['PelvR'], angles['FootR'] = self.inverse_kinematic_y(pelvis_y_value, a)
        # angles['PelvR'], angles['FootR'] = angles['PelvL'], angles['FootL']

        return angles

    def apply_angles(self, angles):
        [self.motors[motor_name].setPosition(math.radians(angles[motor_name])) for motor_name in angles]

    def update(self):
        if self.current_time + 1 == len(self.gyro_values[0]): return

        current_gyro_values = self.gyro.getValues()
        current_accelerometer_values = self.accelerometer.getValues()
        
        values_file = open('local-values.txt', 'a')
        values_file.write('gyro ' + str(current_gyro_values))
        values_file.write('\n')
        values_file.write('accelerometer ' + str(current_accelerometer_values))
        values_file.write('\n')
        values_file.close()

        [self.gyro_values[idx].append(current_gyro_values[idx]) for idx in range(3)]
        [self.accelerometer_values[idx].append(current_accelerometer_values[idx]) for idx in range(3)]

    def step(self):
        self.robot.step(self.accuracy)
        self.current_time += 1
        self.update()

    def inverse_kinematic_xz(self, a, b, theta = 0):
        theta = math.radians(theta)
        l1, l2, l3 = self.LegToKnee, self.KneeToAnkle, self.AnkleToFoot + self.FootToGround
        a -= self.HipToLegH
        A1 = a - l3*np.cos(theta)
        B1 = b - l3*np.sin(theta)
        R = np.sqrt(A1**2 + B1**2)
        Alpha = np.arccos(min(1, max(-1, (l1**2 + R**2 - l2**2) / (2*l1*R))))
        Q1 = np.arctan2(B1, A1) - Alpha
        Q2 = np.arctan2((R*np.sin(Alpha)), (R*np.cos(Alpha) - l1))
        Q3 = theta - Q1 - Q2

        return math.degrees(Q1), math.degrees(Q2), math.degrees(Q3)

    def inverse_kinematic_y(self, dy, a):
        Q1 = np.arcsin((dy) / a)

        return math.degrees(Q1), math.degrees(Q1)

    def get_sensors(self):
        return {
            'gyro': np.array([self.gyro_values[0][-1], self.gyro_values[1][-1], self.gyro_values[2][-1]]),
            'accelerometer': np.array([self.accelerometer_values[0][-1], self.accelerometer_values[1][-1], self.accelerometer_values[2][-1]]),
        }