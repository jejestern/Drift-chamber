# By Jennifer Studer
""" This python script aims to calculate the mean peak hight of the Strontium data as a function of the voltage difference between the anode and the cathode."""

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
Vol = np.array([6000, 6200, 6400, 6500, 6700, 6900, 7000, 7100, 6900, 7000, 7100])

# Import the files with succeeded event numbers.
ev = []
ev.append(np.loadtxt("Strontium_2000_500/Strontium_2000_500_successes"))
ev.append(np.loadtxt("Strontium_2200_250/Strontium_2200_250_successes"))
ev.append(np.loadtxt("Strontium_2400_250/Strontium_2400_250_successes"))
ev.append(np.loadtxt("Strontium_2500_400/Strontium_2500_400_successes"))
ev.append(np.loadtxt("Strontium_2700_500/Strontium_2700_500_successes"))
ev.append(np.loadtxt("Strontium_2900_500_1100mbar/Strontium_2900_500_1100mbar_successes"))
ev.append(np.loadtxt("Strontium_3000_500_1100mbar/Strontium_3000_500_1100mbar_successes"))
ev.append(np.loadtxt("Strontium_3100_1000_1100mbar/Strontium_3100_1000_1100mbar_successes"))
ev.append(np.loadtxt("Strontium_2900_500_1140mbar/Strontium_2900_500_1140mbar_successes"))
ev.append(np.loadtxt("Strontium_3000_500_1140mbar/Strontium_3000_500_1140mbar_successes"))
ev.append(np.loadtxt("Strontium_3100_500_1140mbar/Strontium_3100_500_1140mbar_successes"))

# Import the data
data = []
data.append(np.loadtxt("Strontium_2000_500/Strontium_2000_500_Data/Strontium_2000_500_chn1_v"))
data.append(np.loadtxt("Strontium_2200_250/Strontium_2200_250_Data/Strontium_2200_250_chn1_v"))
data.append(np.loadtxt("Strontium_2400_250/Strontium_2400_250_Data/Strontium_2400_250_chn1_v"))
data.append(np.loadtxt("Strontium_2500_400/Strontium_2500_400_Data/Strontium_2500_400_chn1_v"))
data.append(np.loadtxt("Strontium_2700_500/Strontium_2700_500_Data/Strontium_2700_500_chn1_v"))
data.append(np.loadtxt("Strontium_2900_500_1100mbar/Strontium_2900_500_1100mbar_Data/Strontium_2900_500_1100mbar_chn1_v"))
data.append(np.loadtxt("Strontium_3000_500_1100mbar/Strontium_3000_500_1100mbar_Data/Strontium_3000_500_1100mbar_chn1_v"))
data.append(np.loadtxt("Strontium_3100_1000_1100mbar/Strontium_3100_1000_1100mbar_Data/Strontium_3100_1000_1100mbar_chn1_v"))
data.append(np.loadtxt("Strontium_2900_500_1140mbar/Strontium_2900_500_1140mbar_Data/Strontium_2900_500_1140mbar_chn1_v"))
data.append(np.loadtxt("Strontium_3000_500_1140mbar/Strontium_3000_500_1140mbar_Data/Strontium_3000_500_1140mbar_chn1_v"))
data.append(np.loadtxt("Strontium_3100_500_1140mbar/Strontium_3100_500_1140mbar_Data/Strontium_3100_500_1140mbar_chn1_v"))

# Preparing the fitting
r = 25*10**3
model_to_fit = lambda alpha, V: np.exp(r*alpha[0]*np.log(V) + alpha[1])
parameter_guess = [5*10**(-5), -10]

# Finding of the zero line and the sytematic error
syst = np.loadtxt("Drift_1000_1000_chn1_v")
zero_line = min(abs(syst[int(9)]))
systematic = max(abs(syst[int(9)].mean()-syst[int(9)]))

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
townsend_ideal, townsend_error, townsend_p_value = general_fit(Vol[2:5], peaks[2:5], model_to_fit, parameter_guess, np.sqrt(2)*100, yerror[2:5])
fit_function = lambda V: model_to_fit(townsend_ideal, V)
x_range = np.linspace(6000, 7100, 1000)
plt.plot(x_range, fit_function(x_range), 'k--', label="Fit of the points\nat 6.4, 6.5 and 6.7 kV")
print "The townsend coefficient of the 3 point fit is", townsend_ideal[0]*10**9, "+/-", townsend_error[0]*10**9, "1/nm"
print "The p_value of this fit is", townsend_p_value

townsend_ideal2, townsend_error2, townsend_p_value2 = general_fit(Vol[:2], peaks[:2], model_to_fit, parameter_guess, np.sqrt(2)*100, yerror[:2])
fit_function2 = lambda V: model_to_fit(townsend_ideal2, V)
plt.plot(x_range, fit_function2(x_range), 'k:', label="Fit of the points\nat 6.0 and 6.2 kV")
print "The townsend coefficient of the 2 point fit is", townsend_ideal2[0]*10**9, "+/-", townsend_error2[0]*10**9, "1/nm"
print "The p_value of this fit is", townsend_p_value2

# Plotting
plt.errorbar(Vol[:5], peaks[:5], xerr = np.sqrt(2)*100, yerr = yerror[:5], fmt = 'go', label = "Mean peak heights\nfor pressure\nbetween 1100-1140 mbar")
plt.errorbar(Vol[5:8], peaks[5:8], xerr = np.sqrt(2)*100, yerr= yerror[5:8], fmt='ro', label="Mean peak heights\nfor pressure 1100 mbar")
plt.errorbar(Vol[8:], peaks[8:], xerr= np.sqrt(2)*100, yerr= yerror[8:], fmt='bo', label = "Mean peak heights\nfor pressure 1140 mbar")
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Voltage difference between anode and cathode log[V]')
plt.ylabel('Mean peak heights log[V]')
plt.grid(True)
plt.legend()
plt.title('Mean peak heights of Strontium')
plt.tight_layout()
plt.savefig("Mean_peaks.png")
plt.clf()

# The Residuals of the fit
residuals = []
residuals2 = []
for i in xrange(len(Vol)):
	residuals.append(peaks[i]-fit_function(Vol[i]))
	residuals2.append(peaks[i]-fit_function2(Vol[i]))
residuals = np.array(residuals)
residuals2 = np.array(residuals2)

const = lambda x: 0*x
plt.plot(x_range, const(x_range), 'k', label="Constant zero function")
plt.errorbar(Vol, residuals, xerr = np.sqrt(2)*100, yerr = yerror, fmt='mx', label="Residuals of  the\nfit of the points\nat 6.4, 6.5 and 6.7 kV")
plt.errorbar(Vol, residuals2, xerr = np.sqrt(2)*100, yerr = yerror, fmt='yx', label="Residuals of the\nfit of the points\nat 6.0 and 6.2 kV")
plt.xscale('log')
plt.xlabel('Voltage difference between anode and cathode log[V]')
plt.ylabel('Error of the fits [V]')
plt.grid(True)
plt.legend()
plt.title('Residuals of the fit for Strontium')
plt.tight_layout()
plt.savefig("Residuals.png")
plt.clf()







