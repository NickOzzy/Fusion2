import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, CheckButtons
import matplotlib

matplotlib.use('TkAgg')


def find_nh2ii(T, dl, a, b):
    return (10 ** a / (dl * (T ** b)))


def assemble(Density, no_ne, dl, a, b, h2flag, h2pflag, h3pflag, hmhpflag, hmh2pflag, C_flag):
    D = float(Density)
    absolutes = {}
    for j, absol in enumerate(absols):
        for k, T in enumerate(T_vals):
            nh2 = find_nh2ii(T, dl, a, b)
            if h2flag:
                nh2_ne = nh2 / D
            else:
                nh2_ne = 0
            if h2pflag:
                nh2p_ne = param_dict["Den=" + Density + "T=" + str(T) + "H2p/H2"] * nh2 / D
            else:
                nh2p_ne = 0
            if h3pflag:
                nh3p_ne = param_dict["Den=" + Density + "T=" + str(T) + "H3p/H2"] * nh2 / D
            else:
                nh3p_ne = 0
            if hmhpflag:
                nhm_ne = param_dict["Den=" + Density + "T=" + str(T) + "Hm/H2"] * nh2 / D
            else:
                nhm_ne = 0
            if hmh2pflag:
                nhmnh2p_ne2 = param_dict["Den=" + Density + "T=" + str(T) + "Hm/H2"] * param_dict[
                    "Den=" + Density + "T=" + str(T) + "H2p/H2"] / (D ** 2)
            else:
                nhmnh2p_ne2 = 0

            R2R = YDAS_Recombination_PECs["n=2Den=" + Density + "T=" + str(T)].iloc[0]["Pop Coeff"]
            R2E = YDAS_Excitation_PECs["n=2Den=" + Density + "T=" + str(T)].iloc[0]["Pop Coeff"]
            #print(D*R2R)
            YPECa1 = YDAS_Recombination_PECs["n=" + str(j + 3) + "Den=" + Density + "T=" + str(T)].iloc[0]["PEC"] / (
                        1 + C_flag * D * R2R)
            YPECa2 = YDAS_Excitation_PECs["n=" + str(j + 3) + "Den=" + Density + "T=" + str(T)].iloc[0]["PEC"] / (
                        1 + C_flag * D * R2E)
            YPECa3 = Y_Buster_PECs["Type=H2n=" + str(j + 3) + "Den=" + Density + "T=" + str(T)] / \
                     (1 + C_flag * D * (Y_Buster_PECs["Type=H2n=2Den=" + Density + "T=" + str(T)]) / NIST_As["n=2"])
            YPECa4 = Y_Buster_PECs["Type=H2pn=" + str(j + 3) + "Den=" + Density + "T=" + str(T)] / \
                     (1 + C_flag * D * (Y_Buster_PECs["Type=H2pn=2Den=" + Density + "T=" + str(T)]) / NIST_As["n=2"])
            YPECa5 = Y_Buster_PECs["Type=H3pn=" + str(j + 3) + "Den=" + Density + "T=" + str(T)] / \
                     (1 + C_flag * D * (Y_Buster_PECs["Type=H3pn=2Den=" + Density + "T=" + str(T)]) / NIST_As["n=2"])
            YPECa6 = Y_Buster_PECs["Type=HmHpn=" + str(j + 3) + "Den=" + Density + "T=" + str(T)] / \
                     (1 + C_flag * D * (Y_Buster_PECs["Type=HmHpn=2Den=" + Density + "T=" + str(T)]) / NIST_As["n=2"])
            YPECa7 = Y_Buster_PECs["Type=HmH2pn=" + str(j + 3) + "Den=" + Density + "T=" + str(T)] / \
                     (1 + C_flag * D * (Y_Buster_PECs["Type=HmH2pn=2Den=" + Density + "T=" + str(T)]) / NIST_As["n=2"])

            absolutes["n=" + str(j + 3) + "T=" + str(T)] = dl * (
                        D ** 2 * YPECa1 + no_ne * D ** 2 * YPECa2 + D ** 2 * nh2_ne * YPECa3 + D ** 2 * nh2p_ne *
                        YPECa4 + D ** 2 * nh3p_ne * YPECa5 + D ** 2 * nhm_ne * YPECa6 + D ** 2 * nhmnh2p_ne2 * YPECa7)

    return absolutes


def plotting():
    data = []
    dict_abs = assemble(density, no_ne, 0.05, 17.2, 1.7, False, False, False, False, False, False)
    graph = []
    graph2 = []
    graph3 = []

    for i, absol in enumerate(absols):

        data.append({'Temp': T_vals, 'Abs': [val for key, val in dict_abs.items() if absol in key]})
        graph_frame = pd.DataFrame(data[i], columns=['Temp', 'Abs'])
        x_axis = graph_frame['Temp'].tolist()
        y_axis3 = graph_frame['Abs'].tolist()
        plt.xscale("log")
        graph3.append(plt.plot(x_axis, y_axis3, marker='o', color=colour_list[i], label=absol, linestyle="dashed", visible=True))
    #plt.ylim(0, 0.6)
    plt.xlabel("Temperature in eV")
    plt.ylabel("Absolute brightness")
    plt.legend(loc="upper right")
    return graph3


