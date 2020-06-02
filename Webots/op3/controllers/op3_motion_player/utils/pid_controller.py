
class PID:
    def __init__(self, Kp=1, Ki=0.1, Kd=0.6, guard=(None, None), sampling_time=1):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

        self.I = 0
        self.D = 0

        self.last_error = None
        
        self.guard = guard

        self.time = 0
        self.sampling_time = sampling_time
        self.value = 0

    def __call__(self, error, delta=1):
        return self.update(error, delta)

    def apply_guard(self, value):
        if self.guard[0] is None: return value
        if value > self.guard[1]: return self.guard[1]
        if value < self.guard[0]: return self.guard[0]
        return value

    def update(self, error, delta=1):
        self.time += delta

        if self.time >= self.sampling_time:
            self.I += error * (self.time / 1000)
            self.I = self.apply_guard(self.I)

            d_error = error - (self.last_error if self.last_error is not None else error)

            self.D = d_error / (self.time / 1000) if self.time != 0 else 0

            self.last_error = error

            # print(self.value, error, self.I, self.D)
            self.value = self.Kp * error + self.Ki * self.I + self.Kd * self.D
            self.value = self.apply_guard(self.value)

            self.time = 0

        return self.value