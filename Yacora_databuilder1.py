import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

pd.set_option('display.max_rows', None)

"""Note this is storing the old data obtained from Yacora - i.e. using 8000 K for temperature.  Data refresh needed"""
def Yac_data():
    for i in range(2, 8):
        Yac_data.Exc_PCs["table_n=" + str(i)] = pd.read_csv('Data_files/Exc_YacoraRun_PopCoeff_n'
                    + str(i) + '.dat', sep='\s+', skiprows=27, usecols=[0,1,2], names=['Temp', 'Density', 'Pop Coeff'])
        Yac_data.Rec_PCs["table_n=" + str(i)] = pd.read_csv('Data_files/Rec_YacoraRun_PopCoeff_n'
                    + str(i) + '.dat', sep='\s+', skiprows=27, usecols=[0,1,2], names=['Temp', 'Density', 'Pop Coeff'])

        currExc = Yac_data.Exc_PCs["table_n=" + str(i)]
        currRec = Yac_data.Rec_PCs["table_n=" + str(i)]

        for j, T_val in enumerate(T_vals):
            for k, D_val in enumerate(D_vals):
                E_tab = currExc.loc[currExc['Temp'] == T_val]
                Exc_PC_dict["n=" + str(i) + "Den=" + D_val + "T=" + str(T_val)] = E_tab.loc[E_tab['Density'] == float(D_val)]
                R_tab = currRec.loc[currRec['Temp'] == T_val]
                Rec_PC_dict["n=" + str(i) + "Den=" + D_val + "T=" + str(T_val)] = R_tab.loc[R_tab['Density'] == float(D_val)]



    # make Balmer PECs
    for n in range(3, 8):
        for p, T_val in enumerate(T_vals):
            for m, D_val in enumerate(D_vals):
                Rec_table = Rec_PC_dict["n=" + str(n) + "Den=" + D_val + "T=" + str(T_val)]
                Rec_table = Rec_table.copy()
                Exc_table = Exc_PC_dict["n=" + str(n) + "Den=" + D_val + "T=" + str(T_val)]
                Exc_table = Exc_table.copy()
                Rec_table["PEC"] = Rec_table["Pop Coeff"] * NIST_As["n=" + str(n)]
                Exc_table["PEC"] = Exc_table["Pop Coeff"] * NIST_As["n=" + str(n)]
                Rec_PC_dict["n=" + str(n) + "Den=" + D_val + "T=" + str(T_val)] = Rec_table
                Exc_PC_dict["n=" + str(n) + "Den=" + D_val + "T=" + str(T_val)] = Exc_table

    print(Rec_PC_dict)
    print(Exc_PC_dict)
    np.save("Yacora_Rec_PECs.npy", Rec_PC_dict)
    np.save("Yacora_Exc_PECs.npy", Exc_PC_dict)


if __name__ == '__main__':

    T_vals = [1, 1.5, 2, 3, 7, 10, 15, 20]
    D_vals = ["5e18", "1e19", "2e19", "5e19", "1e20", "2e20"]
    NIST_As = {"n=3": 4.4114e7, "n=4": 8.4217e6, "n=5": 2.5311e6, "n=6": 9.7346e5, "n=7": 4.3901e5,
               "n=8": 2.3153e5, "n=9": 1.2159e5}  # data from NIST
    colour_list = plt.cm.Set1(np.linspace(0, 1, 6))

    Yac_data.Exc_PCs = {}
    Yac_data.Rec_PCs = {}
    Exc_PC_dict = {}
    Rec_PC_dict = {}
    Yac_data()

