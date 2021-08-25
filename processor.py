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

def find_nh2ii(T):
    return(2e18 / (T ** 1.7))

def get_H3plus_H2_ratio(ne, Te):
    return ajt.amjuel_tables('h11', "H11_4_0a", ne, Te)

def get_Hminus_H2_ratio(ne, Te):
    return ajt.amjuel_tables('h11', "H11_7_0a", ne, Te)

def h2plush2_from_h12(ne, Te):
    return ajt.amjuel_tables('h12', "H12_2_0c", ne, Te)


print(h2plush2_from_h12(1e20, 20))
print(get_H2plus_H2_ratio(1e20, 20))

# t = np.arange(1, 1000)
# n1 = find_nh2(t)
# n2 = find_nh2ii(t)
# plt.loglog(t, n1)
# plt.loglog(t, n2)
# plt.show()



#print(get_H2plus_H2_ratio(5,5e19)*find_nh2(2))
# get nH-
# temps = [1, 1.5, 2, 3, 7, 10, 15, 20]
# nhminuses = []
# for temp in temps:
#     nhminuses.append(get_Hminus_H2_ratio(2e19, temp)*find_nh2(temp))
#     print("Temp="+str(temp)+": Density H-="+str(nhminuses[-1])+" nh2="+str(find_nh2(temp))
#           +"; nh2+="+str(get_H2plus_H2_ratio(2e19, temp)*find_nh2(temp))
#           +"; nh3+="+str(get_H3plus_H2_ratio(2e19, temp)*
#                          get_H2plus_H2_ratio(2e19, temp)*(find_nh2(temp)**2)/2e19))
# plt.loglog(temps, nhminuses, "x")
# plt.xlabel("Temp in eV")
# plt.ylabel("H- denisty")
# plt.show()






# nes = [5e18, 1.5e20]
# temps = np.logspace(0, 1.3, 100)
# for ne in nes:
#     ratios = []
#     for temp in temps:
#         ratios.append(get_H2plus_H2_ratio(ne, temp))
#     plt.loglog(temps, ratios, "x")
#
# for ne in nes:
#     ratios = []
#     for temp in temps:
#         ratios.append(get_H2plus_H2_from_single_poly(ne, temp))
#     plt.loglog(temps, ratios, "o")
#
# for ne in nes:
#     ratios = []
#     for temp in temps:
#         ratios.append(get_H3plus_H2_ratio(ne, temp))
#     print(ratios)
#     plt.loglog(temps, ratios, "o")
#
# for ne in nes:
#     ratios = []
#     for temp in temps:
#         ratios.append(get_Hminus_H2_ratio(ne, temp))
#     print(ratios)
#     plt.loglog(temps, ratios, "o")
#
#
# plt.xlabel("Temp in eV")
# plt.ylabel("H2+/H2")
# plt.show()







