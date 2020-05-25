import numpy as np
from numpy import array as arr
import matplotlib.pyplot as plt
import math

Apelvis = 32
Hfoot = 40
d = 100#200
l_over_d = 0.45

Tstride = 1.9 * 1000
Tstep = 0.95 * 1000
Tdelay = 0.2 * 1000
Kdsp = 0.05
Tssp = Tstep * (1.0 - Kdsp)
Tdsp = Tstep * Kdsp
ALPHApelvis = 0.45

# op3
Apelvis = 50 # op3
Hfoot = 40
d = 100#200
l_over_d = 0.45

Tstride = 1.9 * 1000
Tstep = 0.95 * 1000
Tdelay = 0.2 * 1000
Kdsp = 0.2 # op3
Tssp = Tstep * (1.0 - Kdsp)
Tdsp = Tstep * Kdsp

Fs = 8000

def pelvis_y_pattern(t):
    sine_freq = 1 / ((Tstep - Tdelay) * 2)
    from_ = t[0]
    to = t[-1]
    def one_step(now):
        nth_step = (now - from_) // Tstep
        # print(nth_step)
        sign = 1 if nth_step % 2 == 1 else -1
        position = now - from_ - (nth_step * Tstep)
        if (Tstep - Tdelay) / 2 <= position <= (Tstep - Tdelay) / 2 + Tdelay:
            return sign * Apelvis
        elif (Tstep - Tdelay) / 2 > position:
            # print(np.sin(2 * np.pi * sine_freq * position / Fs))
            return sign * Apelvis * np.sin(2 * np.pi * sine_freq * position)
        else:
            position -= Tdelay
            return sign * Apelvis * np.sin(2 * np.pi * sine_freq * position)
    return [one_step(time_step) for time_step in t]

def foot_z_pattern(t):
    sine_freq = 1 / ((Tstep - Tdelay - Tdsp) * 2)
    from_ = t[0]
    to = t[-1]
    def one_step(now):
        nth_step = (now - from_) // Tstep
        # print(nth_step)
        sign = 1 if nth_step % 2 == 1 else -1
        position = now - from_ - (nth_step * Tstep)
        if 0 <= position <= Tdsp / 2 or Tstep - Tdsp / 2 <= position:
            return 0
        if (Tstep - Tdelay) / 2 <= position <= (Tstep - Tdelay) / 2 + Tdelay:
            return sign * Hfoot
        elif (Tstep - Tdelay) / 2 > position:
            position -= Tdsp/2
            return sign * Hfoot * np.sin(2 * np.pi * sine_freq * position)
        else:
            position -= Tdelay + Tdsp/2
            return sign * Hfoot * np.sin(2 * np.pi * sine_freq * position)
    return [one_step(time_step) for time_step in t]

def pelvis_x_pattern(t):
    cosine_freq = 1 / ((l_over_d * Tstep) * 4)
    sine_freq = 1 / (((1 - l_over_d) * Tstep) * 4)
    from_ = t[0]
    to = t[-1]
    ref_values = {'last_value': l_over_d * d, 'base_value': l_over_d * d, 'sine_phase': False}
    def one_step(now, ref_values):
        # now = max(now - Tstep, 0)
        if now < (1 - l_over_d) * Tstep: return 0
        now -= (1 - l_over_d) * Tstep
        nth_step = (now - from_) // Tstep
        position = now - from_ - (nth_step * Tstep)
        if position <= l_over_d * Tstep:
            if ref_values['sine_phase']:
                ref_values['base_value'] = ref_values['last_value']
                ref_values['sine_phase'] = False
            # position -= (1 - l_over_d) * Tstep
            # print(nth_step)
            offset = 0 if nth_step == 0 else l_over_d * d
            ref_values['last_value'] = ref_values['base_value'] + (l_over_d * d) * -np.cos(2 * np.pi * cosine_freq * position) + offset
            return ref_values['last_value']
        else:
            if not ref_values['sine_phase']:
                ref_values['base_value'] = ref_values['last_value']
                ref_values['sine_phase'] = True
            position -= (l_over_d) * Tstep
            ref_values['last_value'] = ref_values['base_value'] + ((1 - l_over_d) * d) * np.sin(2 * np.pi * sine_freq * position)
            return ref_values['last_value']
    return [one_step(time_step, ref_values) for time_step in t]

