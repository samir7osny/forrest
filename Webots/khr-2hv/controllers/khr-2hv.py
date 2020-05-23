import math
from walking_pattern_plot import WalkingPatternPlot
from walking_pattern_generate import *
import zmq
import time
from robot import Robot

class WalkingController:
    def __init__(self):
        self.robot = Robot()

    def update(self, num):

        print(num)

        left_foot_z_value = self.data['left_foot_z_value'][num]
        left_foot_x_value = self.data['left_foot_x_values'][num]
        pelvis_x_value = self.data['pelvis_x_values'][num]
        right_foot_z_value = self.data['right_foot_z_values'][num]
        right_foot_x_value = self.data['right_foot_x_values'][num]
        pelvis_y_value = self.data['pelvis_y_values'][num]

        self.robot.update(left_foot_z_value, left_foot_x_value, right_foot_z_value, right_foot_x_value, pelvis_x_value, pelvis_y_value)


    def set_data(self, data):
        self.data = data


port = "5556"
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % port)
print("Started", flush=True)

walking_controller = WalkingController()

data = get_pattern()
walking_controller.set_data(data)
time.sleep(1)
print('data', flush=True)

while True:
    message = socket.recv_json()
    walking_controller.update(message['num'])
    time.sleep(1) 
    print(message, flush=True)
    socket.send_string("Done")