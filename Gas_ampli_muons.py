# By Jennifer Studer
""" This python script aims to calculate the mean peak hight of the muon data as a function of the voltage difference between the anode and the cathode."""

import numpy as np
import matplotlib.pyplot as plt
from sys import argv, exit
import scipy.stats
from my_general_fit import * # written python file

# This part takes the argument and saves the folder 
if not len(argv) == 1:
    print("Wrong number of arguments!")
    print("Usage: python2 SelectDrift.py base_directory_name")
    print("Exiting...")
    exit()

# Voltage difference between the anode and the cathode
Vol = np.array([4000, 5000, 5500, 6000, 6500, 6800, 7000])
chn = 1

# Import the files with succeeded event numbers.
ev = []
ev.append(np.loadtxt("Drift_1000_1000/Drift_1000_1000_suc_drift_chn{}".format(chn)))
ev.append(np.loadtxt("Drift_2000_1000/Drift_2000_1000_suc_drift_chn{}".format(chn)))
ev.append(np.loadtxt("Drift_2500_1000/Drift_2500_1000_suc_drift_chn{}".format(chn)))
ev.append(np.loadtxt("Drift_3000_1000/Drift_3000_1000_suc_drift_chn{}".format(chn)))
ev.append(np.loadtxt("Drift_3500_1000/Drift_3500_1000_suc_drift_chn{}".format(chn)))
ev.append(np.loadtxt("Drift_3800_1000/Drift_3800_1000_suc_drift_chn{}".format(chn)))
ev.append(np.loadtxt("Drift_4000_1000/Drift_4000_1000_suc_drift_chn{}".format(chn)))

# Import the data
data = []
data.append(np.loadtxt("Drift_1000_1000/Drift_1000_1000_Data/Drift_1000_1000_chn{}_v".format(chn)))
data.append(np.loadtxt("Drift_2000_1000/Drift_2000_1000_Data/Drift_2000_1000_chn{}_v".format(chn)))
data.append(np.loadtxt("Drift_2500_1000/Drift_2500_1000_Data/Drift_2500_1000_chn{}_v".format(chn)))
data.append(np.loadtxt("Drift_3000_1000/Drift_3000_1000_Data/Drift_3000_1000_chn{}_v".format(chn)))
data.append(np.loadtxt("Drift_3500_1000/Drift_3500_1000_Data/Drift_3500_1000_chn{}_v".format(chn)))
data.append(np.loadtxt("Drift_3800_1000/Drift_3800_1000_Data/Drift_3800_1000_chn{}_v".format(chn)))
data.append(np.loadtxt("Drift_4000_1000/Drift_4000_1000_Data/Drift_4000_1000_chn{}_v".format(chn)))

# Preparing the fitting
r = 25*10**3
model_to_fit = lambda alpha, V: np.exp(r*alpha[0]*np.log(V) + alpha[1])
parameter_guess = [5*10**(-5), -10]

# Finding of the zero line and the sytematic error
zero_line = min(abs(data[0][int(9)]))
systematic = max(abs(data[0][int(9)].mean()-data[0][int(9)]))

peaks = []
yerror = []
for i in xrange(len(Vol)):
	goodvolt = []
	peak_heights = []
	for  event in ev[i][:]:
		peak = min(data[i][int(event)])
		peak_height = abs(peak - zero_line)
		peak_heights.append(peak_height)
	peak_heights = np.array(peak_heights)
	mean_peak = np.mean(peak_heights)
	yerror.append(scipy.stats.sem(peak_heights)+systematic)
	peaks.append(mean_peak)
peaks = np.array(peaks)
yerror = np.array(yerror)
Vol = np.array(Vol)

# Doing the fitting and plot it
townsend_ideal, townsend_error, townsend_p_value = general_fit(Vol, peaks, model_to_fit, parameter_guess, np.sqrt(2)*100, yerror)
fit_function = lambda V: model_to_fit(townsend_ideal, V)
x_range = np.linspace(4000, 7000, 1000)
plt.plot(x_range, fit_function(x_range), 'k--', label="Fit of the mean peak amplitudes")
print "The townsend coefficient with the muons is", townsend_ideal[0]*10**9, "+/-", townsend_error[0]*10**9, "1/nm"
print "The p_value of this fit is", townsend_p_value

# Plotting
plt.errorbar(Vol, peaks, xerr = np.sqrt(2)*100, yerr = yerror, fmt = 'go', label = "Mean peak heights")
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Voltage difference between anode and cathode log[V]')
plt.ylabel('Mean peak heights log[V]')
plt.grid(True)
plt.legend()
plt.title('Mean peak heights of the muons {}'.format(chn))
plt.tight_layout()
plt.savefig("Mean_peaks_muon_{}.png".format(chn))
plt.clf()

# The Residuals of the fit
residuals = []
for i in xrange(len(Vol)):
	residuals.append(peaks[i]-fit_function(Vol[i]))
residuals = np.array(residuals)

const = lambda x: 0*x
plt.plot(x_range, const(x_range), 'k', label="Constant zero function")
plt.errorbar(Vol, residuals, xerr = np.sqrt(2)*100, yerr = yerror, fmt='mx', label="Residuals of  the fit")
plt.xscale('log')
plt.xlabel('Voltage difference between anode and cathode log[V]')
plt.ylabel('Error of the fit [V]')
plt.grid(True)
plt.legend()
plt.title('Residuals of the fit for the muons of channel {}'.format(chn))
plt.tight_layout()
plt.savefig("Residuals_muon_{}.png".format(chn))
plt.clf()

