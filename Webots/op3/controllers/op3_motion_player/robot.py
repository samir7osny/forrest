import math
import numpy as np
import controller as webots_controller
import threading

class Robot:
    def __init__(self):

        # self.MotorXSize = 20
        # self.MotorYSize = 40
        # self.MotorZSize = 40.5

        # self.MotorPZAxis = 9
        # self.MotorNZAxis = self.MotorZSize - self.MotorPZAxis
        # self.MotorCenterToAxis = self.MotorZSize / 2 - self.MotorPZAxis

        # self.HipToHip = (67 - 2 * self.MotorCenterToAxis)
        # self.HipToShoulder = (104 - self.MotorCenterToAxis)
        # self.HipToHead = (109 - self.MotorCenterToAxis)
        # self.ShoulderToShoulder = (145 - 2 * (self.MotorYSize/2))
        # self.ShoulderToArm = (30 + self.MotorYSize/2)
        # self.ArmToHand = (74 - 2* self.MotorCenterToAxis)
        # self.HipToLegW = 22
        # self.HipToLegH = 39
        # self.HipToKnee = (94 - self.MotorCenterToAxis)
        # self.LegToKnee = self.HipToKnee - self.HipToLegH
        # self.HipToAnkle = (149 - self.MotorCenterToAxis)
        # self.KneeToAnkle = self.HipToAnkle - self.HipToKnee
        # self.HipToFoot = (197 - self.MotorCenterToAxis)
        # self.AnkleToFoot = self.HipToFoot - self.HipToAnkle
        # self.FootToGround = 15
        # self.HipToGround = self.HipToFoot + self.FootToGround


        self.HipToGround = (0.25465 * 1000)
        self.LegToGround = (0.25465 * 1000)
        self.kneeToGround = (0.144015 * 1000)
        self.AnkleToGround = (0.0340148 * 1000)
        self.FootToGround = (0.0340148 * 1000)

        self.HipToGround = self.HipToGround
        self.LegToKnee = self.LegToGround - self.kneeToGround
        self.KneeToAnkle = self.kneeToGround - self.AnkleToGround
        self.AnkleToFoot = self.AnkleToGround - self.FootToGround
        self.FootToGround = self.FootToGround
        self.HipToLegH = self.HipToGround - self.LegToGround
        self.HipToFoot = self.HipToGround - self.FootToGround

        print(self.HipToGround)
        print(self.LegToKnee)
        print(self.KneeToAnkle)
        print(self.AnkleToFoot)
        print(self.FootToGround)
        print(self.HipToLegH)
        print(self.HipToFoot)

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

        self.robot = webots_controller.Robot()

        self.motors = {}
        for motor_name in motors_names:
            self.motors[motor_name] = self.robot.getMotor(motor_name)


        self.accelerometer = self.robot.getAccelerometer('Accelerometer')
        self.gyro = self.robot.getGyro('Gyro')

        self.accelerometer.enable(1)
        self.gyro.enable(1)

        self.values_file = open('values.txt', 'a+')

    def update(self, left_foot_z_value, left_foot_x_value, right_foot_z_value, right_foot_x_value, pelvis_x_value, pelvis_y_value, left_theta, right_theta, duration = 1000):

        # print('accelerometer', self.accelerometer.getValues())
        # print('gyro', self.gyro.getValues())

        self.values_file.write('accelerometer ' + str(self.accelerometer.getValues()))
        self.values_file.write('\n')
        self.values_file.write('gyro ' + str(self.gyro.getValues()))
        self.values_file.write('\n')

        Angles = {}

        # print('a', self.HipToGround - left_foot_z_value, '   b', -(left_foot_x_value - pelvis_x_value))
        Angles['LegUpperL'], Angles['LegLowerL'], Angles['AnkleL'] = self.inverse_kinematic_xz(self.HipToGround - left_foot_z_value, -(left_foot_x_value - pelvis_x_value), left_theta)
        # Angles['LegUpperL'], Angles['LegLowerL'], Angles['AnkleL'] = -Angles['LegUpperL'], -Angles['LegLowerL'], -Angles['AnkleL']
        Angles['AnkleL'] = -Angles['AnkleL']
        
        # print('a', self.HipToGround - right_foot_z_value, '   b', -(right_foot_x_value - pelvis_x_value))
        Angles['LegUpperR'], Angles['LegLowerR'], Angles['AnkleR'] = self.inverse_kinematic_xz(self.HipToGround - right_foot_z_value, -(right_foot_x_value - pelvis_x_value), right_theta)
        Angles['LegUpperR'], Angles['LegLowerR'] = -Angles['LegUpperR'], -Angles['LegLowerR']

        Angles['PelvL'], Angles['FootL'] = self.inverse_kinematic_y(pelvis_y_value)
        Angles['PelvR'], Angles['FootR'] = Angles['PelvL'], Angles['FootL']

        # print(Angles)

        [self.motors[motor_name].setPosition(math.radians(Angles[motor_name])) for motor_name in Angles]

        self.robot.step(duration)


    def inverse_kinematic_xz(self, a, b, theta):
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

    def inverse_kinematic_y(self, dy):

        Q1 = np.arcsin((dy) / (self.HipToFoot))

        return math.degrees(Q1), math.degrees(Q1)