""" The aim of this file is to create a plot with the drift_velocities of the channels for all voltages and the weithed mean drift velocity for all voltages (everything with their errorbars)."""

import numpy as np
import matplotlib.pyplot as plt
from sys import argv, exit

# This part takes the argument and saves the folder 
if not len(argv) == 1:
    print("Wrong number of arguments!")
    print("Usage: python2 SelectDrift.py base_directory_name")
    print("Exiting...")
    exit()

# Loading all drift_velocities from all channels and all voltages and with their weithed mean and its beloning errors
voltages = [1000, 2000, 2500, 3000, 3500, 3800, 4000]
drift_channels = []
error_channels = []
velocity = []
for vol in xrange(len(voltages)):
	drift_channels.append(np.loadtxt("Drift_{}_1000/Drift_{}_1000_drift_velocity".format(voltages[vol], voltages[vol])))
	error_channels.append(np.loadtxt("Drift_{}_1000/Drift_{}_1000_drift_velocity_error".format(voltages[vol], voltages[vol])))
	velocity.append(np.loadtxt("Drift_{}_1000/Drift_{}_1000_drift_velocity_finalwitherror".format(voltages[vol], voltages[vol])))
	channel_color = ['m', 'b', 'g', 'y', 'k', 'c']
	channel_label = ["Channel 1", "Channel 2", "Channel 3", "Channel 4", "Channel 7", "Channel 8",]

	# Plotting
	for i in range(6):
		plt.errorbar(voltages[vol], 10**6*drift_channels[vol][i], xerr = 100, yerr = 10**6*error_channels[vol][i], color = channel_color[i], marker = 'x', linestyle = '', label = channel_label[i], capsize=5)
	plt.errorbar(voltages[vol], 10**6*velocity[vol][0], xerr = 100, yerr = 10**6*velocity[vol][1], color = 'r', marker= 'o', linestyle = '', label = "Weighted mean drift velocity", capsize=6)

plt.xlabel('Cathode voltage V [V]')
plt.ylabel('Drift velocity v [m/s]')
plt.title('Drift velocities')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig('Drift_velocities.png')
plt.clf()

