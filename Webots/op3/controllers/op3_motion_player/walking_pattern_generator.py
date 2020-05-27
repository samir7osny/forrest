import numpy as np
import matplotlib.pyplot as plt


DEFAULT_Apelvis = 32
# DEFAULT_Apelvis = 50 # op3
DEFAULT_L = 900
DEFAULT_L = 254 # op3
DEFAULT_κdsp = 0.05
DEFAULT_κdsp = 0.2 # op3
DEFAULT_γpelvis = 0.45

CONST_Hfoot_ratio = 40 / DEFAULT_L
CONST_Hfoot_ratio = 30 / DEFAULT_L # op3
CONST_d_ratio = 200 / DEFAULT_L
CONST_d_ratio = 50 / DEFAULT_L # op3

CONST_Tdelay_ratio = 200 / 1900

GRAVITY = 9.81

# Apelvis               Lateral swing amplitude of pelvis 32 (mm)
# Hfoot                 Maximum elevation of foot 40 (mm)
# d                     Step length (stride/2) 200 (mm)
# Tstride               Walking period (stride time) 1.9 (s)
# Tstep                 Step time 0.95 (s)
# Tdelay                Delay time 0.2 (s)
# κdsp                  Double support ratio 0.05 (5%)
# Tssp                  Single support time Tstep * (1.0 - κdsp)
# Tdsp                  Double support time Tstep * κdsp
# γpelvis               Forward landing position ratio of the pelvis 0.45
# L                     The distance from foot to the pelvis 900 (mm)
class PatternGenerator:
    def __init__(self, Apelvis=DEFAULT_Apelvis, L=DEFAULT_L, κdsp=DEFAULT_κdsp, γpelvis=DEFAULT_γpelvis):
        self.Apelvis = Apelvis
        self.L = L
        self.κdsp = κdsp
        self.γpelvis = γpelvis

        self.Hfoot = CONST_Hfoot_ratio * self.L
        self.d = CONST_d_ratio * self.L
        self.Tstride = self.calculate_Tstride()
        self.Tstep = self.Tstride / 2
        self.Tdelay = CONST_Tdelay_ratio * self.Tstride
        self.Tssp = self.Tstride * (1 - self.κdsp)
        self.Tdsp = self.Tstride * self.κdsp

        # print('Apelvis', self.Apelvis)
        # print('L', self.L)
        # print('κdsp', self.κdsp)
        # print('γpelvis', self.γpelvis)
        # print('Hfoot', self.Hfoot)
        # print('d', self.d)
        # print('Tstride', self.Tstride)
        # print('Tstep', self.Tstep)
        # print('Tdelay', self.Tdelay)
        # print('Tssp', self.Tssp)
        # print('Tdsp', self.Tdsp)
    
    def calculate_Tstride(self):
        walking_freq = (1 / (2 * np.pi)) * np.sqrt(GRAVITY / (self.L / 1000))
        print(1000 / walking_freq)
        return 1000 / walking_freq

    def get_smooth_value(self, period, position, peroid_ratio=0.25, shift=0):
        period = period / 1000
        full_period = period / peroid_ratio
        freq = 1 / full_period
        position = position / 1000
        position = position % full_period
        return np.sin(2 * np.pi * freq * position + shift * 2 * np.pi)

    def generate_full_pattern(self, number_of_steps=5):

        t = list(range(int(np.ceil(self.Tstride)) * number_of_steps + 1))

        right_foot_height = self.foot_height(t)
        left_foot_height = self.foot_height(t, False)

        pelvis_side_displacement = self.pelvis_side_displacement(t)

        right_foot_forward_displacement = self.foot_forward_displacement(t)
        left_foot_forward_displacement = self.foot_forward_displacement(t, False)

        pelvis_forward_displacement = self.pelvis_forward_displacement(t)

        return t, right_foot_height, left_foot_height, pelvis_side_displacement, right_foot_forward_displacement, left_foot_forward_displacement, pelvis_forward_displacement

    def get_value_from_ranges(self, t, ranges):
        full_period = np.sum([_range['period'] for _range in ranges])
        t = t % full_period
        current_range = None
        current_range_idx = None
        cumulative_period = 0
        for idx, _range in enumerate(ranges):
            cumulative_period += _range['period']
            if t <= cumulative_period:
                current_range = _range
                current_range_idx = idx
                break
        if current_range['type'] == 'zero':
            return 0
        elif current_range['type'] == 'one':
            return 1
        elif current_range['type'] == 'neg_one':
            return -1
        elif current_range['type'] == 'smooth':
            prev_non_same_smooth = np.sum([_range['period'] for _range in ranges[: current_range_idx] if _range['type'] != 'smooth' or _range['id'] != current_range['id']])
            shift = 0 if 'shift' not in current_range else current_range['shift']
            return self.get_smooth_value(current_range['period'], t - prev_non_same_smooth, current_range['period_ratio'], shift)

    def foot_height(self, t, right=True):
        ranges = [
            {
                'type': 'zero',
                'period': self.Tdsp / 2
            },
            {
                'type': 'smooth',
                'period': (self.Tstep - self.Tdelay - self.Tdsp) / 2,
                'period_ratio': 0.25,
                'id': 0
            },
            {
                'type': 'one',
                'period': self.Tdelay
            },
            {
                'type': 'smooth',
                'period': (self.Tstep - self.Tdelay - self.Tdsp) / 2,
                'period_ratio': 0.25,
                'id': 0
            },
            {
                'type': 'zero',
                'period': self.Tdsp / 2
            },
        ]

        if type(t) is not int:
            _time = t
            result = []
            for t in _time:

                if right and int(t / self.Tstep) % 2 == 0: self_period = True
                elif right: self_period = False
                elif int(t / self.Tstep) % 2 == 1: self_period = True
                else: self_period = False

                if self_period:
                    result.append(self.Hfoot * self.get_value_from_ranges(t, ranges))
                else: 
                    result.append(0)

            return result
        else:
            if right and int(t / self.Tstep) % 2 == 0: self_period = True
            elif right: self_period = False
            elif int(t / self.Tstep) % 2 == 1: self_period = True
            else: self_period = False

            if self_period:
                return self.Hfoot * self.get_value_from_ranges(t, ranges)
            else: 
                return 0

    def pelvis_side_displacement(self, t):
        ranges = [
            {
                'type': 'smooth',
                'period': (self.Tstep - self.Tdelay) / 2,
                'period_ratio': 0.25,
                'id': 0
            },
            {
                'type': 'one',
                'period': self.Tdelay
            },
            {
                'type': 'smooth',
                'period': (self.Tstep - self.Tdelay) / 2,
                'period_ratio': 0.25,
                'id': 0
            }
        ]

        if type(t) is not int:
            _time = t
            result = []
            for t in _time:

                if int(t / self.Tstep) % 2 == 0: result.append(self.Apelvis * self.get_value_from_ranges(t, ranges))
                else: result.append(- self.Apelvis * self.get_value_from_ranges(t, ranges))

            return result
        else:
            if int(t / self.Tstep) % 2 == 0: return self.Apelvis * self.get_value_from_ranges(t, ranges)
            else: return - self.Apelvis * self.get_value_from_ranges(t, ranges)

    def pelvis_forward_displacement(self, t):
        ranges = [
            {
                'type': 'smooth',
                'period': (1 - self.γpelvis) * self.Tstep,
                'period_ratio': 0.25,
                'id': 1
            },
            {
                'type': 'smooth',
                'period': self.γpelvis * self.Tstep,
                'period_ratio': 0.25,
                'id': 0,
                'shift': 0.75
            }
        ]

        if type(t) is not int:
            _time = t
            result = []
            for t in _time:
                t = max(0, t - self.Tstep / 2)

                if (t % self.Tstep) < (1 - self.γpelvis) * self.Tstep:
                    result.append((self.d * (1 - self.γpelvis)) * self.get_value_from_ranges(t, ranges) + self.d * int(t / self.Tstep))
                else:
                    result.append((self.d * self.γpelvis) * self.get_value_from_ranges(t, ranges) + self.d * int(t / self.Tstep) + self.d)

            return result
        else:
            t = max(0, t - self.Tstep / 2)
            if (t % self.Tstep) < (1 - self.γpelvis) * self.Tstep:
                return (self.d * (1 - self.γpelvis)) * self.get_value_from_ranges(t, ranges) + self.d * int(t / self.Tstep) - self.d / 2
            else:
                return (self.d * self.γpelvis) * self.get_value_from_ranges(t, ranges) + self.d * int(t / self.Tstep) + self.d - self.d / 2

        # if type(t) is not int:
        #     _time = t
        #     result = []
        #     for t in _time:

        #         right_forward = self.foot_forward_displacement(t)
        #         left_forward = self.foot_forward_displacement(t, False)

        #         min_ = min(right_forward, left_forward)
        #         max_ = max(right_forward, left_forward)

        #         result.append(self.γpelvis * max_ + (1 - self.γpelvis) * min_)

        #     return result
        # else:
        #     right_forward = self.foot_forward_displacement(t)
        #     left_forward = self.foot_forward_displacement(t, False)

        #     min_ = min(right_forward, left_forward)
        #     max_ = max(right_forward, left_forward)

        #     return self.γpelvis * max_ + (1 - self.γpelvis) * min_

    def foot_forward_displacement(self, t, right=True):
        ranges = [
            {
                'type': 'neg_one',
                'period': self.Tdsp / 2
            },
            {
                'type': 'smooth',
                'period': (self.Tstep - self.Tdsp),
                'period_ratio': 0.5,
                'id': 0,
                'shift': -0.25
            },
            {
                'type': 'one',
                'period': self.Tdsp / 2
            },
        ]
            
        if type(t) is not int:
            _time = t
            result = []
            for t in _time:

                if right and int(t / self.Tstep) % 2 == 0: self_period = True
                elif right: self_period = False
                elif int(t / self.Tstep) % 2 == 1: self_period = True
                else: self_period = False

                if self_period:
                    result.append(max(0, self.d * self.get_value_from_ranges(t, ranges) + self.d * int(t / self.Tstep)))
                else: 
                    result.append(self.d * int(t / self.Tstep))

            return result
        else:
            if right and int(t / self.Tstep) % 2 == 0: self_period = True
            elif right: self_period = False
            elif int(t / self.Tstep) % 2 == 1: self_period = True
            else: self_period = False

            if self_period:
                return max(0, self.d * self.get_value_from_ranges(t, ranges) + self.d * int(t / self.Tstep))
            else: 
                return self.d * int(t / self.Tstep)

if __name__ == "__main__":
        
    pattern_generator = PatternGenerator()
    pattern = pattern_generator.generate_full_pattern()

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    max_of_first_3 = np.max([np.max(pattern[idx]) for idx in range(1, 4)])
    max_of_second_3 = np.max([np.max(pattern[idx]) for idx in range(4, 7)])
    divider = max_of_second_3 / max_of_first_3

    [plt.plot(pattern[0], pattern[idx]) if idx < 4 else plt.plot(pattern[0], np.array(pattern[idx]) / divider) for idx in range(1, len(pattern))]

    start, end = ax.get_xlim()
    x_ticks = np.arange(0, end + 1, int(np.ceil(pattern_generator.Tstride / 2)))
    start, end = ax.get_ylim()
    y_ticks = np.arange(0, end + 1, pattern_generator.d / divider)
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)

    ax.grid()
    plt.show()