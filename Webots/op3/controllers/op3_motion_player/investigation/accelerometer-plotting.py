import numpy as np
import matplotlib.pyplot as plt

file = open('local-values-1.txt', 'r')

accelerometer_lines = [line for line in file.readlines() if 'accelerometer' in line]

accelerometer_values = [np.array(eval(line[len('accelerometer '): ])) if 'nan' not in line else np.array([0, 0, 0]) for line in accelerometer_lines]
last_values = np.array([0, 0, 0])
values = []
for t, _values in enumerate(accelerometer_values):
    current_values = last_values + _values * (1 / 1000)
    # current_values = np.degrees(np.array([np.arctan2(values[0], np.sqrt(values[1]**2 + values[2]**2)),
    #                             np.arctan2(values[1], np.sqrt(values[0]**2 + values[2]**2)),
    #                             np.arctan2(values[2], np.sqrt(values[0]**2 + values[1]**2))
    #                 ]))
    # current_values[0] = 90 - current_values[0]
    values.append(current_values)
    last_values = current_values

print(accelerometer_values[0: 2])
print(values[0: 2])
print(np.max(values))
print(len(values))

x_acc = [values[0] for values in accelerometer_values]
y_acc = [values[1] for values in accelerometer_values]
z_acc = [values[2] for values in accelerometer_values]

x_values = [values[0] for values in values]
y_values = [values[1] for values in values]
z_values = [values[2] for values in values]

msecs = list(range(0, 10000, 1))

figure = plt.figure(1)
plt.plot(msecs, x_acc, label='x')
plt.plot(msecs, y_acc, label='y')
plt.plot(msecs, z_acc, label='z')
plt.legend()
figure.show()

figure = plt.figure(2)
plt.plot(msecs, x_values, label='x values')
plt.plot(msecs, y_values, label='y values')
plt.plot(msecs, z_values, label='z values')
plt.legend()
figure.show()

plt.show()