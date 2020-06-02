
class _controller:
    def __init__(self, accuracy=1):
        self.accuracy = accuracy
        self.current_time = 0
        self.active = True
        self.priority = -1
        self.name = 'controller'

    def update(self, sensors):
        pass

    def get_step(self):
        pass

    def check_stability(self):
        return True

    @property
    def is_finished(self):
        return True