import matplotlib.pyplot as plt
import numpy as np
t_e = [0.1, 0.2, 0.5, 1, 2, 5, 10]
n_e = 2e18

nh2_rat = []
for t in t_e:
    nh2_rat.append(1.8911e20/(2e28*(t**1.4705)))

plt.plot(t_e, nh2_rat, "x")
plt.xscale("log")
plt.ylabel("density of H2")
plt.xlabel("Temp in eV")
plt.show()








