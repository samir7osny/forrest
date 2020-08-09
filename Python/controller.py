from CoM.robot import *
from MotionPattern.walking_pattern_generator import *
import matplotlib.pyplot as plt 
from matplotlib import animation
import math
import serial

robot = Robot()
ser = serial.Serial('COM8', baudrate=9600, timeout=1)

def update_robot(num):
    left_foot_z_value = data['left_foot_z_value'][num]
    left_foot_x_value = data['left_foot_x_value'][num]
    right_foot_z_value = data['right_foot_z_value'][num]
    right_foot_x_value = data['right_foot_x_value'][num]
    pelvis_x_value = data['pelvis_x_value'][num]
    pelvis_y_value = data['pelvis_y_value'][num]


    a = np.sqrt((robot.HipToGround - left_foot_z_value) ** 2 - (-(left_foot_x_value - pelvis_x_value)) ** 2)
    LegAngleL, KneeAngleL, AnkleAngleL = inverse_kinematic_xz(a, -(left_foot_x_value - pelvis_x_value))
    LegAngleL, KneeAngleL, AnkleAngleL = -LegAngleL, -KneeAngleL, -AnkleAngleL
    
    a = np.sqrt((robot.HipToGround - right_foot_z_value) ** 2 - (-(right_foot_x_value - pelvis_x_value)) ** 2)
    LegAngleR, KneeAngleR, AnkleAngleR = inverse_kinematic_xz(a, -(right_foot_x_value - pelvis_x_value))

    a = robot.HipToLeg + robot.LegToKnee * np.cos(np.radians(LegAngleL)) + robot.KneeToAnkle * np.cos(np.radians(KneeAngleL))  + robot.AnkleToFoot * np.cos(np.radians(AnkleAngleL))
    HipAngleL, FootAngleL = inverse_kinematic_y(pelvis_y_value, a)
    a = robot.HipToLeg + robot.LegToKnee * np.cos(np.radians(LegAngleR)) + robot.KneeToAnkle * np.cos(np.radians(KneeAngleR))  + robot.AnkleToFoot * np.cos(np.radians(AnkleAngleR))
    HipAngleR, FootAngleR = inverse_kinematic_y(pelvis_y_value, a)
    
    robot.send_serial(ser, LegL=LegAngleL, KneeL=KneeAngleL, AnkleL=AnkleAngleL, LegR=LegAngleR, KneeR=KneeAngleR, AnkleR=AnkleAngleR, HipL=HipAngleL, FootL=FootAngleL, HipR=HipAngleR, FootR=FootAngleR)


line = {'line': None}
def pattern_init():
    pelvis_y_values = ax_pattern.plot(data['t'], np.array(data['pelvis_y_values']) * 50, label='pelvis y / 50')
    left_foot_z_values = ax_pattern.plot(data['t'], np.array(data['left_foot_z_values']) * 50, label='left foot z / 50')
    right_foot_z_values = ax_pattern.plot(data['t'], np.array(data['right_foot_z_values']) * 50, label='right foot z / 50')
    left_foot_x_values = ax_pattern.plot(data['t'], data['left_foot_x_values'], label='left foot x')
    right_foot_x_values = ax_pattern.plot(data['t'], data['right_foot_x_values'], label='right foot x')
    pelvis_x_values = ax_pattern.plot(data['t'], data['pelvis_x_values'], label='pelvis x')
    
    line['line'] = ax_pattern.axvline(x=0)
    ax_pattern.legend()

    return (pelvis_y_values, left_foot_z_values, right_foot_z_values, left_foot_x_values, right_foot_x_values, pelvis_x_values, line['line'])

def update_pattern(num, data, line):
    line['line'].set_xdata([num, num])
    fig_pattern.canvas.draw()
    return (line['line'], )

def update(num):
    global current_xidx, animation_running
    if current_xidx + 1 >= len(data['t']):
        animation_running = False
        return
    current_xidx += 10
    update_pattern(data['t'][current_xidx], data, line)
    update_robot(current_xidx)

def gen():
    global animation_running
    i = 0
    while animation_running:
        i += 1
        yield i

def inverse_kinematic_xz(a, b, theta):
    theta = math.radians(theta)
    l1, l2, l3 = robot.LegToKnee, robot.KneeToAnkle, robot.AnkleToFoot + robot.FootToGround
    a -= robot.HipToLegH
    A1 = a - l3*np.cos(theta)
    B1 = b - l3*np.sin(theta)
    R = np.sqrt(A1**2 + B1**2)
    Alpha = np.arccos(min(1, max(-1, (l1**2 + R**2 - l2**2) / (2*l1*R))))
    Q1 = np.arctan2(B1, A1) - Alpha
    Q2 = np.arctan2((R*np.sin(Alpha)), (R*np.cos(Alpha) - l1))
    Q3 = theta - Q1 - Q2

    return math.degrees(Q1), math.degrees(Q2), math.degrees(Q3)

def inverse_kinematic_y(dy, a):
    Q1 = np.arcsin((dy) / a)

    return math.degrees(Q1), math.degrees(Q1)

def event_handeler(event):
    global current_x, current_xidx, animation_running, ani
    if animation_running:
        ani.event_source.stop()
    if event.xdata is None: return
    current_x = max(0, min(data['t'][-1], event.xdata))
    current_xidx = int((current_x / (data['to'] - data['from'])) * data['Fs'])
    update_pattern(current_x, data, line)
    update_robot(current_xidx)

def key_event_handeler(event):
    global current_x, current_xidx, animation_running, ani
    if animation_running:
        ani.event_source.stop()
    animation_running = False
    current_x = data['t'][current_xidx]
    if event.key == 'escape':
        plt.close(fig_pattern)
    if event.key == 'right':
        current_x += 10
        current_xidx = int((current_x / (data['to'] - data['from'])) * data['Fs'])
        update_pattern(current_x, data, line)
        update_robot(current_xidx)
    if event.key == 'left':
        current_x -= 10
        current_xidx = int((current_x / (data['to'] - data['from'])) * data['Fs'])
        update_pattern(current_x, data, line)
        update_robot(current_xidx)
    if event.key == 'up':
        animation_running = True
        ani.event_source.start()
    # print(event.key, animation_running)

    
current_x = 0
current_xidx = 0
animation_running = False
ani = None

generator = PatternGenerator(L=robot.HipToGround)
data = generator.generate_full_pattern()
data = {
    't': data[0], # t,
    'right_foot_z_value': data[1], # right_foot_height,
    'left_foot_z_value': data[2], # left_foot_height,
    'pelvis_y_value': data[3], # pelvis_side_displacement,
    'right_foot_x_value': data[4], # right_foot_forward_displacement,
    'left_foot_x_value': data[5], # left_foot_forward_displacement,
    'pelvis_x_value': data[6], # pelvis_forward_displacement
}

update_robot(0)

fig_pattern = plt.figure()
ax_pattern = fig_pattern.gca()
pattern_init()
fig_pattern.canvas.mpl_connect('button_press_event', event_handeler)
fig_pattern.canvas.mpl_connect('key_press_event', key_event_handeler)
# ani = animation.FuncAnimation(fig_pattern, update_pattern,init_func=pattern_init, frames=data['to'] // sample_ratio, fargs=(data, line, ), interval=20, blit=False, repeat=False)
# ani = animation.FuncAnimation(fig_pattern, update, frames=gen, interval=200, blit=False, repeat=False)
animation_running = False
plt.show()