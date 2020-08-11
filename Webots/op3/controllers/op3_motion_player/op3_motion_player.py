import math
import time
from robot import Robot
from controllers.base_controller import BaseController
from controllers.walking_controller import WalkingController
from controllers.inclination_pitch_controller import InclinationPitchController
from controllers.inclination_roll_controller import InclinationRollController
import json
import asyncio
import websockets
import threading

STATE_INIT = 0
STATE_READY = 1
STATE_PLAY = 2
STATE_DONE = 3

robot = Robot(accuracy=1)
controllers = []
current_state = STATE_INIT
buffer = []
mutex = False

def reset_simulation(path=None):
    global controllers, current_state
    print('reset')
    current_state = STATE_READY

    robot.robot.simulationReset()
    robot.reset()

    base_controller = BaseController()
    walking_controller = WalkingController(path=path)
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

    [controller.attach(robot) for controller in controllers]


    return True

def start_simulation():
    global current_state


    if current_state != STATE_READY: return False
    
    current_state = STATE_PLAY
    return True

def pause_simulation():
    global current_state

    if current_state != STATE_PLAY: return False
    
    current_state = STATE_READY
    return True


def control():
    global controllers, current_state, mutex

    reset_simulation()
    while True:
        if robot.current_time == 200: 
            buffer.append({
                'command': 'DONE',
                'current_state': current_state
            })
            
        while not mutex: pass
        mutex = False
        if current_state == STATE_PLAY:
            ik = {}
            angles = {}
            last_unstable_priority = -1
            for controller in controllers:
                controller.update()

                if robot.current_time < 2000 and controller.name == 'WalkingController': continue

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
            
        if len(controllers) > 0 and all([controller.is_finished for controller in controllers]) and robot.current_time > 5000: 
            # robot.save_data()
            current_state = STATE_DONE
            buffer.append({
                'command': 'DONE',
                'current_state': current_state
            })
        mutex = True
        
async def websocket_handler(websocket, path):
    global buffer, mutex

    rmssg = await websocket.recv()
    print('socket', rmssg)

    rmssg = json.loads(rmssg)
    command = rmssg['command']

    ackmssg = {
        'command': '404'
    }

    while not mutex: pass
    mutex = False
    if command == 'PATH':
        path = rmssg['path']
        ack = reset_simulation(path)

    if command == 'PLAY':
        ack = start_simulation()

    if command == 'PAUSE':
        ack = pause_simulation()
        
    if command in ['PATH', 'PLAY', 'PAUSE']:
        ackmssg = { 'command': 'ACK' if ack else 'NACK' }
    mutex = True

    if command == 'PING':
        if len(buffer) != 0: ackmssg = buffer.pop(0) 
        else: ackmssg = {'command': 'CLEAR'}

    ackmssg['current_state'] = current_state
    await websocket.send(json.dumps(ackmssg))

control_thread = threading.Thread(target=control)
control_thread.start()


start_server = websockets.serve(websocket_handler, "localhost", 7374)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

