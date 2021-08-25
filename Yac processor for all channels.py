import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import processor as proc

pd.set_option('display.max_rows', None)

def Yac_data():
#def Yac_data(T_vals, D_vals, NIST_As):


    for i in range(2, 21):
        Yac_data.Exc_stack["table_n=" + str(i)] = pd.read_csv('Data_files/Exc_YacoraRun_PopCoeff_n'
                    + str(i) + '.dat', sep='\s+', skiprows=27, usecols=[0,1,2], names=['Temp', 'Density', 'Pop Coeff'])
        Yac_data.Rec_stack["table_n=" + str(i)] = pd.read_csv('Data_files/Rec_YacoraRun_PopCoeff_n'
                    + str(i) + '.dat', sep='\s+', skiprows=27, usecols=[0,1,2], names=['Temp', 'Density', 'Pop Coeff'])

        currExc = Yac_data.Exc_stack["table_n=" + str(i)]
        currRec = Yac_data.Rec_stack["table_n=" + str(i)]

        for j, T_val in enumerate(T_vals):
            Yac_data.Exc_stack["n=" + str(i) + "T=" + str(T_val)] = currExc.loc[currExc['Temp'] == T_val]
            Yac_data.Rec_stack["n=" + str(i) + "T=" + str(T_val)] = currExc.loc[currRec['Temp'] == T_val]

        for j, D_val in enumerate(D_vals):
            Yac_data.Exc_stack["n=" + str(i) + "Den=" + D_val] = currExc.loc[currExc['Density'] == float(D_val)]
            #Yac_data.Exc_stack["n=" + str(i) + "Den=" + D_val].reset_index(drop=True, inplace=True)
            Yac_data.Rec_stack["n=" + str(i) + "Den=" + D_val] = currRec.loc[currExc['Density'] == float(D_val)]
            #Yac_data.Rec_stack["n=" + str(i) + "Den=" + D_val].reset_index(drop=True, inplace=True)



    # make Balmer PECs
    for n in range(3, 10):
        for p, T_val in enumerate(T_vals):
            Rec_table = Yac_data.Rec_stack["n=" + str(n) + "T=" + str(T_val)]
            Rec_table = Rec_table.copy()
            Exc_table = Yac_data.Exc_stack["n=" + str(n) + "T=" + str(T_val)]
            Exc_table = Exc_table.copy()
            Rec_table["PEC"] = Rec_table["Pop Coeff"] * NIST_As["n=" + str(n)]
            Exc_table["PEC"] = Exc_table["Pop Coeff"] * NIST_As["n=" + str(n)]
            Yac_data.Rec_stack["n=" + str(n) + "T=" + str(T_val)] = Rec_table
            Yac_data.Exc_stack["n=" + str(n) + "T=" + str(T_val)] = Exc_table
        for D_val in D_vals:
            Rec_table = Yac_data.Rec_stack["n=" + str(n) + "Den=" + D_val]
            Rec_table = Rec_table.copy()
            Exc_table = Yac_data.Exc_stack["n=" + str(n) + "Den=" + D_val]
            Exc_table = Exc_table.copy()
            Rec_table["PEC"] = Rec_table["Pop Coeff"] * NIST_As["n=" + str(n)]
            Exc_table["PEC"] = Exc_table["Pop Coeff"] * NIST_As["n=" + str(n)]
            Yac_data.Rec_stack["n=" + str(n) + "Den=" + D_val] = Rec_table
            Yac_data.Exc_stack["n=" + str(n) + "Den=" + D_val] = Exc_table


def ADAS():

    d_indeces = np.arange(0, 23)
    t_pos = [4, 5, 6, 7, 1, 2, 3, 4, 5, 6]
    line_starts = [14, 118, 222, 326, 430, 534, 638]


    for n, line_start in enumerate(line_starts):
        for Dindex in d_indeces:
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

    # print(ADAS.Exc_PECs["n=8Den=2e19T=7"].iloc[0]["PEC"])
    # print(ADAS.Rec_PECs["n=4Den=5e20T=2"].iloc[0]["PEC"])
    # print(ADAS.Rec_PECs["n=4Den=5e20T=50"].iloc[0]["PEC"])
    # print(ADAS.Rec_PECs["n=4Den=1e14T=20"].iloc[0]["PEC"])
    # print(ADAS.Rec_PECs["n=6Den=2e14T=1.5"].iloc[0]["PEC"])
    # exit()

