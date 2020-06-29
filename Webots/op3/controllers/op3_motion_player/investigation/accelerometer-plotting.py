import numpy as np
import matplotlib.pyplot as plt



# acc = np.array([9.81, 0, 0])
# a2 = np.degrees(np.arctan2(acc[1], np.sqrt(acc[0]**2 + acc[2]**2)))
# a1 = np.degrees(np.arctan2(acc[0], np.sqrt(acc[1]**2 + acc[2]**2)))
# a3 = np.degrees(np.arctan2(acc[2], np.sqrt(acc[0]**2 + acc[1]**2)))
# print(a1, a2, a3)
# exit()


file = open('local-values-nothing-2.txt', 'r')

accelerometer_lines = [line for line in file.readlines() if 'accelerometer' in line]

accelerometer_values = [np.array(eval(line[len('accelerometer '): ])) if 'nan' not in line else np.array([0, 0, 0]) for line in accelerometer_lines]
# accelerometer_values = accelerometer_values[2400: 2900]
# accelerometer_values = accelerometer_values[668: ]
values = []
# print(accelerometer_values[0])
for t, _values in enumerate(accelerometer_values):
    # _values = _values / 9.81
    # _values = _values - accelerometer_values[0]
    # _values = _values - np.array([0.00039233646733960936, -4.0066485772406855e-06, 9.81000006194588])
    # _values -= (accelerometer_values[t - 1] if t != 0 else np.array([0, 0, 0]))
    # _values = np.clip(_values,-8.5,5)
    a1 = np.degrees(np.arctan2(_values[0], np.sqrt(_values[1]**2 + _values[2]**2)))
    a2 = np.degrees(np.arctan2(_values[1], np.sqrt(_values[0]**2 + _values[2]**2)))
    a3 = np.degrees(np.arctan2(np.sqrt(_values[0]**2 + _values[1]**2), _values[2]))
    current_values = np.array([a1, a2, a3])
    # current_values = (values[-1] if len(values) > 1 else np.array([0, 0, 0])) + _values * (1 / 1000)
    # current_values = np.degrees(np.array([np.arctan2(values[0], np.sqrt(values[1]**2 + values[2]**2)),
    #                             np.arctan2(values[1], np.sqrt(values[0]**2 + values[2]**2)),
    #                             np.arctan2(values[2], np.sqrt(values[0]**2 + values[1]**2))
    #                 ]))
    # current_values[0] = 90 - current_values[0]
    values.append(current_values)

d_values = []
for t, _values in enumerate(values):
    current_values = (d_values[-1] if len(d_values) > 1 else np.array([0, 0, 0])) + _values * (1 / 1000)
    # current_values = np.degrees(np.array([np.arctan2(values[0], np.sqrt(values[1]**2 + values[2]**2)),
    #                             np.arctan2(values[1], np.sqrt(values[0]**2 + values[2]**2)),
    #                             np.arctan2(values[2], np.sqrt(values[0]**2 + values[1]**2))
    #                 ]))
    # current_values[0] = 90 - current_values[0]
    d_values.append(current_values)

# print(accelerometer_values[0: 2])
print(accelerometer_values[4000])
# print(values[-2: ])
# print(np.max(values))
# print(len(values))

x_acc = [values[0] for values in accelerometer_values]
y_acc = [values[1] for values in accelerometer_values]
z_acc = [values[2] for values in accelerometer_values]

x_values = [values[0] for values in values]
y_values = [values[1] for values in values]
z_values = [values[2] for values in values]

x_displacement = [values[0] for values in d_values]
y_displacement = [values[1] for values in d_values]
z_displacement = [values[2] for values in d_values]

msecs = list(range(0, len(x_acc), 1))

figure = plt.figure(1)
plt.plot(msecs, x_acc, label='x')
plt.plot(msecs, y_acc, label='y')
plt.plot(msecs, z_acc, label='z')
plt.legend()
plt.grid()
figure.show()

figure = plt.figure(2)
plt.plot(msecs, x_values, label='x values')
# plt.plot(msecs, y_values, label='y values')
# plt.plot(msecs, z_values, label='z values')
plt.legend()
plt.grid()
figure.show()


figure = plt.figure(3)
plt.plot(msecs, x_displacement, label='x displacement')
plt.plot(msecs, y_displacement, label='y displacement')
plt.plot(msecs, z_displacement, label='z displacement')
plt.legend()
plt.grid()
figure.show()

plt.show()

# -0.547807 0.322665 -0.301757
# 1 0 0 -1.5708

# 1.6401802550760076 0.26840023571238736 -0.8073025753874619
# 0.9549475634473905 -0.18854176136150066 -0.22918803478496627 -1.5799350826256409