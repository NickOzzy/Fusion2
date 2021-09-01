import Yacora_KV_conversion as YC
import numpy as np

D_vals = ["5e18", "1e19", "2e19", "5e19", "1e20", "2e20"]
T_vals = [1, 1.5, 2, 3, 7, 10, 15, 20]
Types = ["H2", "H2p", "H3p", "HmHp", "HmH2p"]
Yac_mol_dict = {}

for n in range(3,8):
    for D_val in D_vals:
        for T_val in T_vals:
            for type in Types:
                if type == "H2" or type == "H2p" or type == "H3p":
                    TiHmP, TiHpP = None, None
                else:
                    TiHmP, TiHpP = 2.2, T_val
                Yac_mol_dict["Type="+type+"n="+str(n)+"Den="+D_val+"T="+str(T_val)]=YC.TECPEC_Yacora(type, [n], [float(D_val)], [T_val], [TiHmP], [TiHpP])

print(Yac_mol_dict)
np.save("Yacora_molecule_PECs.npy", Yac_mol_dict)
