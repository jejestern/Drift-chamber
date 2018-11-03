### By Jennifer Studer
""" This script aims to write a function which creates a fit for 
a given modell"""

from numpy import *
from scipy.odr import *
from scipy.stats import t, chi2, kstwobign

def cdf(Y_ord_data, Y_ord_model):
    """ Function which calculates the cdf. Copied from 
		https://www.astro.rug.nl/software/kapteyn/kmpfittutorial.html"""
    cdfnew = []
    n = Y_ord_model.shape[0]
    for yy in Y_ord_data:
        fr = len(where(Y_ord_model <= yy)[0])/float(n)
        cdfnew.append(fr)
    return asarray(cdfnew)

def general_fit(x, y, model_to_fit, initial_guess, x_err = None, y_err = None):
	""" x, y are the data which we want to fit.
		The model_to_fit has the following form: 
		model_to_fit = lambda parameter, data: parameter[0]*data + parameter[1],
		and the parameter is a list.
		The initial guess for the parameters is initial_guess = [a, b]"""
	
	# Save the model in the needed form	
	odr_model = Model(model_to_fit)
	
	# Save the data with errors if given in the needed form
	if (y_err is None) and (x_err is None):
		odr_data = RealData(x, y)
	elif x_err is None:
		odr_data = RealData(x, y, sy = y_err)
	elif y_err is None:
		odr_data = RealData(x, y, sx = x_err)
	else:
		odr_data = RealData(x, y, sx = x_err, sy = y_err)
	
	# This value tells the number of data points - degrees of freedom
	degrees_of_freedom = x.shape[0] - len(initial_guess)
	
	myodr = ODR(odr_data, odr_model, beta0 = initial_guess)
	
	# Runs the fitting and saves the found parameters and there errors
	odr_output = myodr.run()
	odr_parameter_ideal = odr_output.beta
	odr_parameter_error = odr_output.sd_beta
	
	### This part is to calculate the p-value of the fit and for this we 
	### need first to calculate chi2
	
	if y_err is None:
		# We make a distinguish between the general case and if yerr=None, 
		# there we need to use a different test which is called the 
		# Kolmogorov-Smirnov test.
		
		# We compute the cdf
		N = y.shape[0]
		z = sort(y)
		cdf_data_high = arange(1.0, N+1.0)/N
		cdf_data_low = arange(0.0, 1.0*N)/N
		X = linspace(min(x), max(x), 300)
		fitted_values = model_to_fit(odr_parameter_ideal, X)
		fitted_values.sort()
		cdf_fitted = cdf(z, fitted_values)
    	
    		# Find biggest distance between cumulative functions
		DD = cdf_data_high - cdf_fitted
        	Dip = DD.argmax()
        	Dplus = DD[Dip]
        	DD = cdf_fitted - cdf_data_lo
        	Dim = DD.argmax()
        	Dmin = DD[Dim]
        	if Dplus >= Dmin:
			Di = Dip
		else:
			Di = Dim
        	Dmax = max(Dplus, Dmin)

        	rv = kstwobign()

        	odr_p_value = 1.0 - rv.cdf(Dmax)

	else:
		# This is for the general case.
		chi_squarred = sum((y - model_to_fit(odr_parameter_ideal, x))**2/y_err**2)
		odr_p_value = 1.0 - chi2.cdf(chi_squarred, degrees_of_freedom)

	return odr_parameter_ideal, odr_parameter_error, odr_p_value
    
