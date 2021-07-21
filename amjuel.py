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

temps = [0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]

ratios = []

for T in temps:
      ratios.append(np.exp(calc(T)))

print(ratios)
smooth = interp1d(temps, ratios, kind="cubic")
tempsnew = np.linspace(0.5, 1000, 100)
plt.loglog(tempsnew, smooth(tempsnew), "-")

plt.show()
#yeah