import math
from matplotlib import pyplot as plt
from matplotlib.legend_handler import HandlerLine2D
import numpy as np
from scipy import stats

"""
Determination for the constant of gravitational acceleration using
a pendulum. Three experiments tested mass, initial degree for testing
the small angle approximation, and pendulum length.

Author: Wyatt Hoodes

This file shows a series of graphs, as opposed to using subplots,
as I needed each graph separate for a report.
"""

plt.rc('font', size=14)
N = 5  # Number of trials

mass_data = {
    'al': [1.5, 1.48, 1.48, 1.46, 1.49],
    'fe': [1.47, 1.46, 1.47, 1.47, 1.47],
    'pb': [1.48, 1.50, 1.48, 1.48, 1.50],
}

degree_data = {
    '5_degrees': [7.44, 7.38, 7.51, 7.49, 7.51],
    '10_degrees': [7.44, 7.5, 7.63, 7.45, 7.44],
    '15_degrees': [7.63, 7.44, 7.78, 7.59, 7.71],
    '20_degrees': [7.9, 7.64, 7.8, 7.7, 7.7],
    '25_degrees': [7.84, 7.71, 7.99, 7.64, 7.88],
    '30_degrees': [7.89, 8.03, 7.83, 7.92, 7.89],
    '35_degrees': [7.97, 7.88, 7.86, 8.17, 8.03],
    '40_degrees': [8.04, 8.17, 8.03, 8.24, 8.36],
    '45_degrees': [8.16, 8.35, 8.23, 8.38, 8.5],
}

length_data = {
    '20_cm': [4.37, 4.3, 4.28, 4.37, 4.24],
    '30_cm': [5.41, 5.35, 5.33, 5.4, 5.4],
    '40_cm': [6.14, 6.19, 6.05, 6.26, 6.20],
    '50_cm': [6.98, 7.06, 7.04, 6.98, 6.95],
    '60_cm': [7.69, 7.70, 7.71, 7.64, 7.83],
    '70_cm': [8.37, 8.28, 8.25, 8.10, 8.36],
}

'''

Begin mass data section

'''

for key, values in mass_data.items():
    print(('%s: ') % (key,), [round(value, 3) for value in values])

    average = sum(values) / 5
    print("AVG for %s: %f" % (key, round(average, 2)))

    summation = 0.0
    for value in values:
        summation += (value - average)**2
    std_dev = (summation / 4)**0.5

    print("STD DEV: %f" % std_dev)
    print("SDM: %f" % (std_dev / (5)**0.5))
    print()
    print("***************************************************")


###### Graph for mass data ######

al = 26.982
fe = 55.845
pb = 207.2

# Ordered pairs
xi = np.array([al] * N + [fe] * N + [pb] * N)
y = mass_data['al'] + mass_data['fe'] + mass_data['pb']

# Set the dimensions for the axes.
plt.axis([20, 225, 1.44, 1.53])

# Run a linear regression and add a label.
slope, intercept, r_value, p_value, std_err = stats.linregress(xi, y)
x = np.linspace(20, 225)  # span the graph
y = slope * x + intercept
plt.plot(x, y, label="Linear regression: y = %fx + %.2f" %
    (slope, intercept,))

# Plot the aluminum trials and the corresponding deviation.
aluminum, = plt.plot([al] * N, mass_data['al'],
                    'ro', markersize=4, 
                    label="Aluminum (Al)")
plt.errorbar([al] * N, mass_data['al'],
            yerr=0.014832, fmt='|', capsize=3,
            ecolor='red')

# Plot the iron trials and the corresponding deviation.
iron, = plt.plot([fe] * N, mass_data['fe'],
                'bo', markersize=4,
                label="Iron (Fe)")
plt.errorbar([fe] * N, mass_data['fe'],
            yerr=0.004472, fmt='|', capsize=3,
            ecolor='blue')

# Plot the plead trials and corresponding deviation.
lead, = plt.plot([pb] * N, mass_data['pb'], 'go', markersize=4, label="Lead (Pb)")
plt.errorbar([pb] * N, mass_data['pb'],
            yerr=0.010954, fmt='|', capsize=3,
            ecolor='blue')
plt.legend(handler_map={lead: HandlerLine2D(numpoints=1)})

plt.title('Graph of the time to complete a period vs molar mass of an element')
plt.xlabel('Molar mass of a particular element in grams/mol (g/mol)')
plt.ylabel('Period of a complete pendulum swing in seconds (s)')
plt.show()

