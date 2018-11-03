# By Jennifer Studer
"""This programm has the aim to seperate the data into useful data and unusful datas. It will creat a new folder for each of them and show their plots. Additionally we will creat two text files one for the failures and one for the succeeded data takings. In each we will save the event number of the belonging events. 
We will ignore channels 5 and 6, since we saw that they do not work anymore."""

import numpy as np
import matplotlib.pyplot as plt
from sys import argv, exit
import os

# This part takes the argument and saves the folder 
if not len(argv) == 2:
    print("Wrong number of arguments!")
    print("Usage: python2 Select_Drift.py base_directory_name")
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

if not os.path.exists(input_filename+'/'+input_filename+"_Success"):
    os.makedirs(input_filename+'/'+input_filename+"_Success")
if not os.path.exists(input_filename+'/'+input_filename+"_Failure"):
    os.makedirs(input_filename+'/'+input_filename+"_Failure")
clear_directory(input_filename+'/'+input_filename+"_Success")
clear_directory(input_filename+'/'+input_filename+"_Failure")

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

# Saving all failures and all successes
successes = open(input_filename+'/'+input_filename+'_successes', 'w')
failures = open(input_filename+'/'+input_filename+'_failures', 'w')

for x in xrange(events):
	fail = 0
	for i in xrange(len(channels)):
		plt.plot(times[i][x], voltages[i][x], label="Signal of channel {}".format(channels[i]))
		plt.ylim(bottom=-0.6)
		plt.xlabel('time [s]')
		plt.ylabel('Voltage [V]')
		plt.legend()
		starting_noise = -max(abs(voltages[i][x][:40]))
		if min(voltages[i][x])<=-0.499: # If the voltage goes below -0.5V it is extracted.
			fail = 0
		elif min(voltages[i][x])<= starting_noise*5: 
			fail += 1
		else:
			fail = 0
		
	if fail == len(channels):
		plt.savefig(input_filename+'/'+input_filename+"_Success/event{}.png".format(x+1))
		successes.write(str(x)+' ')
	else:
		plt.savefig(input_filename+'/'+input_filename+"_Failure/event{}.png".format(x+1))
		failures.write(str(x)+' ')

	plt.clf()
successes.close()
failures.close()

print "The programm has finished his work."







