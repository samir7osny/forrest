import math
from walking_pattern_plot import WalkingPatternPlot
from walking_pattern_generate import *
import zmq
import time
from robot import Robot


class WalkingController:
    def __init__(self, using_graph, accuracy=20):
        self.robot = Robot()

        self.accuracy = accuracy

        data = get_pattern()
        self.set_data(data)

        if using_graph:
            self.graph()
        else:
            self.simulate()

    def update(self, num, duration = 1000):

        # print(num)

        left_foot_z_value = self.data['left_foot_z_values'][num]
        left_foot_x_value = self.data['left_foot_x_values'][num]
        left_theta = self.data['left_theta_values'][num]
        pelvis_x_value = self.data['pelvis_x_values'][num]
        right_foot_z_value = self.data['right_foot_z_values'][num]
        right_foot_x_value = self.data['right_foot_x_values'][num]
        right_theta = self.data['right_theta_values'][num]
        pelvis_y_value = self.data['pelvis_y_values'][num]

        self.robot.update(left_foot_z_value, left_foot_x_value, right_foot_z_value, right_foot_x_value, pelvis_x_value, pelvis_y_value, left_theta, right_theta, duration)

    def graph(self):
        port = "5556"
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:%s" % port)
        print("Started", flush=True)

        time.sleep(1)
        print('data', flush=True)

        while True:
            message = socket.recv_json()

            if message['num'] == -1:
                socket.send_string("Done")
                break
            self.update(message['num'])
            time.sleep(1) 
            print(message, flush=True)
            socket.send_string("Done")

    def simulate(self):
        num_of_steps = 10000 // self.accuracy
        step_in_index = (len(self.data['t']) - 1) // num_of_steps
        print('step_in_index', step_in_index)
        for step in range(10000 // self.accuracy):
            self.update(step * step_in_index, self.accuracy)
            time.sleep(self.accuracy / 1000)


    def set_data(self, data):
        self.data = data


using_graph = False
walking_controller = WalkingController(using_graph)