import matplotlib.pyplot as plt
import numpy as np

import amjuel_tables as ajt



def get_H2plus_H2_ratio(ne, Te):
    ratio = (ajt.amjuel_tables('h2', "H2_3_2_3", ne, Te) + ajt.amjuel_tables('h4', "H4_2_2_9", ne, Te))\
            / (ajt.amjuel_tables('h4', "H4_2_2_14", ne, Te) + ajt.amjuel_tables('h4', "H4_2_2_11", ne, Te)
               + ajt.amjuel_tables('h4', "H4_2_2_12", ne, Te))
    return ratio

def get_H2plus_H2_from_single_poly(ne, Te):
    return ajt.amjuel_tables('h11', "H11_2_0c", ne, Te)

# returns the H2 density according to ** paper
def find_nh2(T):
   return(1.8911e20 / ((T ** 1.4705)))

def get_H3plus_H2_ratio(ne, Te):
    return ajt.amjuel_tables('h11', "H11_4_0a", ne, Te)




nes = [5e18, 1.5e20]
temps = np.logspace(0, 1.3, 100)
for ne in nes:
    ratios = []
    for temp in temps:
        ratios.append(get_H2plus_H2_ratio(ne, temp))
    plt.loglog(temps, ratios, "x")

for ne in nes:
    ratios = []
    for temp in temps:
        ratios.append(get_H2plus_H2_from_single_poly(ne, temp))
    plt.loglog(temps, ratios, "o")

# for ne in nes:
#     ratios = []
#     for temp in temps:
#         ratios.append(get_H3plus_H2_ratio(ne, temp))
#     print(ratios)
#     plt.loglog(temps, ratios, "o")
#
#
plt.xlabel("Temp in eV")
plt.ylabel("H2+/H2")
plt.show()







