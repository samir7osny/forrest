import numpy as np
import matplotlib.pyplot as plt

file = open('local-values-1.txt', 'r')

gyro_lines = [line for line in file.readlines() if 'gyro' in line]

gyro_values = [np.array(eval(line[len('gyro '): ])) if 'nan' not in line else np.array([0, 0, 0]) for line in gyro_lines]

last_values = np.array([0, 0, 0])
values = []
for t, _values in enumerate(gyro_values):
    current_values = last_values + np.degrees(_values * (1 / 1000))
    values.append(current_values)
    last_values = current_values

print(gyro_values[0: 2])
print(values[0: 2])
print(np.max(values))
print(len(values))

x_velocity = [values[0] for values in gyro_values]
y_velocity = [values[1] for values in gyro_values]
z_velocity = [values[2] for values in gyro_values]

x_values = [values[0] for values in values]
y_values = [values[1] for values in values]
z_values = [values[2] for values in values]

msecs = list(range(0, len(x_velocity), 1))

figure = plt.figure(1)
plt.plot(msecs, x_velocity, label='x')
plt.plot(msecs, y_velocity, label='y')
plt.plot(msecs, z_velocity, label='z')
plt.legend()
figure.show()

figure = plt.figure(2)
plt.plot(msecs, x_values, label='x values')
plt.plot(msecs, y_values, label='y values')
plt.plot(msecs, z_values, label='z values')
plt.legend()
figure.show()

plt.show()