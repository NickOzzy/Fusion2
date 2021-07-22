import matplotlib.pyplot as plt
import numpy as np

import amjuel_tables as ajt



def get_H2plus_H2_ratio(ne, Te):
    ratio = (ajt.amjuel_tables('h2', "H2_3_2_3", ne, Te) + ajt.amjuel_tables('h4', "H4_2_2_9", ne, Te))\
            / (ajt.amjuel_tables('h4', "H4_2_2_14", ne, Te) + ajt.amjuel_tables('h4', "H4_2_2_11", ne, Te)
               + ajt.amjuel_tables('h4', "H4_2_2_12", ne, Te))
    return ratio


ne = 1e19
temps = np.logspace(0, 1.3, 100)
ratios = []
for temp in temps:
    ratios.append(get_H2plus_H2_ratio(ne, temp))
plt.loglog(temps, ratios, "x")
plt.xlabel("Temp in eV")
plt.ylabel("H2+/H2")
plt.show()