def Channels():
    # get all PCs


    levels = np.arange(3, 10)
    for level in levels:
        for T in T_vals_full:
            Channels.PCs["CHAN=H2n=" + str(level) + "Den=2e19T=" + str(T)] = \
                pd.read_csv('Data_files/H2PCn2e19T' + str(T) + 'level' + str(level) + '.dat', sep='\s+',
                            skiprows=27, nrows=1, usecols=[0], names=['PC'])


    for level in levels:
        for T in T_vals_full:
            Channels.PCs["CHAN=H2+n=" + str(level) + "Den=2e19T=" + str(T)] = \
                pd.read_csv('Data_files/H2plusPCn2e19T' + str(T) + 'level' + str(level) + '.dat', sep='\s+',
                            skiprows=27, nrows=1, usecols=[0], names=['PC'])

    for level in levels:
        for T in T_vals_full:
            Channels.PCs["CHAN=H3+n=" + str(level) + "Den=2e19T=" + str(T)] = \
                pd.read_csv('Data_files/H3plusPCn2e19T' + str(T) + 'level' + str(level) + '.dat', sep='\s+',
                            skiprows=28, nrows=1, usecols=[0], names=['PC'])

    for level in levels:
        for T in T_vals_full:
            Channels.PCs["CHAN=H-n=" + str(level) + "Den=2e19T=" + str(T)] = \
                pd.read_csv('Data_files/H-PCn2e19T' + str(T) + 'level' + str(level) + '.dat', sep='\s+',
                            skiprows=29, nrows=1, usecols=[0], names=['PC'])

    for level in levels:
        for T in T_vals_full:

            Channels.PCs["CHAN=H2n=" + str(level) + "Den=2e19T=" + str(T)]["PEC"] =\
                Channels.PCs["CHAN=H2n=" + str(level) + "Den=2e19T=" + str(T)]["PC"] * NIST_As["n=" + str(level)]
            Channels.PCs["CHAN=H2+n=" + str(level) + "Den=2e19T=" + str(T)]["PEC"] = \
                Channels.PCs["CHAN=H2+n=" + str(level) + "Den=2e19T=" + str(T)]["PC"] * NIST_As["n=" + str(level)]
            Channels.PCs["CHAN=H-n=" + str(level) + "Den=2e19T=" + str(T)]["PEC"] = \
                Channels.PCs["CHAN=H-n=" + str(level) + "Den=2e19T=" + str(T)]["PC"] * NIST_As["n=" + str(level)]
            Channels.PCs["CHAN=H3+n=" + str(level) + "Den=2e19T=" + str(T)]["PEC"] = \
                Channels.PCs["CHAN=H3+n=" + str(level) + "Den=2e19T=" + str(T)]["PC"] * NIST_As["n=" + str(level)]

    for level in levels:
        for T in T_vals_full:
            print("Channel=H-, n="+str(level)+", Den = 2e19, T="+str(T)+": PC is: "
                  +str(Channels.PCs["CHAN=H-n="+str(level)+"Den=2e19T="+str(T)].iloc[0]["PC"]))
            print("Channel=H-, n=" + str(level) + ", Den = 2e19, T=" + str(T) + ": PEC is: "
                  + str((Channels.PCs["CHAN=H-n=" + str(level) + "Den=2e19T=" + str(T)].iloc[0]["PC"]*NIST_As["n="+str(level)])))

    # print(Channels.PCs["CHAN=H2n=3Den=2e19T=1"].iloc[0]["PC"])
    # print(Channels.PCs["CHAN=H2n=3Den=2e19T=1"].iloc[0]["PEC"])
    #
    # print(Channels.PCs["CHAN=H2+n=6Den=2e19T=10"].iloc[0]["PC"])
    # print(Channels.PCs["CHAN=H2+n=6Den=2e19T=10"].iloc[0]["PEC"])
    #
    # print(Channels.PCs["CHAN=H-n=6Den=2e19T=10"].iloc[0]["PC"])
    # print(Channels.PCs["CHAN=H-n=6Den=2e19T=10"].iloc[0]["PEC"])
    #
    #
    # print("Channel=H-n=3Den=5e19T=2__PC is:"+str(Channels.PCs["CHAN=H-n=3Den=5e19T=2"].iloc[0]["PC"]))
    # print(" PEC is:" + str(Channels.PCs["CHAN=H-n=3Den=5e19T=2"].iloc[0]["PEC"]))
    #
    # print("Channel=H-n=4Den=5e19T=2__PC is:" + str(Channels.PCs["CHAN=H-n=4Den=5e19T=2"].iloc[0]["PC"]))
    # print(" PEC is:" + str(Channels.PCs["CHAN=H-n=4Den=5e19T=2"].iloc[0]["PEC"]))


