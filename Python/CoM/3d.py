from cuboid import *
from motor import *
import math

# ArmMotorR.rotate_z(30)
ArmMotorL = Cuboid(size=(2, 2, 2), position=(4, 0, 0))
ArmMotorL.rotate_x(90)


LegMotor = Motor(size=(2, 4, 4), position=(4, 0, 0), rotation_axis_direction=(0, 1, 0), rotation_axis_position=(0, 0, -1))
LegMotor.rotate(0)

ArmMotorR = Cuboid(size=(1, 2, 3), position=(0, 0, 0))
ArmMotorR.rotate_x(30)
ArmMotorR.move((0, 3, 1))
# ArmMotorR.set_parent(LegMotor)
# ArmMotorR.move((1, 2, 1))


LegMotor2 = Motor(size=(2, 4, 4), position=(-4, 0, 0), rotation_axis_direction=(0, 1, 0), rotation_axis_position=(0, 0, -1))
# LegMotor2.rotate(180)
LegMotor2.set_parent(LegMotor)

objs = [LegMotor, LegMotor2, ArmMotorR]
objs = [LegMotor, LegMotor2]
# objs = [LegMotor]

def press(event):
    if event.key == 'escape':
        plt.close(fig)
    if event.key == 'a':
        # import pdb; pdb.set_trace()
        ax.cla()
        ax.set_xlim([-7,7])
        ax.set_ylim([-7,7])
        ax.set_zlim([-7,7])
        ax.set_xlabel('$X$')
        ax.set_ylabel('$Y$')
        ax.set_zlabel('$Z$')
        LegMotor.rotate(LegMotor.angle + 10)
        LegMotor2.rotate(LegMotor2.angle - 10)
        [obj.draw(ax) for obj in objs]
        CoM = CoM_objects(objs)
        ax.scatter([CoM[0]], [CoM[1]], [CoM[2]], c=[20])
        event.canvas.draw()
        print(objs[0].center)

fig = plt.figure(figsize=(9.5, 9.5))
fig.canvas.mpl_connect('key_press_event', press)
ax = fig.gca(projection='3d')
# ax.set_aspect('equal')
[obj.draw(ax) for obj in objs]
# fig.clf()
# ax = fig.gca(projection='3d')
CoM = CoM_objects(objs)
ax.scatter([CoM[0]], [CoM[1]], [CoM[2]], c=[20])

ax.set_xlim([-7,7])
ax.set_ylim([-7,7])
ax.set_zlim([-7,7])

ax.set_xlabel('$X$')
ax.set_ylabel('$Y$')
ax.set_zlabel('$Z$')

mng = plt.get_current_fig_manager()
mng.window.wm_geometry("+200+0")
# mng.full_screen_toggle()
plt.show()