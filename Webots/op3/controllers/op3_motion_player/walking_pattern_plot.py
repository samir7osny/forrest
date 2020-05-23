# from CoM.robot import *
import math
from walking_pattern_generate import *
import matplotlib.pyplot as plt
from matplotlib import animation
import sympy as sp
import time
import threading
import zmq

class WalkingPatternPlot:
    def __init__(self, update_func):

        self.iterative_thread = None
        self.iterative_thread_running = False

        self.update_func = update_func

        self.current_x = 0
        self.current_xidx = 0

        self.data = get_pattern()
        print("data")

        self.update_func(self.data, 0)

        self.fig_pattern = plt.figure()
        self.ax_pattern = self.fig_pattern.gca()

        self.line = {'line': None}

        self.pattern_init()

        self.fig_pattern.canvas.mpl_connect('button_press_event', self.event_handeler)
        self.fig_pattern.canvas.mpl_connect('key_press_event', self.key_event_handeler)

        plt.show()


    def pattern_init(self):
        pelvis_y_values = self.ax_pattern.plot(self.data['t'], np.array(self.data['pelvis_y_values']) * 50, label='pelvis y / 50')
        left_foot_z_values = self.ax_pattern.plot(self.data['t'], np.array(self.data['left_foot_z_values']) * 50, label='left foot z / 50')
        right_foot_z_values = self.ax_pattern.plot(self.data['t'], np.array(self.data['right_foot_z_values']) * 50, label='right foot z / 50')
        left_foot_x_values = self.ax_pattern.plot(self.data['t'], self.data['left_foot_x_values'], label='left foot x')
        right_foot_x_values = self.ax_pattern.plot(self.data['t'], self.data['right_foot_x_values'], label='right foot x')
        pelvis_x_values = self.ax_pattern.plot(self.data['t'], self.data['pelvis_x_values'], label='pelvis x')
        
        self.line['line'] = self.ax_pattern.axvline(x=0)
        self.ax_pattern.legend()

        return (pelvis_y_values, left_foot_z_values, right_foot_z_values, left_foot_x_values, right_foot_x_values, pelvis_x_values, self.line['line'])

    def update_pattern(self, num, data, line):
        self.line['line'].set_xdata([num, num])
        self.fig_pattern.canvas.draw()
        return (self.line['line'], )

    def event_handeler(self, event):
        if event.xdata is None: return
        self.current_x = max(0, min(self.data['t'][-1], event.xdata))
        self.current_xidx = int((self.current_x / (self.data['to'] - self.data['from'])) * self.data['Fs'])
        self.update_pattern(self.current_x, self.data, self.line)
        self.update_func(self.data, self.current_xidx)

    def iteravtive_update(self):
        for idx in range(self.current_xidx, len(self.data['t'])):
            if not self.iterative_thread_running: break
            self.current_x = self.data['t'][idx]
            self.current_xidx = idx
            self.update_pattern(self.current_x, self.data, self.line)
            self.update_func(self.data, self.current_xidx)
            time.sleep(2)

    def key_event_handeler(self, event):
        if self.iterative_thread_running:
            self.iterative_thread_running = False
        if event.key == 'escape':
            plt.close(self.fig_pattern)
        if event.key == 'right':
            self.current_x += 10
            self.current_xidx = int((self.current_x / (self.data['to'] - self.data['from'])) * self.data['Fs'])
            self.update_pattern(self.current_x, self.data, self.line)
            self.update_func(self.data, self.current_xidx)
        if event.key == 'left':
            self.current_x -= 10
            self.current_xidx = int((self.current_x / (self.data['to'] - self.data['from'])) * self.data['Fs'])
            self.update_pattern(self.current_x, self.data, self.line)
            self.update_func(self.data, self.current_xidx)
        # if event.key == 'up':
        #     self.iterative_thread = threading.Thread(target=self.iteravtive_update) 
        #     self.iterative_thread.start()
        #     self.iterative_thread_running = True

        
if __name__ == "__main__":
    
    port = "5556"
    context = zmq.Context()
    print("Connecting to server...")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:%s" % port)

    def update(data, num):
        socket.send_json({
            'num': num
        })
        print(socket.recv_string())

    walking_pattern_plot = WalkingPatternPlot(update)

    socket.send_json({
        'num': -1
    })
    print(socket.recv_string())
