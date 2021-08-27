import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


pd.set_option('display.max_rows', None)



def ADAS():

    d_indeces = [15, 16, 17, 18, 19, 20]
    t_pos = [4, 5, 6, 7, 1, 2, 3, 4]
    line_starts = [70, 174, 278, 382, 486]


    for n, line_start in enumerate(line_starts):
        for Dindex, D in enumerate(d_indeces):
            for j, Tindex in enumerate(t_pos):
                if j < 4:
                    ADAS.Exc_PECs["n=" + str(n+3) + "Den=" + str(D_vals[Dindex]) + "T=" + str(T_vals[j])] = \
                        pd.read_csv('Data_files/pec12#h_balmer#h0 (1).dat', sep='\s+', skiprows=line_start-1+(Dindex*4)
                                    , nrows=1, usecols=[Tindex], names=['PEC'])
                    ADAS.Rec_PECs["n=" + str(n + 3) + "Den=" + str(D_vals[Dindex]) + "T=" + str(T_vals[j])] = \
                        pd.read_csv('Data_files/pec12#h_balmer#h0 (1).dat', sep='\s+',
                                    skiprows=line_start + 1872 - 1 + (Dindex * 4)
                                    , nrows=1, usecols=[Tindex], names=['PEC'])
                else:
                    ADAS.Exc_PECs["n=" + str(n+3) + "Den=" + str(D_vals[Dindex]) + "T=" + str(T_vals[j])] = \
                        pd.read_csv('Data_files/pec12#h_balmer#h0 (1).dat', sep='\s+', skiprows=line_start+(Dindex*4)
                                    , nrows=1, usecols=[Tindex], names=['PEC'])
                    ADAS.Rec_PECs["n=" + str(n + 3) + "Den=" + str(D_vals[Dindex]) + "T=" + str(T_vals[j])] = \
                        pd.read_csv('Data_files/pec12#h_balmer#h0 (1).dat', sep='\s+',
                                    skiprows=line_start + 1872 + (Dindex * 4)
                                    , nrows=1, usecols=[Tindex], names=['PEC'])

    np.save("ADAS_Rec_PECs.npy", ADAS.Rec_PECs)
    np.save("ADAS_Exc_PECs.npy", ADAS.Exc_PECs)



    exit()



if __name__ == '__main__':

    D_vals = ["5e18", "1e19", "2e19", "5e19", "1e20", "2e20"]
    T_vals = [1, 1.5, 2, 3, 7, 10, 15, 20]

    ADAS.Exc_PECs = {}
    ADAS.Rec_PECs = {}


    ADAS()

