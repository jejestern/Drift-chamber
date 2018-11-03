""" This script plots the probability distribution of the muons for each channel."""
from numpy import *
import matplotlib.pyplot as plt
from pdf_drift import pdf_drift_zone

D = 98.5
L = 104.0
anode_pos = 4.2

chn1_zone = [30., 52.]
chn2_zone = [20., 30.]
chn3_zone = [10., 20.]
chn4_zone = [0.0, 10.]
#chn5_zone = [-10., 0.0]
#chn6_zone = [-20., -10.]
chn7_zone = [-30., -20.]
chn8_zone = [-52., -30.]

zones = [chn1_zone, chn2_zone, chn3_zone, chn4_zone, chn7_zone, chn8_zone]
channels = [1, 2, 3, 4, 7, 8]

x = linspace(-D/2.0, D/2.0, 1000)

for i in xrange(len(channels)):
	pdf_model = pdf_drift_zone(zones[i][0], zones[i][1], D, L, anode_pos)
	plt.plot(x, pdf_model(x), label = 'Zone of channel {}'.format(channels[i]) + ', from ' + str(zones[i][0]) + 'mm to ' + str(zones[i][1]) + 'mm')
plt.xlabel('Horizontal position [mm]')
plt.ylabel('Vertical position [mm]')
plt.title('Probability distribution for a muons posistion\ninside a drift chamber of height 104 mm and width 98.5 mm,\nwith the origin in the middle of the chamber')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('pdf.png')
plt.clf()


