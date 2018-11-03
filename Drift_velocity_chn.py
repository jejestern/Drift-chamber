"""This programm will create a histogram on which the different flight times of the succeeded events to a point T are plotted. From this it will extract the flight time from the cathode to the anode and finally calculate the drift velocity."""

import numpy as np
import matplotlib.pyplot as plt
from sys import argv, exit
import os
import scipy.stats
from my_general_fit import * # written python file
from pdf_drift import * # written python file

# This part takes the argument and saves the folder 
if not len(argv) == 2:
    print("Wrong number of arguments!")
    print("Usage: python2 Drift_velocity_chn.py base_directory_name")
    print("Exiting...")
    exit()

input_filename = argv[1]

# Preparation of the arrays which will contain the datas afterwards.
channels = [1,2,3,4,7,8] # The channels which are taken into account.

# Constants etc.
D = 98.5 # Width (from wall to wall)
L = 104.0 # Height 
anode_dist = 4.2 # Distance from the anode to the wall

# Vertical 'height' on which electrons would go to one particular anode.
# Corresponds to each channel.
chn1_zone = [30, 52]
chn2_zone = [20, 30]
chn3_zone = [10, 20]
chn4_zone = [0.0, 10]
chn5_zone = [-10, 0.0]
chn6_zone = [-20, -10]
chn7_zone = [-30, -20]
chn8_zone = [-52, -30]

chn_zones = [chn1_zone, chn2_zone, chn3_zone, chn4_zone, chn5_zone, chn6_zone, chn7_zone, chn8_zone]

# An array for the drift velocities and one for the statistical errors
drifts = open(input_filename+"/"+input_filename+'_drift_velocity', 'w')
drifts_stat = open(input_filename+"/"+input_filename+'_drift_velocity_error', 'w')
v_wmean_numerator = 0
v_wmean_denominator = 0
v_stat_denominator = 0

# Define a function which calculates the systematic error in dependency of v
def systematic_error(v, D):
	sigma_t = 15*10**(-3)
	return np.sqrt(2)*v**2*sigma_t/D

# An array which contains the information to know which events succeeded.
good = np.loadtxt(input_filename+"/"+input_filename+"_successes")

# Loading the datas from the channels.
print "Starting to load the arrays from the channels."
for i in xrange(len(channels)):
	pulls = []
	print "Loading channel", channels[i], " "
	volt = np.loadtxt(input_filename+"/"+input_filename+"_Data/"+input_filename+"_chn{}_v".format(channels[i]))
	tim = np.loadtxt(input_filename+"/"+input_filename+"_Data/"+input_filename+"_chn{}_t".format(channels[i]))
	
	# Finding the start time of the drop
	print "Calculates the drop point"
	for event in good:
		peak_height = min(volt[int(event)])
		peak = np.where(volt[int(event)] == peak_height)[0][0]
		drop_point = np.where(volt[int(event)][:int(peak)] >= -max(abs(volt[int(event)][:40])))[0][-1]
		pulls.append(tim[int(event)][drop_point])

	pulls=np.array(pulls)
	print "Creating the histogramms"
	min_zone = chn_zones[i][0]
        max_zone = chn_zones[i][1]
	model_to_fit = pdf_drift_model(min_zone, max_zone, D, L, anode_dist)
	parameter_guess = [3000.0/2.0, D/3000.0]
        model_linestyle = ':'
        model_marker = ''
        model_label = "Fit for the area covered by the channel"
        model_color = 'r'

	# Plotting histogram, and computing the centers and standard deviations for each bin.
	bin_heights, bin_borders, _  = plt.hist(pulls, bins=10, density = True, label='number of events starting at t')
	height = []
    	bin_heights_mean_center = []
    	bin_heights_std_center = []
    	N = bin_heights.shape[0]
    	for j in xrange(N):
        	if j != N - 1:
            		data_values = pulls[np.where( (pulls >= bin_borders[j]) & (pulls < bin_borders[j+1]))[0]]
        	else:
            		data_values = pulls[np.where( (pulls >= bin_borders[j]) & (pulls <= bin_borders[j+1]))[0]]
            		
		if data_values.shape[0] == 1 or data_values.shape[0] == 0:
			print "In this bean there is only one event, this means the probablity goes to infinity."
			print "We cannot work with this, so we will not take this event into account."
		else:
			height.append(bin_heights[j])
			bin_heights_mean_center.append(data_values.mean())
        		bin_heights_std_center.append(scipy.stats.sem(data_values))
        		
        height = np.array(height)
        bin_heights_mean_center = np.array(bin_heights_mean_center)
    	bin_heights_std_center = np.array(bin_heights_std_center)
    	
    	# Plotting the means, as well as their error
    	plt.errorbar(bin_heights_mean_center, height, xerr = bin_heights_std_center, color = 'red', marker = 'x', linestyle = '', label = "Mean of each bin", capsize=5)

    	# Doing the fit        	
        parameter_ideal, parameter_error, parameter_p_value= general_fit(bin_heights_mean_center, height, model_to_fit, parameter_guess, x_err = bin_heights_std_center)
        
        # Preparing to plot the fit
        fit_function = lambda x : model_to_fit(parameter_ideal, x)
        start = min(pulls)
        end = max(pulls)
        x_range = np.linspace(start, end, 1000)
        plt.plot(x_range, fit_function(x_range), linestyle = model_linestyle, color = model_color, marker = model_marker, label = model_label)
        plt.xlim(start, end)
        plt.ylim(0.0, 1.1*max(bin_heights))

	plt.xlabel('Time [ns]')
	plt.ylabel('counts')
	plt.legend()
	plt.savefig(input_filename+"/"+input_filename+"_Histo_chn{}.png".format(channels[i]))
	plt.clf()
	
	# We caluculate the drift velocity for each channel
	drift_syst = systematic_error(parameter_ideal[1], D)
        print "Drift velocity of channel", channels[i], "is (", parameter_ideal[1], ",", parameter_error[1]+drift_syst, ")"
        drifts.write(str(parameter_ideal[1])+' ')
        drifts_stat.write(str(parameter_error[1]+drift_syst)+' ')
        v_wmean_numerator += parameter_ideal[1]/(parameter_error[1])**2
        v_wmean_denominator += 1/(parameter_error[1])**2
        v_stat_denominator += 1/(parameter_error[1])**2
        
drifts.close()
drifts_stat.close()

# Calculation of the drift velocity at this voltage 
v_wmean = v_wmean_numerator/v_wmean_denominator
v_stat = 1/v_stat_denominator
v_syst = systematic_error(v_wmean, D)
print "The mean drift velocity at this voltage is (", v_wmean,"+/-", v_stat + v_syst, ")"
velocity = open(input_filename+"/"+input_filename+'_drift_velocity_finalwitherror', 'w')
velocity.write(str(v_wmean)+' ')
velocity.write(str(v_stat + v_syst)+' ')
velocity.close()

print "The programm has finished his work."


