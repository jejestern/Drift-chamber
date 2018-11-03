# By Jennifer Studer
"""This programm has the aim to seperate the data into useful data and unusful data. It will creat a new folder for each of them and show their plots. Additionally we will creat two text files one for the failures and one for the succeeded data takings. In each we will save the event number of the belonging events. 
We will ignore channels 5 and 6, since we saw that they do not work anymore."""

import numpy as np
import matplotlib.pyplot as plt
from sys import argv, exit, stdout
import os

# This part takes the argument and saves the folder 
if not len(argv) == 2:
    print("Wrong number of arguments!")
    print("Usage: python2 SelectDrift.py base_directory_name")
    print("Exiting...")
    exit()

input_filename = argv[1]

def clear_directory(folder_name):
    """Clears the given directory of any files, but not of any subdirectories"""
    for the_file in os.listdir(folder_name):
        file_path = os.path.join(folder_name, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

if not os.path.exists(input_filename+"_Suc_Drift"):
    os.makedirs(input_filename+"_Suc_Drift")
clear_directory(input_filename+"_Suc_Drift")

# Preparation of the arrays which will contain the datas afterwards.
voltages = []
times = []
channels = [1,2,3,4,7,8] # The channels which are taken into account.

# Loading the datas from channel 1.
print "Starting to load the arrays from the channels."
for i in channels:
	print "Loading channel", i, " "
	volt = np.loadtxt(input_filename+"/"+input_filename+"_Data/"+input_filename+"_chn{}_v".format(i))
	tim = np.loadtxt(input_filename+"/"+input_filename+"_Data/"+input_filename+"_chn{}_t".format(i))
	voltages.append(volt)
	times.append(tim)

### Selection starts:
print "Selection of the signals in progress..."
events = voltages[0].shape[0] #Number of events

for i in xrange(len(channels)):
	print "Selection on channel", channels[i]
	# Saving all failures and all successes
	successes = open(input_filename+'_suc_drift_chn{}'.format(channels[i]), 'w')
	failures = open(input_filename+'_fail_drift_chn{}'.format(channels[i]), 'w')
	for x in xrange(events):
		starting_noise = -max(abs(voltages[i][x][:40]))
		if min(voltages[i][x])<= starting_noise*10 and min(voltages[i][x])>=-0.499: 
			plt.plot(times[i][x], voltages[i][x])
			successes.write(str(x)+' ')
		else:
			failures.write(str(x)+' ')
	plt.ylim(bottom=-0.6)
	plt.savefig(input_filename+"_Suc_Drift/chn{}.png".format(channels[i]))
	plt.clf()
	successes.close()
	failures.close()

print "The programm has finished his work."







