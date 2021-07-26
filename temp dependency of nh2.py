import matplotlib.pyplot as plt
import numpy as np
t_e = np.logspace(0, 1.3, 100)
n_e = 2e18

nh2 = []
for t in t_e:
    nh2.append(1.8911e20/((t**1.4705)))

plt.plot(t_e, nh2, "x")
plt.xscale("log")
plt.ylabel("density of H2")
plt.xlabel("Temp in eV")
plt.show()








