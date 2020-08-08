import numpy as np
import matplotlib.pyplot as plt
import pickle

file = open('local-values.pickle', 'rb')

data = pickle.load(file)

# print(np.array(data['actual_velocities'])[: 1])
# print(np.array(data['actual_velocities'])[: 1, [0, 2, 1]])
# print(np.array(data['velocities'])[: 1])
# print(np.array(data['velocities'])[: 1, [0, 1, 2]])

# data['actual_velocities'] = np.array(data['actual_velocities'])[:, [0, 2, 1]]
data['actual_velocities'] = np.array(data['actual_velocities'])
data['test'] = np.array(data['velocities']) - np.array(data['actual_velocities'])
data['test2'] = np.array(data['tilt_angles']) - np.array(data['orientation'])

# data['trap'] = []
# for i in range(20000):
#     data['trap'].append((np.trapz(data['corrected_accelerometer_values'][: i + 2], axis=0)/1000) - np.array([0,0,9.80999959e-03]))
# data['test2'] = np.array(data['trap'])[1:] - np.array(data['actual_velocities'])[:20000-1]

for idx, key in enumerate(data):

    info = np.array(data[key])
    info = info[0: 20000]
    msecs = list(range(0, len(info), 1))

    # if key == 'tilt_angles':
    #     print(key)
    #     print(np.trapz(info[:, 1], dx=(1 / 1000)))
    #     print(info[500])
        
    if key == 'velocities':
        print(key)
        print(info[-1])
        print(np.trapz(info[:, 0], dx=(1 / 1000)))
        # print(info[3000])
        # info[:, 1] = 0
        # info[:, 2] = 0
    if key == 'orientation':
        print(key)
        print(info[0])
    if key == 'tilt_angles':
        print(key)
        print(info[0])
    if key == 'actual_velocities':
        print(key)
        print(info[-1])
        print(np.trapz(info[:, 0], dx=(1 / 1000)))
    if key == 'accelerometer_values':
        print(key)
        print(info[280])
        print(info[0])
        # info[:, 1] = 0
        # info[:, 2] = 0
    if key == 'corrected_accelerometer_values':
        print(key)
        print(info[280])
        print(info[0])
        print(np.trapz(info[: 280], axis=0, dx = 1/1000))
    # if key == 'positions':
    #     print(key)
    #     print(info[-1])

    figure = plt.figure(key)
    figure.suptitle(key, fontsize=20)
    plt.plot(msecs, info[:, 0], label='X')
    plt.plot(msecs, info[:, 1], label='Y')
    plt.plot(msecs, info[:, 2], label='Z')
    plt.legend()
    plt.grid()
    # figure.show()

info = np.array(data['actual_position'])
info = info[1: ]
figure = plt.figure('actual_location')
figure.suptitle('actual_location', fontsize=20)
# print(info[:, 0][:10])
plt.scatter(info[:,2], info[:,0], s=1)
# plt.legend()
plt.grid()

plt.draw()
plt.pause(0.001)
while True:
    import pdb; pdb.set_trace()