import numpy as np
import matplotlib.pyplot as plt
import pickle
from pytransform3d.rotations import *

file = open('local-values.pickle', 'rb')

data = pickle.load(file)


# 5.68132559e-03 4.45849117e-05 9.81019745e+00

def accelerometer_corrector(tilt_angles, accelerometer_values):
        
        factor = np.array([-1, -1, -1])
        angles = tilt_angles * factor
        rot_mat = matrix_from_euler_xyz(angles)
        accelerometer_values = np.matmul(rot_mat, accelerometer_values)
        acc_offset = np.array([0, 0, 9.81])
        accelerometer_values -= acc_offset
        # print(accelerometer_values, acc_offset)

        return accelerometer_values

corrected_accelerometer_values = []
accelerometer_values = data['accelerometer_values'][1:]
last_values = np.array([0, 0, 0])
velocities = []
for t, _values in enumerate(accelerometer_values):
    _values = accelerometer_corrector(data['tilt_angles'][t], _values)
    corrected_accelerometer_values.append(_values)
    current_values = last_values + _values * (1 / 1000)
    velocities.append(current_values)
    last_values = current_values

last_values = np.array([-0.01187519, 0, -9.80999959e-03])
# last_values = np.array([0, 0, 0])
positions = []
for t, _values in enumerate(velocities):
    current_values = last_values + _values * (1 / 1000)
    positions.append(current_values)
    last_values = current_values

x_acc = [values[0] for values in accelerometer_values]
y_acc = [values[1] for values in accelerometer_values]
z_acc = [values[2] for values in accelerometer_values]

x_corrected_acc = [values[0] for values in corrected_accelerometer_values]
y_corrected_acc = [values[1] for values in corrected_accelerometer_values]
z_corrected_acc = [values[2] for values in corrected_accelerometer_values]

x_velocities = [values[0] for values in velocities]
y_velocities = [values[1] for values in velocities]
z_velocities = [values[2] for values in velocities]

x_positions = [values[0] for values in positions]
y_positions = [values[1] for values in positions]
z_positions = [values[2] for values in positions]

msecs = list(range(0, len(accelerometer_values), 1))

figure = plt.figure(1)
plt.plot(msecs, x_acc, label='x')
plt.plot(msecs, y_acc, label='y')
plt.plot(msecs, z_acc, label='z')
plt.legend()
plt.grid()
figure.show()

msecs = list(range(0, len(corrected_accelerometer_values), 1))
figure = plt.figure(2)
plt.plot(msecs, x_corrected_acc, label='x')
plt.plot(msecs, y_corrected_acc, label='y')
plt.plot(msecs, z_corrected_acc, label='z')
plt.legend()
plt.grid()
figure.show()

figure = plt.figure(3)
plt.plot(msecs, x_velocities, label='x velocities')
plt.plot(msecs, y_velocities, label='y velocities')
plt.plot(msecs, z_velocities, label='z velocities')
plt.legend()
plt.grid()
figure.show()

figure = plt.figure(4)
plt.plot(msecs, x_positions, label='x positions')
plt.plot(msecs, y_positions, label='y positions')
plt.plot(msecs, z_positions, label='z positions')
plt.legend()
plt.grid()
figure.show()

plt.show()