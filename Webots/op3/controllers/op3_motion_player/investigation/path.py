from svgpathtools import parse_path
import numpy as np
from matplotlib import pyplot as plt
width=500
height=500
path_str = 'M 300 100 C 100 100 200 200 200 300 L 250 350 L 220 300'
# path_str = 'm 100 100 c 59 47 33 19 150 40 l 100 0 l -51 -8'
# path_str = 'm 0 0 l 500 0'
path_str = 'm 0 0 c 0 0 250 50 500 0'

path = parse_path(path_str)

SAMPLES_PER_PX = 1

points = []
path_length = path.length()
num_samples = int(path_length * SAMPLES_PER_PX)
for i in range(num_samples):
    point = path.point(path.ilength(path_length * i / (num_samples-1)))
    points.append([point.real, height-point.imag])

points = np.array(points)
points -= points[0]
current_point_idx = 0
x, y = points.T
plt.scatter(x,y, s=1)

# get vectos
unit_vectors = (points[1:] - points[:-1]) / np.sqrt(np.sum((points[1:] - points[:-1]) ** 2, axis=1, keepdims=True))

# get vectors' orientations
get_vector_degree = lambda unit_vector: np.degrees(np.arctan2(unit_vector[1], unit_vector[0]))
get_vector = lambda angle: np.array([np.cos(np.radians(angle)), np.sin(np.radians(angle))])
get_distance = lambda points: np.sqrt(np.sum(points[0] - points[1]))
def get_distance(point1 ,point2):
    return np.sqrt(np.sum((point1 - point2) ** 2))
degrees = np.array([0] + [get_vector_degree(unit_vectors[idx]) - get_vector_degree(unit_vectors[idx + 1]) for idx in range(len(unit_vectors) - 1)])
# [plt.quiver(*points[idx], *unit_vectors[idx], width=0.003) for idx in range(0, len(unit_vectors), 10)]
# unit_vector1 = (points[1] - points[0]) / np.sqrt(np.sum((points[1] - points[0]) ** 2, axis=0))
# plt.quiver(*points[0], *unit_vector1, width=0.003)
# find checkpoints
mask = np.abs(degrees) > 0.5
mask[-1] = True
# reduce the checkpoints
for idx in range(len(mask)):
    mask[idx] = mask[idx] and sum(mask[idx - 20: idx]) == 0
[plt.scatter(x[idx], y[idx], color='red', s=20) if ele else None for idx, ele in enumerate(mask)]

# robot_position = np.array([5.54330768, -16.85882498])
robot_position = np.array([0, 0])
robot_z_tilt = 0
# robot_z_tilt = -12.722111068437277
# robot_position = np.array([-0.06088682, 1.29233404])
# robot_z_tilt = -150.73155977244693
robot_vector = get_vector(robot_z_tilt)
plt.quiver(*robot_position, *robot_vector, width=0.003, color='black')
max_angle = 20
max_d = 5
# plt.quiver(*points[10], *unit_vectors[10], width=0.003)

target_point = points[30]
move_vector = (target_point - robot_position) / np.sqrt(np.sum((target_point - robot_position) ** 2))
plt.quiver(*robot_position, *move_vector, width=0.003, color='red')
if np.degrees(np.arccos(np.dot(robot_vector, move_vector) / (np.linalg.norm(robot_vector) * np.linalg.norm(move_vector)))) > max_angle:
    δ = robot_vector[0] * move_vector[1] - robot_vector[1] * move_vector[0]
    δ = δ / np.abs(δ) if δ != 0 else 1
    angle = δ * max_angle
    move_vector = get_vector(angle)
    move_d = 0
else:
    δ = robot_vector[0] * move_vector[1] - robot_vector[1] * move_vector[0]
    angle = δ * np.degrees(np.arccos(np.dot(robot_vector, move_vector) / (np.linalg.norm(robot_vector) * np.linalg.norm(move_vector))))
    move_d = min(max_d, get_distance(robot_position, target_point))

print(angle, move_d)
print(get_vector_degree(move_vector), get_vector_degree(robot_vector))
plt.quiver(*robot_position, *move_vector, width=0.003, color='green')
plt.scatter(*target_point, color='yellow', s=20)
plt.scatter(*robot_position, color='green', s=20)

plt.axis('equal')
mng = plt.get_current_fig_manager()
mng.resize(*(np.array(mng.window.maxsize())*0.7))
plt.show()