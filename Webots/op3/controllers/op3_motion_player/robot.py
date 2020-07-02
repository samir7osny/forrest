import math
import numpy as np
import controller as webots_controller
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pickle
from pytransform3d.rotations import *

class Robot:
    def __init__(self, accuracy=1, real_time_plotting=False):
        
        self.robot = webots_controller.Supervisor()
        

        if self.robot.getSupervisor():
            self.supervised = True
            self.robot_node = self.robot.getFromDef("OP3")
            # self.trans_field = self.robot_node.getField("translation")
        else:
            self.supervised = False
        
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

            "PelvYR",  # ID7
            "PelvYL",  # ID8
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

        self.reset()

        self.motors = {}
        for motor_name in motors_names:
            self.motors[motor_name] = self.robot.getMotor(motor_name)

        self.accelerometer = self.robot.getAccelerometer('Accelerometer')
        self.gyro = self.robot.getGyro('Gyro')

        self.accelerometer.enable(1)
        self.gyro.enable(1)

        self.current_time = 0

        open('local-values.txt', 'w').close()

    def reset(self):
        self.gyro_values = []
        self.accelerometer_values = []
        
        self.corrected_accelerometer_values = []

        self.tilt_angles = []
        self.velocities = []
        self.positions = []

        self.current_time = 0

        if self.supervised:
            self.actual_position = [np.array(self.robot_node.getPosition())]
            mat = self.robot_node.getOrientation()
            mat = np.reshape(mat, (3, 3))
            or_x = np.arctan2(mat[2, 1], mat[2, 2])
            or_y = np.arctan2(-mat[2, 0], np.sqrt(mat[2, 1]**2 + mat[2, 2]**2))
            or_z = np.arctan2(mat[1, 0], mat[0, 0])
            self.orientation = [np.array([or_x, or_y, or_z])]
            # self.actual_velocities = [np.array(self.robot_node.getVelocity())]
            self.actual_velocities = []

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

    # def logger(self, current_gyro_values, current_accelerometer_values):
    #     values_file = open('local-values.txt', 'a')
    #     values_file.write('gyro ' + str(current_gyro_values))
    #     values_file.write('\n')
    #     values_file.write('accelerometer ' + str(current_accelerometer_values))
    #     values_file.write('\n')
    #     values_file.close()

    def accelerometer_corrector(self, tilt_angles, accelerometer_values):
        
        factor = np.array([-1, -1, -1])
        # factor = np.array([1, 1, 1])
        # factor = np.array([0, 0, 0])
        angles = tilt_angles * factor
        # rot_matrix_x = np.array(
        #     [
        #         [1, 0, 0],
        #         [0, np.cos(angles[0]), -np.sin(angles[0])],
        #         [0, np.sin(angles[0]), np.cos(angles[0])],
        #     ]
        # )
        # rot_matrix_y = np.array(
        #     [
        #         [np.cos(angles[1]), 0, np.sin(angles[1])],
        #         [0, 1, 0],
        #         [-np.sin(angles[1]), 0, np.cos(angles[1])],
        #     ]
        # )
        # rot_matrix_z = np.array(
        #     [
        #         [np.cos(angles[2]), -np.sin(angles[2]), 0],
        #         [np.sin(angles[2]), np.cos(angles[2]), 0],
        #         [0, 0, 1],
        #     ]
        # )
        # rot_mat = rot_matrix_x
        # rot_mat = np.matmul(rot_matrix_y, rot_mat)
        # rot_mat = np.matmul(rot_matrix_z, rot_mat)
        
        rot_mat = matrix_from_euler_xyz(angles)
        accelerometer_values = np.matmul(rot_mat, accelerometer_values)

        accelerometer_values -= np.array([5.00201980e-04, -4.10223144e-06, 9.81])

        return accelerometer_values

    def supervised_update(self):
        self.actual_position.append(np.array(self.robot_node.getPosition()) - self.actual_position[0])
        
        mat = self.robot_node.getOrientation()
        mat = np.reshape(mat, (3, 3))
        or_x = np.arctan2(mat[2, 1], mat[2, 2])
        or_y = np.arctan2(-mat[2, 0], np.sqrt(mat[2, 1]**2 + mat[2, 2]**2))
        or_z = np.arctan2(mat[1, 0], mat[0, 0])
        self.orientation.append(np.array([or_x, or_y, or_z]) - self.orientation[0])

        self.actual_velocities.append(np.array(self.robot_node.getVelocity()))

    def update(self):
        # already updated
        if self.current_time + 1 == len(self.gyro_values): return

        # new values
        current_gyro_values = self.gyro.getValues()
        current_accelerometer_values = self.accelerometer.getValues()
        # current_accelerometer_values = -np.array(current_accelerometer_values)

        # if self.current_time < 1000: print(current_gyro_values)
        # self.logger(current_gyro_values, current_accelerometer_values)

        self.gyro_values.append(current_gyro_values)
        self.accelerometer_values.append(current_accelerometer_values)
        
        # convert to useful info
        current_tilt_angles = (self.tilt_angles[-1] if len(self.tilt_angles) > 0 else np.array([0, 0, 0])) + (1 / 1000) * np.array(current_gyro_values)
        self.tilt_angles.append(current_tilt_angles)

        current_accelerometer_values = self.accelerometer_corrector(current_tilt_angles, current_accelerometer_values)

        self.corrected_accelerometer_values.append(current_accelerometer_values)

        # delta = (1 / 1000) * (((self.corrected_accelerometer_values[max(0, len(self.corrected_accelerometer_values) - 2)]) + current_accelerometer_values) / 2)
        delta = (1 / 1000) * current_accelerometer_values
        current_velocities = (self.velocities[-1] if len(self.velocities) > 0 else np.array([0, 0, 0])) + delta
        self.velocities.append(current_velocities)

        current_position = (self.positions[-1] if len(self.positions) > 0 else np.array([0, 0, 0])) + (1 / 1000) * current_velocities
        self.positions.append(current_position)

        if self.supervised:
            self.supervised_update()

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
            'gyro': self.gyro_values[-1],
            'accelerometer': self.accelerometer_values[-1]
        }

    @property
    def tilt(self):
        return self.tilt_angles[-1] if len(self.tilt_angles) > 0 else np.array([0, 0, 0])

    @property
    def position(self):
        return self.positions[-1] if len(self.positions) > 0 else np.array([0, 0, 0])

    def save_data(self):

        data = {
            'gyro_values': self.gyro_values,
            'accelerometer_values': self.accelerometer_values,
            'tilt_angles': self.tilt_angles,
            'velocities': self.velocities,
            'positions': self.positions,
            'corrected_accelerometer_values': self.corrected_accelerometer_values
        }

        if self.supervised: 
            data['actual_position'] = self.actual_position
            data['orientation'] = self.orientation
            data['actual_velocities'] = self.actual_velocities
        
        with open('local-values.pickle', 'wb') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)