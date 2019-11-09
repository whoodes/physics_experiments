from matplotlib import pyplot as plt
from matplotlib.legend_handler import HandlerLine2D

import numpy as np
from scipy import stats

plt.rc('font', size=18)

data = {
    '100_med': [ 4.81, 4.27, 4.08, 3.94, 3.82],
    '150_med': [3.20, 3.14, 3.32, 3.57, 3.21],
    '100_small': [6.15, 5.97, 6.16, 6.12, 6.23],
    '150_small': [5.05, 4.80, 4.82, 4.82, 4.77],
}

def get_error_values(key_value):
    values = data[key_value]
    summation = 0.0
    average = sum(values) / len(values)

    for value in values:
        summation += (value - average)**2
    std_dev = (summation / (len(values) - 1))**0.5
    sdm = std_dev / (len(values))**0.5
    t_error = 2 * average * sdm

    print("KEY: ", key)
    print("STD DEV: %f" % (std_dev,))
    print("SDM: %f" % (sdm,))
    print("average: %f" % (average,))
    print("delta(T^2): %f" % ((2 * average * sdm),))
    print('T^2 %f' % (average**2))
    print("ERROR!!!", t_error)
    print("***************************************************\n")


    return average**2, t_error

ordered_pairs = []
for key, value in data.items():
    t_squared = get_error_values(key)[0]
    x_y_error = ()

    if '100_med' in key:
        x_y_error = (1.828 / (0.0349 * t_squared), (0.00349 * (9.8 - (1.828 / t_squared))), 0.002803)
        print(key, x_y_error)
    elif '150_med' in key:
        x_y_error = (1.828 / (0.0349 * t_squared), (0.005235 * (9.8 - (1.828 / t_squared))), 0.002341)
        print(key, x_y_error)
    elif '100_small' in key:
        x_y_error = (1.828 / (0.0255 * t_squared), (0.00255 * (9.8 - (1.828 / t_squared))), 0.000354)
        print(key, x_y_error)
    elif '150_small' in key:
        x_y_error = (1.828 / (0.0255 * t_squared), (0.003825 * (9.8 - (1.828 / t_squared))), 0.0007717)
        print(key, x_y_error)
    ordered_pairs.append(x_y_error)

x_coordinates = [pair[0] for pair in ordered_pairs]
y_coordinates = [pair[1] for pair in ordered_pairs]
plt.plot(x_coordinates, y_coordinates, 'go', markersize=5)

slope, intercept, r_value, p_value, std_err = stats.linregress(x_coordinates, y_coordinates)
x = np.linspace(1.8, 5)  # span the graph
y = slope * x + intercept
delta, = plt.plot(x, y, label="v1, final: y = %.4fx + %.3f" %
                  (slope, intercept,))

error_bars = [pair[2] for pair in ordered_pairs]
plt.errorbar(x_coordinates, y_coordinates,
             yerr=error_bars, fmt='|',
             capsize=3, ecolor='green')

plt.legend(handler_map={delta: HandlerLine2D(numpoints=1)})

plt.title('Graph of the Relationship Between Applied Torque and Angular Acceleration')
plt.xlabel('Angular acceleration', fontsize=16)
plt.ylabel('Applied torque', fontsize=16)
plt.show()