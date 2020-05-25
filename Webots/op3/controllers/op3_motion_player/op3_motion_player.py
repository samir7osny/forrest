import math
import time
from robot import Robot
from controllers.walking_controller import WalkingController
from controllers.balance_controller import BalanceController

walking_controller = WalkingController()
balance_controller = BalanceController()

controllers = [
    walking_controller,
    # balance_controller,
]

robot = Robot()

while True:
    angles = {}
    for controller in controllers:
        sensors = robot.get_sensors()
        controls_parameters = controller.get_step(sensors)

        controller_angles = {}
        if 'ik' in controls_parameters:
            controller_angles = robot.get_ik_angles(controls_parameters['ik'])

        if 'angles' in controls_parameters:
            controller_angles.update(controls_parameters['angles'])

        angles.update(controller_angles)

    robot.apply_angles(angles)
    robot.step()
        
    if any([controller.is_finished for controller in controllers]): break