'''

End mass data section

'''

print('\n---------------------------------------------------------------------\n')

'''

Begin degree data section

'''

for key, values in degree_data.items():
    new_values = []
    for value in values:
        new_values.append(value / 5)
    degree_data.update({key: new_values})

for key, values in degree_data.items():
    print(('%s: ') % (key,), [round(value, 3) for value in values])

    average = sum(values) / 5
    print("AVG for %s: %f" % (key, round(average, 2)))

    summation = 0.0
    for value in values:
        summation += (value - average)**2
    std_dev = (summation / 4)**0.5

    print("STD DEV: %f" % std_dev)
    print("SDM: %f" % (std_dev / (5)**0.5))
    print()
    print("***************************************************")

##### Graph for degree data ######

# Ordered pairs
xi = np.array([5] * N + [10] * N + [15] * N + [20] * N + [25] * N + [30] * N + [35] * N + [40] * N + [45] * N)
y = degree_data['5_degrees'] + degree_data['10_degrees'] + \
    degree_data['15_degrees'] + degree_data['20_degrees'] + \
    degree_data['25_degrees'] + degree_data['30_degrees'] + \
    degree_data['35_degrees'] + degree_data['40_degrees'] + \
    degree_data['45_degrees']

# Set the dimensions for the axes.
plt.axis([3, 47, 1.46, 1.8])

# Std degree error
error = [
    0.011189, 0.016211, 0.025807,
    0.020513, 0.027763, 0.014724,
    0.025116, 0.027835, 0.026556
]

# Plot degree data points
for i in range(5, 46, 5):
    error_index = i // 5 - 1
    five_degs, = plt.plot([i] * N, degree_data['%d_degrees' % (i,)], 'ro', markersize=4)
    plt.errorbar([i] * N, degree_data['%d_degrees' % (i,)],
        yerr=error[error_index], fmt='|', capsize=3,
        ecolor='blue'
    )

plt.title('Graph of the time to complete a period vs pendulum offset angle')
plt.xlabel('Angle formed between the pendulm\'s start and rest positions (degrees)')
plt.ylabel('Period of a complete pendulum swing in seconds (s)')
plt.show()


'''

End degree data section

'''

print('\n---------------------------------------------------------------------\n')

'''

Begin Angle data section

'''

for key, values in length_data.items():
    new_values = []
    for value in values:
        new_values.append((value / 5)**2)
    length_data.update({key: new_values})

for key, values in length_data.items():
    print(('%s: ') % (key,), [round(value, 3) for value in values])

    average = sum(values) / 5
    print("AVG for %s: %f" % (key, round(average, 2)))

    summation = 0.0
    for value in values:
        summation += (value - average)**2
    std_dev = (summation / 4)**0.5

    print("STD DEV: %f" % std_dev)
    print("SDM: %f" % (std_dev / (5)**0.5))
    print()
    print("***************************************************")

# Ordered pairs
xi = np.array([20] * N + [30] * N + [40] * N + [50] * N + [60] * N + [70] * N)
y = length_data['20_cm'] + length_data['30_cm'] + \
    length_data['40_cm'] + length_data['50_cm'] + \
    length_data['60_cm'] + length_data['70_cm']

# Set the dimensions for the axes.
plt.axis([15, 75, 1.0, 2.9])

# Run a linear regression.
slope, intercept, r_value, p_value, std_err = stats.linregress(xi, y)
x = np.linspace(15, 75)  # span the graph
y = slope * x + intercept
plt.plot(x, y, label="Linear regression: y = %fx + %.2f" %
    (slope, intercept,))

# Standard length error
error = [
    0.011437, 0.007127, 0.015710,
    0.009209, 0.014043, 0.021790
]
# Plot length data
for i in range(20, 71, 10):
    error_index = (i - 10) // 10 - 1
    twenty, = plt.plot([i] * N, length_data['%d_cm' % (i,)],
                        'ro', markersize=4)
    plt.errorbar([i] * N, length_data['%d_cm' % (i,)],
        yerr=error[error_index], fmt='|', capsize=3,
        ecolor='red'
    )

plt.legend(handler_map={lead: HandlerLine2D(numpoints=1)})

plt.title('Graph of the square of a complete period time vs string length.')
plt.xlabel('Length of the pendulum string in centimeters (cm)')
plt.ylabel('Period of a complete pendulum swing in seconds squared (s^2)')
plt.show()

'''

End lendth data section

'''
