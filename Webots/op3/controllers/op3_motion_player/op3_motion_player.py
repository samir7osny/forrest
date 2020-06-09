import math
import time
from robot import Robot
from controllers.base_controller import BaseController
from controllers.walking_controller import WalkingController
from controllers.inclination_pitch_controller import InclinationPitchController
from controllers.inclination_roll_controller import InclinationRollController
from controllers.landing_momentum_controller import LandingMomentumController

base_controller = BaseController()
walking_controller = WalkingController()
inclination_pitch_controller = InclinationPitchController()
inclination_roll_controller = InclinationRollController()
landing_momentum_controller = LandingMomentumController()

controllers = [
    base_controller,
    #inclination_pitch_controller,
    #inclination_roll_controller,
    landing_momentum_controller,
    walking_controller,
]
base_controller.priority = 0
inclination_pitch_controller.priority = 1
inclination_roll_controller.priority = 1
walking_controller.priority = 2
# DEF op3 Robot > Solid > HingeJoint > Solid > HingeJoint > Solid > HingeJoint > Solid > HingeJoint > Solid > HingeJoint > Solid > HingeJoint > Solid > TouchSensor
robot = Robot(accuracy=1)
changed = False
while True:
    ik = {}
    angles = {}
    last_unstable_priority = -1
    for controller in controllers:
        sensors = robot.get_sensors()
        controller.update(sensors)

        # if last_unstable_priority != -1 and (controller.priority == -1 or controller.priority > last_unstable_priority): 
        #     # print(robot.current_time, controller.name, 'ignore')
        #     continue

        # # testing
        if robot.current_time < 1000 and controller.name == 'WalkingController': 
            # print(controller.name, 'ignore')
            continue

        controls_parameters = controller.get_step()
        
        # controller_angles = {}
        # if 'ik' in controls_parameters:
        #     controller_angles = robot.get_ik_angles(controls_parameters['ik'])
        # if 'angles' in controls_parameters:
        #     controller_angles.update(controls_parameters['angles'])

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
    # print(robot.get_sensors()['touch_sensor'])
    robot.apply_angles(angles)
    robot.step()
        
    if all([controller.is_finished for controller in controllers]) and robot.current_time > 1000: 
        print(inclination_pitch_controller.tilt_angles[1])
        break