def plots():

    # variation with Temperature
    pairs = []
    no_ne = 0.1


    for n in range(4,10):
        pairs.append("B=" + str(n) + "/" + "B=" + str(n-1))
    for i, D in enumerate(D_vals_full):
        for j, pair in enumerate(pairs):
            ratios = []
            ratios2 = []
            ratiosH2 = []
            ratiosH2plus = []
            ratiosHminus = []
            ratiosall = []
            ratiosH3plus = []
            table1 = Yac_data.Rec_stack["n=" + str(j + 4) + "Den=" + D]
            table2 = Yac_data.Exc_stack["n=" + str(j + 4) + "Den=" + D]
            table3 = Yac_data.Rec_stack["n=" + str(j + 3) + "Den=" + D]
            table4 = Yac_data.Exc_stack["n=" + str(j + 3) + "Den=" + D]
            for k, T in enumerate(T_vals_full):
                #get PECs for Yacora data
                PEC1 = table1[table1.Temp == T]["PEC"].iloc[0]
                PEC2 = table2[table2.Temp == T]["PEC"].iloc[0]
                PEC3 = table3[table3.Temp == T]["PEC"].iloc[0]
                PEC4 = table4[table4.Temp == T]["PEC"].iloc[0]
                ratios.append((PEC1 + no_ne*PEC2)/(PEC3 + no_ne*PEC4))
                #get PECs for ADAS data
                APEC1 = ADAS.Rec_PECs["n=" + str(j + 4) + "Den=" + D + "T=" + str(T)].iloc[0]["PEC"]
                APEC2 = ADAS.Exc_PECs["n=" + str(j + 4) + "Den=" + D + "T=" + str(T)].iloc[0]["PEC"]
                APEC3 = ADAS.Rec_PECs["n=" + str(j + 3) + "Den=" + D + "T=" + str(T)].iloc[0]["PEC"]
                APEC4 = ADAS.Exc_PECs["n=" + str(j + 3) + "Den=" + D + "T=" + str(T)].iloc[0]["PEC"]
                ratios2.append((APEC1 + no_ne*APEC2)/(APEC3 + no_ne*APEC4))

                #get extra data for H2 channel
                H2PEC1 = Channels.PCs["CHAN=H2n=" + str(j + 4) + "Den=2e19T=" + str(T)].iloc[0]["PEC"]
                H2PEC2 = Channels.PCs["CHAN=H2n=" + str(j + 3) + "Den=2e19T=" + str(T)].iloc[0]["PEC"]
                nh2_ne = proc.find_nh2(T)/2e19
                ratiosH2.append((PEC1 + no_ne*PEC2 + nh2_ne*H2PEC1)/(PEC3 + no_ne*PEC4 +nh2_ne*H2PEC2))


                #get extra data for H2+ channel
                H2plusPEC1 = Channels.PCs["CHAN=H2+n=" + str(j + 4) + "Den=2e19T=" + str(T)].iloc[0]["PEC"]
                H2plusPEC2 = Channels.PCs["CHAN=H2+n=" + str(j + 3) + "Den=2e19T=" + str(T)].iloc[0]["PEC"]
                nh2plus_ne = proc.get_H2plus_H2_ratio(2e19, T)*proc.find_nh2(T) / 2e19
                ratiosH2plus.append((PEC1 + no_ne * PEC2 + nh2plus_ne * H2plusPEC1) / (PEC3 + no_ne * PEC4 + nh2plus_ne * H2plusPEC2))

                # get extra data for H3+ channel
                H3plusPEC1 = Channels.PCs["CHAN=H3+n=" + str(j + 4) + "Den=2e19T=" + str(T)].iloc[0]["PEC"]
                H3plusPEC2 = Channels.PCs["CHAN=H3+n=" + str(j + 3) + "Den=2e19T=" + str(T)].iloc[0]["PEC"]
                nh3plus_ne = proc.get_H3plus_H2_ratio(2e19, T) * proc.find_nh2(T) / 2e19
                ratiosH3plus.append(
                    (PEC1 + no_ne * PEC2 + nh3plus_ne * H3plusPEC1) / (PEC3 + no_ne * PEC4 + nh3plus_ne * H3plusPEC2))

                #get extra data for H- channel
                HminusPEC1 = Channels.PCs["CHAN=H2+n=" + str(j + 4) + "Den=2e19T=" + str(T)].iloc[0]["PEC"]
                HminusPEC2 = Channels.PCs["CHAN=H2+n=" + str(j + 3) + "Den=2e19T=" + str(T)].iloc[0]["PEC"]
                nhminus_ne = proc.get_Hminus_H2_ratio(2e19, T) * proc.find_nh2(T) / 2e19
                ratiosHminus.append(
                    (PEC1 + no_ne * PEC2 + nhminus_ne * HminusPEC1) / (PEC3 + no_ne * PEC4 + nhminus_ne * HminusPEC2))


                #all effects
                ratiosall.append(
                    (PEC1 + no_ne * PEC2 + nhminus_ne * HminusPEC1 + nh2_ne * H2PEC1 + nh2plus_ne * H2plusPEC1) /
                    (PEC3 + no_ne * PEC4 + nhminus_ne * HminusPEC2 + nh2_ne * H2PEC2 + nh2plus_ne * H2plusPEC2))

            data = {'Temp': T_vals_full, 'ratio': ratios}
            data2 = {'Temp': T_vals_full, 'ratio': ratios2}
            graph_frame = pd.DataFrame(data, columns=['Temp', 'ratio'])
            graph_frame2 = pd.DataFrame(data2, columns=['Temp', 'ratio'])

            x_axis = graph_frame['Temp'].tolist()
            y_axis = graph_frame['ratio'].tolist()
            y_axis2 = graph_frame2['ratio'].tolist()

            plt.xscale("log")
            plt.plot(x_axis, y_axis, color=colour_list[j], label=pair)
            plt.plot(x_axis, y_axis2, color=colour_list[j], linestyle='dotted')

            # dataH2 = {'Temp': T_vals_full, 'ratio': ratiosH2}
            # graph_frameH2 = pd.DataFrame(dataH2, columns=['Temp', 'ratio'])
            # y_axisH2 = graph_frameH2['ratio'].tolist()
            # plt.plot(x_axis, y_axisH2, color=colour_list[j], linestyle='dashed')

            # dataH2plus = {'Temp': T_vals_full, 'ratio': ratiosH2plus}
            # graph_frameH2plus = pd.DataFrame(dataH2plus, columns=['Temp', 'ratio'])
            # y_axisH2plus = graph_frameH2plus['ratio'].tolist()
            # plt.plot(x_axis, y_axisH2plus, color=colour_list[j], linestyle='dashed')

            # dataHminus = {'Temp': T_vals_full, 'ratio': ratiosHminus}
            # graph_frameHminus = pd.DataFrame(dataHminus, columns=['Temp', 'ratio'])
            # y_axisHminus = graph_frameHminus['ratio'].tolist()
            # plt.plot(x_axis, y_axisHminus, color=colour_list[j], linestyle='dashed')

            dataH3plus = {'Temp': T_vals_full, 'ratio': ratiosH3plus}
            graph_frameH3plus = pd.DataFrame(dataH3plus, columns=['Temp', 'ratio'])
            y_axisH3plus = graph_frameH3plus['ratio'].tolist()
            plt.plot(x_axis, y_axisH3plus, color=colour_list[j], linestyle='dashed')


            # dataall = {'Temp': T_vals_full, 'ratio': ratiosall}
            # graph_frameall = pd.DataFrame(dataall, columns=['Temp', 'ratio'])
            # y_axisall = graph_frameall['ratio'].tolist()
            # plt.plot(x_axis, y_axisall, color=colour_list[j], linestyle='dashed')



            plt.grid()
            plt.ylim(0, 0.8)
            plt.title("Density = " + D +"/m^-3")
            plt.xlabel("Temperature in eV")
            plt.ylabel("Balmer line ratio")

        plt.plot([], [], ' ', label="dots: ADAS")
        plt.plot([], [], ' ', label="solid: Yacora")
        plt.plot([], [], ' ', label="dashed: H3+")

        plt.legend(loc="upper right")

        plt.show()



     # Yac_data.Exc_stack["n=5T=1"].plot(x='Temp', y='Pop Coeff')
     # plt.show()



if __name__ == '__main__':

    T_vals = [1, 1.5, 2, 3, 7, 10, 15, 20, 30, 50]
    D_vals = ["1e14", "2e14", "5e14", "1e15", "2e15", "5e15", "1e16", "2e16", "5e16", "1e17", "2e17", "5e17", "1e18",
              "2e18",
              "5e18", "1e19", "2e19", "5e19", "1e20", "2e20", "5e20", "1e21", "2e21"]
    T_vals_full = [1, 2, 3, 7, 10, 20]
    D_vals_full = ["2e19"]
    NIST_As = {"n=3": 4.4114e7, "n=4": 8.4217e6, "n=5": 2.5311e6, "n=6": 9.7346e5, "n=7": 4.3901e5,
               "n=8": 2.3153e5, "n=9": 1.2159e5}  # data from NIST
    colour_list = plt.cm.Set1(np.linspace(0, 1, 6))

    Yac_data.Exc_stack = {}
    Yac_data.Rec_stack = {}
    ADAS.Exc_PECs = {}
    ADAS.Rec_PECs = {}
    Channels.PCs = {}





    ADAS()
    Yac_data()
    Channels()
    #plots()