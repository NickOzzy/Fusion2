import Yacora_KV_conversion as YC
import numpy as np

D_vals = ["5e18", "1e19", "2e19", "5e19", "1e20", "2e20"]
T_vals = [1, 1.5, 2, 3, 7, 10, 15, 20]
Types = ["H2", "H2p", "H3p", "HmHp", "HmH2p"]
NIST_As = {"n=3": 4.4114e7, "n=4": 8.4217e6, "n=5": 2.5311e6, "n=6": 9.7346e5, "n=7": 4.3901e5,
               "n=8": 2.3153e5, "n=9": 1.2159e5}  # data from NIST
Yac_mol_dict = {}
Yac_mol_dict_corrected = {} # use full n instead of ground state n.

for n in range(2,8):
    for D_val in D_vals:
        for T_val in T_vals:
            for type in Types:
                if type == "H2" or type == "H2p" or type == "H3p":
                    TiHmP, TiHpP = None, None
                else:
                    TiHmP, TiHpP = 2.2, T_val

                Yac_mol_dict["Type="+type+"n="+str(n)+"Den="+D_val+"T="+str(T_val)]=YC.TECPEC_Yacora(type, [n], [float(D_val)], [T_val], [TiHmP], [TiHpP])
                #Yac_mol_dict_corrected["Type="+type+"n="+str(n)+"Den="+D_val+"T="+str(T_val)]=YC.TECPEC_Yacora(type, [n], [float(D_val)], [T_val], [TiHmP], [TiHpP])/(1+)

print(Yac_mol_dict)
np.save("Yacora_molecule_PECs.npy", Yac_mol_dict)