def foot_x_pattern(t, even=True):
    sine_freq = 1 / ((Tstep - Tdsp) * 2)
    from_ = t[0]
    to = t[-1]
    ref_values = {'last_value': 0, 'base_value': 0}
    def one_step(now, ref_values):
        nth_step = (now - from_) // Tstep
        position = now - from_ - (nth_step * Tstep)
        if not(Tdsp/2 <= position <= Tstep - Tdsp/2) or (even and nth_step % 2 == 0) or (not even and nth_step % 2 == 1):
            ref_values['base_value'] = ref_values['last_value']
            return ref_values['last_value']
        else:
            position -= Tdsp/2
            offset = 0 if not even and nth_step == 0 else d
            ref_values['last_value'] = max(0, ref_values['base_value'] + d * -np.cos(2 * np.pi * sine_freq * position) + offset)
            return ref_values['last_value']
    return [one_step(time_step, ref_values) for time_step in t]

def theta_pattern(z_values, max_theta = 0):
    max_z_value = max(z_values)
    return [0 for value in z_values]
    # return [max(0, max_theta * (value / max_z_value)) for value in z_values]

def get_pattern(from_=0, to=10000):
    global Fs
    Fs = to
    t = np.arange(from_, to, to / Fs)
    pelvis_y_values = pelvis_y_pattern(t)
    foot_z_values = foot_z_pattern(t)

    left_foot_z_values = [max(0, -v) for v in foot_z_values]
    right_foot_z_values = [max(0, v) for v in foot_z_values]

    left_theta_values = theta_pattern(left_foot_z_values)
    right_theta_values = theta_pattern(right_foot_z_values)

    left_foot_x_values = foot_x_pattern(t, False)
    right_foot_x_values = foot_x_pattern(t, True)
    # pelvis_x_values = [(lf + rf) / 2 for lf, rf in zip(left_foot_x_values, right_foot_x_values)]
    pelvis_x_values = pelvis_x_pattern(t)

    return {'t': t, 'pelvis_y_values': pelvis_y_values, 'foot_z_values': foot_z_values, 'left_foot_z_values': left_foot_z_values, 'right_foot_z_values': right_foot_z_values, 'left_theta_values': left_theta_values, 'right_theta_values': right_theta_values, 'left_foot_x_values': left_foot_x_values, 'right_foot_x_values': right_foot_x_values, 'pelvis_x_values': pelvis_x_values, 'from': from_, 'to': to, 'Hfoot': Hfoot, 'Fs': Fs, 'd': d}

if __name__ == "__main__":

    data = get_pattern()

    plt.plot(data['t'], np.array(data['pelvis_y_values']) * 50, label='pelvis y / 50')
    plt.plot(data['t'], np.array(data['left_foot_z_values']) * 50, label='left foot z / 50')
    plt.plot(data['t'], np.array(data['right_foot_z_values']) * 50, label='right foot z / 50')
    plt.plot(data['t'], np.array(data['left_theta_values']) * 100, label='left theta / 100')
    plt.plot(data['t'], np.array(data['right_theta_values']) * 100, label='right theta / 100')
    plt.plot(data['t'], data['left_foot_x_values'], label='left foot x')
    plt.plot(data['t'], data['right_foot_x_values'], label='right foot x')
    plt.plot(data['t'], data['pelvis_x_values'], label='pelvis x')
    plt.legend()
    # plt.axvline(x=5000)
    # plt.axis([0, to, -Hfoot - 10 - 2000, Hfoot + 10 + 2000])
    plt.show()