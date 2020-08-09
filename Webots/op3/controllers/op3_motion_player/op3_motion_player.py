import math
import time
from robot import Robot
from controllers.base_controller import BaseController
from controllers.walking_controller import WalkingController
from controllers.inclination_pitch_controller import InclinationPitchController
from controllers.inclination_roll_controller import InclinationRollController

base_controller = BaseController()
walking_controller = WalkingController()
inclination_pitch_controller = InclinationPitchController()
inclination_roll_controller = InclinationRollController()

controllers = [
    base_controller,
    inclination_pitch_controller,
    inclination_roll_controller,
    walking_controller,
]
base_controller.priority = 0
inclination_pitch_controller.priority = 1
inclination_roll_controller.priority = 1
walking_controller.priority = 2

robot = Robot(accuracy=1)

[controller.attach(robot) for controller in controllers]

while True:
    ik = {}
    angles = {}
    last_unstable_priority = -1
    for controller in controllers:
        controller.update()

        # testing
        if robot.current_time < 2000 and controller.name == 'WalkingController': continue
        if robot.current_time > 1000 and robot.current_time < 1500 and (controller.name == 'InclinationPitchController' or controller.name == 'InclinationRollController'): continue

        controls_parameters = controller.get_step()
        if 'ik' in controls_parameters:
            for value in controls_parameters['ik']:
                ik[value] = controls_parameters['ik'][value] + (ik[value] if value in ik else 0)
        if 'angles' in controls_parameters:
            for angle_name in controls_parameters['angles']:
                angles[angle_name] = controls_parameters['angles'][angle_name] + (angles[angle_name] if angle_name in angles else 0)

        if not controller.check_stability():
            last_unstable_priority = controller.priority

    if len(ik) > 0:
        ik_angles = robot.get_ik_angles(ik)
        for angle_name in ik_angles:
            angles[angle_name] = ik_angles[angle_name] + (angles[angle_name] if angle_name in angles else 0)
    robot.apply_angles(angles)
    robot.step()
        
    if robot.current_time == 20000 or all([controller.is_finished for controller in controllers]) and robot.current_time > 5000: 
        robot.save_data()
        break