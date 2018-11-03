""" This script aims to calculate the probability of a muon to be at a point inside the drift chamber."""
from numpy import *
from scipy.integrate import *

def pdf_drift_point(P_x, P_y, D, L):
    D = float(D)
    L = float(L)
    P_x = float(P_x)
    P_y = float(P_y)
    Z_1 = -(L/2*(D/2-P_x) - P_y*(D/2-P_x))/(L/2 + P_y) + P_x
    Z_2 = (L/2*(D/2+P_x) - P_y*(D/2+P_x))/(L/2 + P_y) + P_x
    
	# In case the point is outside the chamber    
    if P_x > D/2.0 or P_x < - D/2.0:
        return 0.0
    if P_y == L/2.0 or P_y == -L/2.0:
    	return 0.0

	# For the  four different regions
    if P_x == 0 and P_y >= 0:
        event_number = Z_2-Z_1
    elif P_x == 0 and P_y < 0:
        event_number =D
    elif abs(P_y/P_x) >= L/D and P_y>0:
        event_number = Z_2-Z_1
    elif abs(P_y/P_x) <= L/D and P_x>0:
        event_number = D/2-Z_1
    elif abs(P_y/P_x) <= L/D and P_x<0:
        event_number = Z_2+D/2
    else:
        event_number = D
    
    return event_number
    
def pdf_drift_point_shift(P_x, P_y, D, L, shift):
	if P_x < -D/2.0 + shift:
		event_number = 0
	elif P_x < -D/2.0 + 2.0*shift:
		event_number = pdf_drift_point(P_x, P_y, D, L) + pdf_drift_point(-D + 2.0*shift - P_x, P_y, D, L)
	else:
		event_number = pdf_drift_point(P_x, P_y, D, L)
	
	return event_number

def pdf_drift_zone(min_height, max_height, D, L, shift):
    f = lambda x, y: pdf_drift_point_shift(x, y, D, L, shift)
    M = quad(lambda z : quad(lambda h : f(z, h), min_height, max_height)[0], -D/2.0, D/2.0)[0]
    
    return vectorize(lambda z : quad(lambda h: f(z,h), min_height, max_height)[0]/M)

def pdf_drift_model(min_height, max_height, D, L, shift):
    fmodel = pdf_drift_zone(min_height, max_height, D, L, shift)
    return lambda parameters, t : fmodel((t-parameters[0])*parameters[1])*parameters[1]







