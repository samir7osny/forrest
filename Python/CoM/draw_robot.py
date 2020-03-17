from cuboid import *
from motor import *
from robot import *
import math

robot = Robot()

dangle = 2
angle = 0 - dangle

def press(event):
    global angle, dangle
    if type(event) is not str and event.key == 'escape':
        plt.close(fig)
    if (type(event) is not str and event.key == 'a') or (type(event) is str):
        # import pdb; pdb.set_trace()
        ax.cla()
        # robot.rotate_x(30)
        if not (30 > angle + dangle > -30):
            dangle = -dangle
        angle += dangle
        robot.ShoulderR.rotate(angle)
        robot.ShoulderL.rotate(-angle)
        axis_info = robot.draw(ax)
        print(robot.mass)
        CoM = robot.CoM
        print(robot.CoM)
        ax.scatter([CoM[0]], [CoM[1]], [CoM[2]], c=[20])
        
        # ax.set_xlim([axis_info[2][0], axis_info[2][1]])
        # ax.set_ylim([axis_info[2][0], axis_info[2][1]])
        # ax.set_zlim([axis_info[2][0], axis_info[2][1]])
        ax.set_xlim([-150, 150])
        ax.set_ylim([-150, 150])
        ax.set_zlim([-250, 250])
        ax.set_xlabel('$X$')
        ax.set_ylabel('$Y$')
        ax.set_zlabel('$Z$')

        if type(event) is str:
            plt.show()
        else:
            event.canvas.draw()
    

fig = plt.figure(figsize=(9.5, 9.5))
fig.canvas.mpl_connect('key_press_event', press)
ax = fig.gca(projection='3d')

press('start')

mng = plt.get_current_fig_manager()
mng.window.wm_geometry("+200+0")
# plt.show()