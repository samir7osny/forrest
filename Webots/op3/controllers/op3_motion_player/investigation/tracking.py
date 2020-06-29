import numpy as np
import matplotlib.pyplot as plt

# file = open('local-values-1.txt', 'r')
file = open('local-values-straight.txt', 'r')
# file = open('local-values-nothing-2.txt', 'r')

filelines = file.readlines()

_from = 0
_to = -1

gyro_lines = [line for line in filelines if 'gyro' in line]
gyro_values = np.array([np.array(eval(line[len('gyro '): ])) if 'nan' not in line else np.array([0, 0, 0]) for line in gyro_lines])
angles_values = []
gyro_values = gyro_values[_from: _to]
for t, _values in enumerate(gyro_values):
    delta = (1 / 1000) * ((_values + gyro_values[max(t - 1, 0)]) / 2)
    current_values = (angles_values[-1] if len(angles_values) > 0 else np.array([0, 0, 0])) + (1 / 1000) * _values

    # # prev_last = (gyro_values[max(0, t - 1)] / 2)

    # current_values = (1 / 1000) * ((gyro_values[0] / 2) + np.sum(gyro_values[1: t], axis=0) + (gyro_values[t] / 2))
    angles_values.append(current_values)

accelerometer_lines = [line for line in filelines if 'accelerometer' in line]
accelerometer_values = np.array([np.array(eval(line[len('accelerometer '): ])) if 'nan' not in line else np.array([0, 0, 0]) for line in accelerometer_lines])
velocity_values = []
displacement_values = []
accelerometer_values = accelerometer_values[_from: _to]
corrected_acc_values = []
for t, _values in enumerate(accelerometer_values):

    factors = np.array([-1, -1, -1])
    factors = np.array([1, 1, 1])
    # factors = np.array([0, 0, 0])
    angles = (angles_values[t] * factors)
    # angles = np.radians(angles_values[t] * np.array([-1, -1, 1]))

    rot_matrix_x = np.array(
        [
            [1, 0, 0],
            [0, np.cos(angles[0]), -np.sin(angles[0])],
            [0, np.sin(angles[0]), np.cos(angles[0])],
        ]
    )
    rot_matrix_y = np.array(
        [
            [np.cos(angles[1]), 0, np.sin(angles[1])],
            [0, 1, 0],
            [-np.sin(angles[1]), 0, np.cos(angles[1])],
        ]
    )
    rot_matrix_z = np.array(
        [
            [np.cos(angles[2]), -np.sin(angles[2]), 0],
            [np.sin(angles[2]), np.cos(angles[2]), 0],
            [0, 0, 1],
        ]
    )
    rot_mat = rot_matrix_x
    rot_mat = np.matmul(rot_matrix_y, rot_mat)
    rot_mat = np.matmul(rot_matrix_z, rot_mat)
    
    _values = np.matmul(rot_mat, _values)

    # if np.sum(angles_values[t]) > 10: print(_values)
    # print(_values)
    if t == 1000: print(_values)
    _values -= np.array([0, 0, 9.81])
    if t == 1000: print(_values)
    # _values = np.round(_values, 3)
    # _values = np.round(_values, 2)
    # print(_values)
    # print('\n')
    corrected_acc_values.append(_values)


    delta = (1 / 1000) * ((_values + corrected_acc_values[max(t - 1, 0)]) / 2)
    velocity_current_values = (velocity_values[-1] if len(velocity_values) > 0 else np.array([0, 0, 0])) + (1 / 1000) * _values
    # velocity_current_values = np.round(velocity_current_values, 4)
    velocity_values.append(velocity_current_values)
    
    delta = (1 / 1000) * ((velocity_current_values + velocity_values[max(t - 1, 0)]) / 2)
    current_values = (displacement_values[-1] if len(displacement_values) > 0 else np.array([0, 0, 0])) + (1 / 1000) * velocity_current_values
    # current_values = np.round(current_values, 2)
    displacement_values.append(current_values)
# print('dfvdfv', np.mean(corrected_acc_values[5290: 5520]))
positions = displacement_values

msecs = list(range(0, len(velocity_values), 1))

figure_num = 1

figure = plt.figure(figure_num)
figure_num += 1
x_acc = [values[0] for values in accelerometer_values]
y_acc = [values[1] for values in accelerometer_values]
z_acc = [values[2] for values in accelerometer_values]
plt.plot(msecs, x_acc, label='x acc')
plt.plot(msecs, y_acc, label='y acc')
plt.plot(msecs, z_acc, label='z acc')
plt.legend()
plt.grid()
figure.show()

figure = plt.figure(figure_num)
figure_num += 1
x_acc = [values[0] for values in corrected_acc_values]
y_acc = [values[1] for values in corrected_acc_values]
z_acc = [values[2] for values in corrected_acc_values]
plt.plot(msecs, x_acc, label='x acc corrected')
plt.plot(msecs, y_acc, label='y acc corrected')
plt.plot(msecs, z_acc, label='z acc corrected')
plt.legend()
print(corrected_acc_values[4000] if len(corrected_acc_values) > 4000 else -1)
plt.grid()
figure.show()

figure = plt.figure(figure_num)
figure_num += 1
x_velocity = [values[0] for values in velocity_values]
y_velocity = [values[1] for values in velocity_values]
z_velocity = [values[2] for values in velocity_values]
plt.plot(msecs, x_velocity, label='x velocity')
plt.plot(msecs, y_velocity, label='y velocity')
plt.plot(msecs, z_velocity, label='z velocity')
plt.legend()
plt.grid()
figure.show()

figure = plt.figure(figure_num)
figure_num += 1
x_angle = [values[0] for values in angles_values]
y_angle = [values[1] for values in angles_values]
z_angle = [values[2] for values in angles_values]
plt.plot(msecs, x_angle, label='x angle')
plt.plot(msecs, y_angle, label='y angle')
plt.plot(msecs, z_angle, label='z angle')
plt.legend()
plt.grid()
figure.show()

figure = plt.figure(figure_num)
figure_num += 1
x_position = [values[0] for values in positions]
y_position = [values[1] for values in positions]
z_position = [values[2] for values in positions]
plt.plot(msecs, x_position, label='x position')
plt.plot(msecs, y_position, label='y position')
plt.plot(msecs, z_position, label='z position')
plt.legend()
plt.grid()
figure.show()

figure = plt.figure(figure_num)
figure_num += 1
points_x = [positions[idx][0] for idx in range(len(positions))]
points_y = [positions[idx][1] for idx in range(len(positions))]
print(points_y[-1])
# print(positions)
plt.scatter(points_x, points_y, s=1)
# plt.legend()
plt.axis('equal')
plt.show()