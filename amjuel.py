#reproducing crude version of reaction 2.0c Amjuel

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

def calc(x):
      total = 0
      for i, k in enumerate(ks):
            total = total + (k * (np.log(x)**i))
      return total


ks = [-5.281428900665, 3.115995571855, -3.690629726865, 1.448918180601, -0.3928689243481,
      0.1236809448625, -0.02877121006548, 0.003391113110854, -0.0001521565312043]

temps = np.linspace(1, 20, 20)

ratios = []

for T in temps:
      ratios.append(np.exp(calc(T)))

print(ratios)

plt.loglog(temps, ratios, "-")

plt.show()
#okok