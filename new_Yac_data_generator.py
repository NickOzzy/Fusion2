import numpy as np

D_vals = ["5e18", "1e19", "2e19", "5e19", "1e20", "2e20"]
T_vals = [1, 1.5, 2, 3, 7, 10, 15, 20]
Yacora_Exc_PEC_dict = {}

for n in range(2,8,1):
    for T in T_vals:
        for i, D in enumerate(D_vals):
            Yacora_Exc_PEC_dict["n="+str(n)+"Den="+D+"T="+str(T)] = np.genfromtxt("ExcT"+str(T)+"n"+str(n)+".dat", skip_header=27+i, skip_footer=5-i, usecols=(1))


