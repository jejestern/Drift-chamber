""" The aim of this programm is to reconstruct the track of a muon flying throught our drift chamber."""

import numpy as np
import matplotlib.pyplot as plt
from sys import argv, exit
import os
import scipy.stats

# This part takes the argument and saves the folder 
if not len(argv) == 2:
    print("Wrong number of arguments!")
    print("Usage: python2 Track_Reconstruction.py base_directory_name")
    print("Exiting...")
    exit()

input_filename = argv[1]

# Constants etc.
D = 98.5 # Width (from wall to wall)
L = 104.0 # Height 
anode_dist = 4.2 # Distance from the anode to the wall

# An array which contains the information to know which events succeeded.
good = np.loadtxt(input_filename+"/"+input_filename+"_successes")

# Vertical 'height' on which electrons would go to one particular anode.
# Corresponds to each channel.
chn1_pos = 35
chn2_pos = 25
chn3_pos = 15
chn4_pos = 5
chn7_pos = -25
chn8_pos = -35

chn_pos = [chn1_pos, chn2_pos, chn3_pos, chn4_pos, chn7_pos, chn8_pos]

channels = [1,2,3,4,7,8] # The channels which are taken into account.
v_drift = np.loadtxt(input_filename+"/"+input_filename+"_drift_velocity_finalwitherror")

# Calculates the systematic error of v
sigma_t = 15*10**(-3)
v_syst = np.sqrt(2)*v_drift[0]**2*sigma_t/D

# Define a function which calculates the systematic error of x
def systematic_error_x(x, v, D):
	sigma_t = 15*10**(-3)
	return np.sqrt(2)*v*sigma_t*np.sqrt(x**2/D**2 +1)

# Loading the datas from the channels.
print "Starting to load the arrays from the channels."
voltage = []
time = []
for i in xrange(len(channels)):
	print "Loading channel", channels[i], " "
	volt = np.loadtxt(input_filename+"/"+input_filename+"_Data/"+input_filename+"_chn{}_v".format(channels[i]))
	tim = np.loadtxt(input_filename+"/"+input_filename+"_Data/"+input_filename+"_chn{}_t".format(channels[i]))
	voltage.append(volt)
	time.append(tim)

for event in good:
	t = [] # Starting point of the drops of each channel for you event.
	x_pos = []
	x_stat = []
	x_syst = []
	
	for i in xrange(len(channels)):
		# Finding the start time of the drop
		print "Calculates the drop points of your event"
		peak_height = min(voltage[i][int(event)])
		peak = np.where(voltage[i][int(event)] == peak_height)[0][0]
		drop_point = np.where(voltage[i][int(event)][:int(peak)] >= -max(abs(voltage[i][int(event)][:40])))[0][-1]
		t.append(time[i][int(event)][drop_point])

		# Calculation of the track
		x_pos.append(v_drift[0]*time[i][int(event)][drop_point])
		x_stat.append((v_drift[1]-v_syst)*time[i][int(event)][drop_point])
		x_syst.append(systematic_error_x(v_drift[0]*time[i][int(event)][drop_point], v_drift[0], D))

	# Plotting of the track
	chn_pos = np.array(chn_pos)
	x_pos = np.array(x_pos)
	x_stat = np.array(x_stat)
	x_syst = np.array(x_syst)
	x_err = x_stat+x_syst
	plt.errorbar(x_pos, chn_pos, xerr = x_err, yerr = 5, color = 'red', marker = 'x', linestyle = '', label = "Track of the muon", capsize=4)
	plt.xlim(0, 94.3)
	plt.xlabel('Location inside the chamber from anode to cathode [mm]')
	plt.ylabel('Height of the chamber [mm]')
	plt.title('Muon tracking of event {}'.format(int(event)))
	plt.legend()
	plt.grid(True)
	plt.savefig("Track/"+input_filename+"/event_{}.png".format(int(event)))
	plt.clf()



