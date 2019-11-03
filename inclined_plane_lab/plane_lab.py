
import os
from matplotlib import pyplot as plt
from matplotlib.legend_handler import HandlerLine2D

import numpy as np
from scipy import stats

data = dict()
speed_of_sound_files = os.listdir('speed_of_sound')
gravity_files = os.listdir('gravity')

plt.rc('font', size=14)

def formalize_data(key_value):
    """
    This function turns data points into the form of velocity vs change in time.

    We use simple kinematics as the principle to our formula namely:

    Delta S = v_0 + a_x * Delta T

    Where Delta S is the velocity, v_0 is the initial velocity, a_x is the acceleration,
    and Delta T is the the change in time.
    """
    time = [delta_time[0] for delta_time in data[key_value]]
    delta = [delta_time[1] for delta_time in data[key_value]]

    # time_delta has N - 1 elements, we delete the first
    # two deltas leaving N - 3.
    time_delta = []
    for i in range(1, len(delta)):
        time_delta.append(time[i] - time[0])
    del time_delta[:2]

    position = []
    for i in range(1, len(delta)):
        position.append((SPEED_OF_SOUND * delta[i]) / 2)

    # pos_delta has N - 1 - 1 = N - 2 elements, we therefore delete the
    # first entry, leaving N - 3
    pos_delta = []
    for i in range(1, len(position)):
        pos_delta.append(position[i] - position[0])
    del pos_delta[:1]

    y_value = [y / x for (x, y) in zip(time_delta, pos_delta)]

    # print(
    #     '{key}: time delta: {time_delt},\n\n position: {pos},\n\n pos delta: {pos_delt},\n\n'
    #     'velocity: {velocity}'.format(
    #         key=key_value,
    #         time_delt=time_delta,
    #         pos=position,
    #         pos_delt=pos_delta,
    #         velocity=y_value
    #     )
    # )

    return time_delta, y_value

def get_error_values(key_value):
    values = data[key_value]
    average = sum(data[key_value][1]) / len(data[key_value])

    summation = 0.0
    for value in values:
        summation += (value[1] - average)**2
    std_dev = (summation / (len(data[key_value]) - 1))**0.5

    print("STD DEV: %f" % std_dev)
    print("SDM: %f" % (std_dev / (5)**0.5))
    print()
    print("***************************************************")
    return std_dev

def get_static_error(average, data):
    summation = 0.0
    for value in data:
        summation += (value - average)**2
    std_dev = (summation / (len(data) - 1))**0.5

    print("STD DEV: %f" % std_dev)
    print("SDM: %f" % (std_dev / (5)**0.5))
    print()
    print("***************************************************")
    return std_dev

"""
Each entry here is simply the delta, they are stored as follows:

<Ncm>: [delta1, delta2, ..., deltaM]

These values are averaged out and used to determine the speed of sound.
"""

for file in speed_of_sound_files:
    with open(os.path.join('speed_of_sound', file), 'r') as f:
        cleaned_values = []
        for line in f.readlines():
            y = line.strip().split(' ')[1]
            cleaned_values.append(float(y))
    key = file.split('.', 1)[0]
    data.update({'%s' % (key,): cleaned_values})

# Average Delta T values

delta_1_avg = sum(data['1400cm']) / len(data['1400cm'])
delta_1_err = get_static_error(delta_1_avg, data['1400cm'])

delta_2_avg = sum(data['1300cm']) / len(data['1300cm'])
delta_2_err = get_static_error(delta_2_avg, data['1300cm'])

delta_3_avg = sum(data['1200cm']) / len(data['1200cm'])
delta_3_err = get_static_error(delta_3_avg, data['1200cm'])

# delta_4_avg = sum(data['1100cm']) / len(data['1100cm'])  # This is a duplicate of delta_3

delta_5_avg = sum(data['1000cm']) / len(data['1000cm'])
delta_5_err = get_static_error(delta_5_avg, data['1000cm'])


plt.axis([1350, 1850, 0.0007, 0.004])
plt.plot(1400, delta_1_avg)
plt.errorbar(1400, delta_1_avg,
             yerr=delta_1_err, fmt='|', capsize=3,
             ecolor='red')
plt.plot(1500, delta_2_avg)
plt.errorbar(1500, delta_2_avg,
             yerr=delta_2_err, fmt='|', capsize=3,
             ecolor='red')
plt.plot(1600, delta_3_avg)
plt.errorbar(1600, delta_3_avg,
             yerr=delta_3_err, fmt='|', capsize=3,
             ecolor='red')
plt.plot(1800, delta_5_avg)
plt.errorbar(1800, delta_5_avg,
             yerr=delta_5_err, fmt='|', capsize=3,
             ecolor='red')

x = [1400, 1500, 1600, 1800]
y = [delta_1_avg, delta_2_avg, delta_3_avg, delta_5_avg]         
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

x = np.linspace(1350, 1850)  # span the graph
y = slope * x + intercept
delta, = plt.plot(x, y, label="Linear regression: y = %.8fx + %.5f" %
         (slope, intercept,))

