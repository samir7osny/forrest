
class _controller:
    def __init__(self, accuracy=1):
        self.accuracy = accuracy
        self.current_time = 0

    def get_step(self, sensors):
        pass

    @property
    def is_finished(self):
        return True