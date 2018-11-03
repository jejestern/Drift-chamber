### By Jennifer Studer

import numpy as np
import matplotlib.pyplot as plt

Channels = np.array([1, 2, 3, 4, 7, 8])
Townsend = np.array([76596.0, 61427.0, 62449.0, 69921.0, 63225.0, 45231.0])
Townerror = np.array([7170.0, 3560.0, 3537.0, 4737.0, 4122.0, 8403.0])
p_value = [0.869, 0.996, 0.998, 0.990, 0.639, 0.002]

Town_coeff = sum(Townsend/Townerror**2)/sum(1/Townerror**2)
Town_error = np.sqrt(1/sum(1/Townerror**2))

# Constant function at Town_coeff
Town = lambda x: Town_coeff + x*0
x_range = np.linspace(1, 8, 10)

plt.plot(x_range, Town(x_range), 'k', label="mean Townsend coefficient = (63562 +/- 1838) 1/m")
plt.plot(x_range, Town(x_range)+1838, 'k--', label="error of the mean Townsend coefficient")
plt.plot(x_range, Town(x_range)-1838, 'k--')
plt.errorbar(Channels, Townsend, yerr = Townerror, fmt = 'ro', label="Townsend coefficient of each channel")
plt.xlabel('Channel')
plt.ylabel('Townsendcoefficient [1/m]')
plt.grid(True)
plt.legend()
plt.title('Townsend coefficient')
plt.tight_layout()
plt.savefig("Townsend.png")
plt.clf()



print "The Townsend-coefficient is ", Town_coeff, "+/-", Town_error