print('std err: %s' % (std_err,))

plt.legend(handler_map={delta: HandlerLine2D(numpoints=1)})
plt.title('Graph for the Static Distance Experiment for the measurment of the Speed of Sound')
plt.xlabel('Distance form the cart to the ultrasonic sensor (mm)')
plt.ylabel('Time delta for the sensor\'s signal to reutrn back to the point of origin (s)')
plt.show()


SPEED_OF_SOUND = (2 / round(slope, 9)) / 1000

"""
Each entry in the dictionary is as follows:

<left|right>-side-raised-by-<M>-blocks: [(time1, delta1), (time2, delta2), ..., (timeM, deltaM)]

We will create a table to derive values for the position function that will yield the acceleration
in the slope of the linear fit, we can use the slope value to determine _g_.
"""

for file in gravity_files:
    with open(os.path.join('gravity', file), 'r') as f:
        cleaned_values = []
        for line in f.readlines():
            split = line.strip().split(' ')
            time = split[0]
            delta = split[1]
            cleaned_values.append((float(time), float(delta)))
    key = file.split('.', 1)[0]
    data.update({'%s' % (key,): cleaned_values})

  # ------------------------------------------------------------------ #
# -----------------------Left / right by two ------------------------- #
  # ------------------------------------------------------------------ #

# ------------ Left ------------- #
time_delta, y_value = formalize_data('left-side-raised-two-blocks')
plt.plot(time_delta, y_value, 'ro')

err = get_error_values('left-side-raised-two-blocks')
plt.errorbar(time_delta, y_value,
             yerr=err, fmt='|', capsize=3,
             ecolor='red')

slope, intercept, r_value, p_value, std_err = stats.linregress(time_delta, y_value)
x = np.linspace(0, 1.4)  # span the graph
y = slope * x + intercept
delta, = plt.plot(x, y, label="Left raised regression: y = %.3fx + %.3f" %
         (slope, intercept,))
plt.legend(handler_map={delta: HandlerLine2D(numpoints=1)})
print("ERRR left 2", std_err)

# ------------ Right ------------- #
time_delta, y_value = formalize_data('right-side-raised-by-two')
plt.plot(time_delta, y_value, 'bo')

err = get_error_values('right-side-raised-by-two')
plt.errorbar(time_delta, y_value,
             yerr=err, fmt='|', capsize=3,
             ecolor='blue')

slope, intercept, r_value, p_value, std_err = stats.linregress(time_delta, y_value)
x = np.linspace(0, 1.4)  # span the graph
y = slope * x + intercept
delta, = plt.plot(x, y, label="Right raised regression: y = %.3fx + %.3f" %
         (slope, intercept,))
plt.legend(handler_map={delta: HandlerLine2D(numpoints=1)})
print("ERRR right 2", std_err)
plt.axis([0, 1.4, -0.35, 0])
plt.title('Graph for the Sliding cart Experiment for the left and Right Sides Raised by Two Blocks')
plt.xlabel('The Change in Time During Active Measurements (s)')
plt.ylabel('The velocity of the cart along the track towards the sensor (mm/s)')
plt.show()

  # ------------------------------------------------------------------ #
# -----------------------Left / right by three ------------------------- #
  # ------------------------------------------------------------------ #

# ------------ Left ------------- #
time_delta, y_value = formalize_data('left-side-raised-three-blocks')
plt.plot(time_delta, y_value, 'yo')

err = get_error_values('right-side-raised-by-two')
plt.errorbar(time_delta, y_value,
             yerr=err, fmt='|', capsize=3,
             ecolor='black')

slope, intercept, r_value, p_value, std_err = stats.linregress(time_delta, y_value)
x = np.linspace(0, 1.2)  # span the graph
y = slope * x + intercept
delta, = plt.plot(x, y, label="Left raised regression: y = %.3fx + %.3f" %
         (slope, intercept,))
plt.legend(handler_map={delta: HandlerLine2D(numpoints=1)})
print("ERRR left 3", std_err)
# ------------ Right ------------- #
time_delta, y_value = formalize_data('right-side-raised-by-three')
plt.plot(time_delta, y_value, 'go')

err = get_error_values('right-side-raised-by-two')
plt.errorbar(time_delta, y_value,
             yerr=err, fmt='|', capsize=3,
             ecolor='green')

slope, intercept, r_value, p_value, std_err = stats.linregress(time_delta, y_value)
x = np.linspace(0, 1.2)  # span the graph
y = slope * x + intercept
delta, = plt.plot(x, y, label="Right raised regression: y = %.3fx + %.3f" %
         (slope, intercept,))
plt.legend(handler_map={delta: HandlerLine2D(numpoints=1)})
print("ERRR right 3", std_err)
plt.axis([0, 1.2, -0.5, 0.2])
plt.title('Graph for the Sliding cart Experiment for the left and Right Sides Raised by Three Blocks')
plt.xlabel('The Change in Time During Active Measurements (s)')
plt.ylabel('The velocity of the cart along the track towards the sensor (mm/s)')
plt.show()