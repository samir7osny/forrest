from svgpathtools import parse_path
import numpy as np
from matplotlib import pyplot as plt
import time

WIDTH = 500
HEIGHT = 500
path = parse_path('M 300 100 C 100 100 200 200 200 300 L 250 350')

SAMPLES_PER_PX = 1

myPathList = []
pathLength = path.length()
numSamples = int(pathLength * SAMPLES_PER_PX)
for i in range(numSamples):
    point = path.point(path.ilength(pathLength * i / (numSamples-1)))
    myPathList.append([point.real, HEIGHT-point.imag])

data = np.array(myPathList)
x, y = data.T
plt.scatter(x,y, s=1)

point = [200, 380]
np.argmin(data)
plt.scatter(point[0], point[1], color='green', s=5)

# print(spatial.KDTree(data).query(point)[1]) # 196
nearest_idx = np.argmin(np.sqrt(np.sum((data - np.array(point)) ** 2, axis=1)))
d = 20
unit_vector = (data[nearest_idx + d] - data[nearest_idx]) / np.sqrt(np.sum((data[nearest_idx + d] - data[nearest_idx]) ** 2, axis=0))
print(unit_vector)
print(np.degrees(np.arctan2(unit_vector[1], unit_vector[0])))


target_point_idx = np.argmin(np.abs(np.sqrt(np.sum((data - np.array(point)) ** 2, axis=1)) - d))
print(np.sqrt(np.sum((data[target_point_idx] - point) ** 2, axis=0)))
nearest = data[nearest_idx]
traget_point = data[target_point_idx]
plt.scatter(*traget_point, color='red', s=5)
plt.quiver(*nearest, *unit_vector, width=0.003)
# print(np.argmin(np.sqrt(np.sum((data - np.array(point)) ** 2, axis=1))))

plt.scatter(nearest[0], nearest[1], color='yellow', s=5)
plt.axis('equal')
plt.show()