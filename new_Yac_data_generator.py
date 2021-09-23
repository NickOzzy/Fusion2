import numpy as np

D_vals = ["5e18", "1e19", "2e19", "5e19", "1e20", "2e20"]
T_vals = [1, 1.5, 2, 3, 7, 10, 15, 20]
NIST_As = {"n=2": 4.6999e8, "n=3": 4.4114e7, "n=4": 8.4217e6, "n=5": 2.5311e6, "n=6": 9.7346e5, "n=7": 4.3901e5,
               "n=8": 2.3153e5, "n=9": 1.2159e5}  # data from NIST, note "n=2" is the lyman alpha coefficient.

Yacora_Exc_PEC_dict = {}
Yacora_Rec_PEC_dict = {}

for n in range(3,8,1):
    for T in T_vals:
        if T == 1.5:
            T = "1point5"
        for i, D in enumerate(D_vals):
            Yacora_Exc_PEC_dict["n="+str(n)+"Den="+D+"T="+str(T)] = np.genfromtxt("Data_files/ExcT"+str(T)+"n"+str(n)
                                                                                  +".dat", skip_header=27+i, skip_footer=5-i, usecols=(1))*NIST_As["n="+str(n)]
            Yacora_Rec_PEC_dict["n="+str(n)+"Den+"+D+"T="+str(T)] = np.genfromtxt("Data_files/RecombT"+str(T)+"n"+str(n)
                                                                                  +".dat", skip_header=27+i, skip_footer=5-i, usecols=(1))*NIST_As["n="+str(n)]

print(Yacora_Exc_PEC_dict)
print(Yacora_Rec_PEC_dict)

np.save("updated_YAC_Exc_PECs.npy", Yacora_Exc_PEC_dict)
np.save("updated_YAC_Rec_PECs.npy", Yacora_Rec_PEC_dict)
