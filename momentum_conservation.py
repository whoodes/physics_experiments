import os
import re

from matplotlib import pyplot as plt
from matplotlib.legend_handler import HandlerLine2D

import numpy as np
from scipy import stats

data = dict()
plt.axis([0, 4, 0, 0.6])
med_large_files = os.listdir('./med-large')
plt.rc('font', size=18)

def get_error_values(key_value):
    values = data[key_value]
    average = sum(data[key_value][1]) / len(data[key_value])

    summation = 0.0
    for value in values:
        summation += (value[1] - average)**2
    std_dev = (summation / (len(data[key_value]) - 1))**0.5
    sdm = std_dev / (len(data[key_value]))**0.5

    print("STD DEV: %f" % (std_dev,))
    print("SDM: %f" % (sdm,))
    print()
    print("***************************************************")
    return std_dev, sdm


for file in med_large_files:
    with open(os.path.join('med-large', file), 'r') as f:
        cleaned_values = []
        for line in f.readlines():
            split = line.strip().split(' ')
            time, delta, position = split[0], split[1], split[2]
            cleaned_values.append((float(time), float(delta), float(position)))
    # Name the key as the particular data file.
    key = file.split('.', 1)[0]
    data.update({'%s' % (key,): cleaned_values})

sensor_2_error = get_error_values('sensor-2-medium-hitting-large-pos')
sensor_1_error = get_error_values('sensor-1-medium-hitting-large-with-pos')

# We remove the leading six data points as that measured the cart at rest.
time = [
    value[0]
    for value in data['sensor-1-medium-hitting-large-with-pos']
]
position = [
    value[2]
    for value in data['sensor-1-medium-hitting-large-with-pos']
]

# Clean up the data
del time[:6]
del position[:6]

# Plot for the final velocity of mass 1
slope, intercept, r_value, p_value, std_err = stats.linregress(time, position)
x = np.linspace(0, 4)  # span the graph
y = slope * x + intercept
delta, = plt.plot(x, y, label="v1, final: y = %.4fx + %.3f" %
                  (slope, intercept,))
plt.plot(time, position, 'yo', markersize=5)
plt.errorbar(time, position,
             yerr=sensor_1_error[0], fmt='|',
             capsize=3, ecolor='black')

# For running a linear regression on the initial velocity of mass_1,
# whose slope:
#   m = v_1i, the initial velocity of mass 1.
# Our first four data points represent the time before collision with
# the second mass, thus we delete all data proceeding these.
time_initial = time
del time_initial[4:]
position_initial = position
del position_initial[4:]

# Plot for the initial velocity of mass 1
slope, intercept, r_value, p_value, std_err = stats.linregress(
    time_initial, position_initial)
y = slope * x + intercept
delta, = plt.plot(x, y, label="v1, initial: y = %.3fx + %.4f" %
                  (slope, intercept,))
print("v1 initial error: %s" % (std_err,))
plt.plot(time, position, 'bo', markersize=5)

time = [
    value[0]
    for value in data['sensor-2-medium-hitting-large-pos']
]
position = [
    value[2]
    for value in data['sensor-2-medium-hitting-large-pos']
]

# A lot of this data turned out to be gargage, so throw away the first thirteen
# data points.  This is due to inaccuracy of the sensor beyond 50cm.
# The last three points recorded the cart bouncing off the
# other side of the track, and thus were not used.
del time[:13]
del position[:13]
del time[(len(time) - 3):]
del position[(len(position) - 3):]

# Plot for the final velocity of mass 2
slope, intercept, r_value, p_value, std_err = stats.linregress(time, position)
y = slope * x + intercept
delta, = plt.plot(x, y, label="v2, final: y = %.3fx + %.3f" %
                  (slope, intercept,))
plt.plot(time, position, 'go', markersize=5)
plt.errorbar(time, position,
             yerr=sensor_1_error[0], fmt='|',
             capsize=3, ecolor='green')
plt.legend(handler_map={delta: HandlerLine2D(numpoints=1)})

plt.title('Graph for a Medium Cart Impacting a Large Cart')
plt.xlabel('Time Measured in Seconds (s)', fontsize=16)
plt.ylabel('Distance of a Given Cart from a Particular Sensor (m)', fontsize=16)
plt.show()
