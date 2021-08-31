import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, CheckButtons
import matplotlib
matplotlib.use('TkAgg')


def assemble(Density, no_ne):
    ratios_ADAS = {}
    ratios_Yacora = {}
    for j, pair in enumerate(pairs):
        for k, T in enumerate(T_vals):
            APEC1 = ADAS_Recombination_PECs["n=" + str(j + 4) + "Den=" + Density + "T=" + str(T)].iloc[0]["PEC"]
            APEC2 = ADAS_Excitation_PECs["n=" + str(j + 4) + "Den=" + Density + "T=" + str(T)].iloc[0]["PEC"]
            APEC3 = ADAS_Recombination_PECs["n=" + str(j + 3) + "Den=" + Density + "T=" + str(T)].iloc[0]["PEC"]
            APEC4 = ADAS_Excitation_PECs["n=" + str(j + 3) + "Den=" + Density + "T=" + str(T)].iloc[0]["PEC"]
            ratios_ADAS["pair="+pair+" T="+str(T)] = ((APEC1 + no_ne*APEC2)/(APEC3 + no_ne*APEC4))
            YPEC1 = YDAS_Recombination_PECs["n=" + str(j + 4)+ "Den=" + Density + "T=" + str(T)].iloc[0]["PEC"]
            YPEC2 = YDAS_Excitation_PECs["n=" + str(j + 4)+ "Den=" + Density + "T=" + str(T)].iloc[0]["PEC"]
            YPEC3 = YDAS_Recombination_PECs["n=" + str(j + 3) + "Den=" + Density + "T=" + str(T)].iloc[0]["PEC"]
            YPEC4 = YDAS_Excitation_PECs["n=" + str(j + 3) + "Den=" + Density + "T=" + str(T)].iloc[0]["PEC"]
            ratios_Yacora["pair="+pair+"T="+ str(T)] = ((YPEC1 + no_ne*YPEC2)/(YPEC3 + no_ne*YPEC4))
    return ratios_ADAS, ratios_Yacora


def plotting():
        data = []
        data_dict_A, data_dict_Y = assemble(density, no_ne)
        graph = []
        graph2 = []

        for i, pair in enumerate(pairs):
            data.append({'Temp': T_vals, 'ratio': [val for key, val in data_dict_A.items() if pair in key],
                         'ratio2': [val for key, val in data_dict_Y.items() if pair in key]})
            graph_frame = pd.DataFrame(data[i], columns=['Temp', 'ratio', 'ratio2'])
            x_axis = graph_frame['Temp'].tolist()
            y_axis = graph_frame['ratio'].tolist()
            y_axis2 = graph_frame['ratio2'].tolist()
            plt.xscale("log")
            graph.append(plt.plot(x_axis, y_axis, marker='o', color=colour_list[i], label=pair, visible=False))
            graph2.append(plt.plot(x_axis, y_axis2, color=colour_list[i], linestyle="dashed", visible=False))
        plt.ylim(0, 0.6)
        plt.xlabel("Temperature in eV")
        plt.ylabel("Balmer line ratio")
        plt.legend(loc="upper right")
        return graph, graph2


def update(val):
    data = []
    density = str('{:0.0e}'.format(10**(D_Slider.val), 0)).replace("+", "")
    no_ne = no_ne_Slider.val
    data_dict_A, data_dict_Y = assemble(density, no_ne)

    for i, pair in enumerate(pairs):
        data.append({'Temp': T_vals, 'ratio': [val for key, val in data_dict_A.items() if pair in key],
                     'ratio2': [val for key, val in data_dict_Y.items() if pair in key]})
        graph_frame = pd.DataFrame(data[i], columns=['Temp', 'ratio', 'ratio2'])
        y_axis = graph_frame['ratio'].tolist()
        y_axis2 = graph_frame['ratio2'].tolist()
        graph[i][0].set_ydata(y_axis)
        graph[i][0].set_visible(Y_radio.get_status()[1])
        graph2[i][0].set_ydata(y_axis2)
        graph2[i][0].set_visible(Y_radio.get_status()[0])
    D_Slider.valtext.set_text(density+" /m^3")
    fig.canvas.draw_idle()




if __name__ == '__main__':

    D_vals = ["5e18", "1e19", "2e19", "5e19", "1e20", "2e20"]
    T_vals = [1, 1.5, 2, 3, 7, 10, 15, 20]

    NIST_As = {"n=3": 4.4114e7, "n=4": 8.4217e6, "n=5": 2.5311e6, "n=6": 9.7346e5, "n=7": 4.3901e5,
               "n=8": 2.3153e5, "n=9": 1.2159e5}  # data from NIST
    colour_list = plt.cm.Set1(np.linspace(0, 1, 6))

    ADAS_Excitation_PECs = np.load("ADAS_Exc_PECs.npy", allow_pickle=True).item()
    ADAS_Recombination_PECs = np.load("ADAS_Rec_PECs.npy", allow_pickle=True).item()
    YDAS_Excitation_PECs = np.load("Yacora_Exc_PECs.npy", allow_pickle=True).item()
    YDAS_Recombination_PECs = np.load("Yacora_Rec_PECs.npy", allow_pickle=True).item()
    no_ne, density = 0.1, "2e19"


    pairs = []
    for n in range(4,8):
        pairs.append("B=" + str(n) + "/" + "B=" + str(n-1))

    fig = plt.figure()
    fig.set_size_inches(6,8)
    plt.subplots_adjust(bottom=0.5)
    graph, graph2 = plotting()
    D_axis = plt.axes([0.1, 0.35, 0.7, 0.02])
    steps = [np.log10(5e18), np.log10(1e19), np.log10(2e19), np.log10(5e19), np.log10(1e20), np.log10(2e20)]
    dmin, dmax, dinit = np.log10(5e18), np.log10(2e20), np.log10(2e19)
    D_Slider = Slider(D_axis, "density", dmin, dmax, valinit=dinit, valstep=steps)
    D_Slider.valtext.set_text(density+" /m^3")
    D_Slider.on_changed(update)
    no_ne_axis = plt.axes([0.1, 0.4, 0.7, 0.02])
    no_nemin, no_nemax = 0, 1.1
    no_ne_Slider = Slider(no_ne_axis, "no/ne", no_nemin, no_nemax, valinit=0.1, valstep=np.arange(0, 1.11, 0.01))
    no_ne_Slider.on_changed(update)
    Y_radio_axis = plt.axes([0.1, 0.1, 0.4, 0.2])
    Y_radio = CheckButtons(Y_radio_axis, ['Yacora - no molecules', 'ADAS - no molecules', 'Yacora - include H2',
                                          'Yacora - include H2+', 'Yacora - include H3+', 'Yacora - include H-H+',
                                          'Yacora - include H-H2+'], [False]*7)
    Y_radio.on_clicked(update)
    plt.show()
    # print(ADAS_Excitation_PECs["n=6Den=2e19T=7"].iloc[0]["PEC"])
    # print(ADAS_Excitation_PECs["n=3Den=5e19T=1"].iloc[0]["PEC"])
    # print(ADAS_Recombination_PECs["n=4Den=2e20T=2"].iloc[0]["PEC"])
    # print(ADAS_Recombination_PECs["n=5Den=5e18T=20"].iloc[0]["PEC"])
    #
    # print(ADAS_Excitation_PECs)