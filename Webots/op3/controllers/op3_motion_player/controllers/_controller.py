
class _controller:
    def __init__(self, accuracy=1):
        self.accuracy = accuracy
        self.current_time = 0
        self.active = True
        self.priority = -1
        self.name = 'controller'
        self.buffer = []

    def attach(self, robot):
        self.robot = robot

    def flush_buffer(self):
        data = self.buffer
        self.buffer = []
        return data

    def update(self):
        pass

    def get_step(self):
        pass

    def check_stability(self):
        return True

    @property
    def is_finished(self):
        return True