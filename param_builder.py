import processor as PR
import numpy as np

param_dict = {}
D_vals = ["5e18", "1e19", "2e19", "5e19", "1e20", "2e20"]
T_vals = [1, 1.5, 2, 3, 7, 10, 15, 20]

for D_val in D_vals:
    for T_val in T_vals:
        param_dict["Den="+D_val+"T="+str(T_val)+"H2p/H2"]=PR.get_H2plus_H2_ratio(float(D_val), T_val)
        param_dict["Den="+D_val+"T="+str(T_val)+"H3p/H2"]=PR.get_H3plus_H2_ratio(float(D_val), T_val)
        param_dict["Den="+D_val+"T="+str(T_val)+"Hm/H2"]=PR.get_Hminus_H2_ratio(float(D_val), T_val)

np.save("params.npy", param_dict)

print(param_dict["Den=5e18T=1H2p/H2"])