def update(val):
    data = []
    density = str('{:0.0e}'.format(10 ** (D_Slider.val), 0)).replace("+", "")
    no_ne = no_ne_Slider.val
    dl = deltaL.val
    a = power.val
    b = bval.val
    dict_abs = assemble(density, no_ne, dl, a, b, Y_radio.get_status()[2], Y_radio.get_status()[3],
                                        Y_radio.get_status()[4], Y_radio.get_status()[5], Y_radio.get_status()[6],
                                        Y_correct.get_status()[0])
    for i, absol in enumerate(absols):
        data.append({'Temp': T_vals, 'Abs': [val for key, val in dict_abs.items() if absol in key]})
        graph_frame = pd.DataFrame(data[i], columns=['Temp', 'Abs'])
        y_axis3 = graph_frame['Abs'].tolist()

        graph3[i][0].set_ydata(y_axis3)

    D_Slider.valtext.set_text(density + " /m^3")
    fig.canvas.draw_idle()


if __name__ == '__main__':

    D_vals = ["5e18", "1e19", "2e19", "5e19", "1e20", "2e20"]
    T_vals = [1, 1.5, 2, 3, 7, 10, 15, 20]

    NIST_As = {"n=2": 4.6999e8, "n=3": 4.4114e7, "n=4": 8.4217e6, "n=5": 2.5311e6, "n=6": 9.7346e5, "n=7": 4.3901e5,
               "n=8": 2.3153e5, "n=9": 1.2159e5}  # data from NIST, note "n=2" is the lyman alpha coefficient.
    colour_list = plt.cm.Set1(np.linspace(0, 1, 6))

    ADAS_Excitation_PECs = np.load("ADAS_Exc_PECs.npy", allow_pickle=True).item()
    ADAS_Recombination_PECs = np.load("ADAS_Rec_PECs.npy", allow_pickle=True).item()
    YDAS_Excitation_PECs = np.load("Yacora_Exc_PECs.npy", allow_pickle=True).item()
    YDAS_Recombination_PECs = np.load("Yacora_Rec_PECs.npy", allow_pickle=True).item()
    Y_Buster_PECs = np.load("Yacora_molecule_PECs.npy", allow_pickle=True).item()
    param_dict = np.load("params.npy", allow_pickle=True).item()
    no_ne, density = 0.1, "2e19"

    pairs = []
    absols = []
    for n in range(4, 9):
        pairs.append("B=" + str(n) + "/" + "B=" + str(n - 1))
        absols.append("n="+str(n-1))
    fig = plt.figure()
    fig.set_size_inches(6, 8)
    plt.subplots_adjust(bottom=0.5)
    graph3 = plotting()
    D_axis = plt.axes([0.1, 0.35, 0.7, 0.02])
    steps = [np.log10(5e18), np.log10(1e19), np.log10(2e19), np.log10(5e19), np.log10(1e20), np.log10(2e20)]
    dmin, dmax, dinit = np.log10(5e18), np.log10(2e20), np.log10(2e19)
    D_Slider = Slider(D_axis, "density", dmin, dmax, valinit=dinit, valstep=steps)
    D_Slider.valtext.set_text(density + " /m^3")
    D_Slider.on_changed(update)
    no_ne_axis = plt.axes([0.1, 0.4, 0.7, 0.02])
    no_nemin, no_nemax = 0, 1.1
    no_ne_Slider = Slider(no_ne_axis, "no/ne", no_nemin, no_nemax, valinit=0.1, valstep=np.arange(0, 1.11, 0.01))
    no_ne_Slider.on_changed(update)
    Y_radio_axis = plt.axes([0.05, 0.1, 0.4, 0.2])
    Y_radio = CheckButtons(Y_radio_axis, ['Yacora - no molecules', 'ADAS - no molecules', 'Yacora - include H2',
                                          'Yacora - include H2+', 'Yacora - include H3+', 'Yacora - include H-H+',
                                          'Yacora - include H-H2+'], [True, False, False, False, False, False, False])
    Y_radio.on_clicked(update)
    plt.figtext(0.55, 0.25, "$n_{H_2} = \dfrac{10^a}{\Delta L*T^b}$", fontsize=12)
    dLaxis = plt.axes([0.50, 0.20, 0.35, 0.02])
    baxis = plt.axes([0.50, 0.10, 0.35, 0.02])
    poweraxis = plt.axes([0.50, 0.15, 0.35, 0.02])
    dLmin, dLmax, dLinit = 0.01, 0.5, 0.05
    deltaL = Slider(dLaxis, "$\Delta L$", dLmin, dLmax, valinit=dLinit, valstep=np.arange(0.01, 0.501, 0.01))
    deltaL.valtext.set_text("0.05 m")
    deltaL.on_changed(update)
    bval = Slider(baxis, "$b$", 1, 2, 1.7, valstep=np.arange(1, 2.1, 0.1))
    bval.on_changed(update)
    power = Slider(poweraxis, "$a$", 15, 19, 17.2, valstep=np.arange(15, 19.1, 0.1))
    power.on_changed(update)
    Y_correct_axis = plt.axes([0.05, 0.02, 0.4, 0.05])
    Y_correct = CheckButtons(Y_correct_axis, ['Gnd-state only correction'], [False])
    Y_correct.on_clicked(update)
    plt.show()