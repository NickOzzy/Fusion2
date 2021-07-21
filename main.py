import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)

# makes lists of the densities and temperatures.
def make_lists(row1, row2):
    dens = []
    temps = []
    drows = int((row1) / 8) + ((row1) % 8 > 0)
    trows = int((row2) / 8) + ((row2) % 8 > 0)
    for row in range(1, drows + 1):
        dens.extend(df.iloc[row, 0].split())
    for row in range(drows + 1, drows + trows + 1):
        temps.extend(df.iloc[row, 0].split())
    return dens, temps, drows, trows


if __name__ == '__main__':

    df = pd.read_table('pec12#h_balmer#h0 (1).dat')
    no_dens = df.iloc[0, 0].split()[1]
    no_temps = df.iloc[0, 0].split()[2]
    print(df)
    dens, temps, drows, trows = make_lists(int(no_dens), int(no_temps))
    print(temps)
    print(dens)
    ex_wavelengths = df[df[df.columns[0]].str.contains('A') &
                     df[df.columns[0]].str.contains('EX')]
    rec_wavelengths = df[df[df.columns[0]].str.contains('A') &
                     df[df.columns[0]].str.contains('REC')]
    ex_rows = ex_wavelengths.index.tolist()
    rec_rows = rec_wavelengths.index.tolist()
    print(ex_rows)
    print(rec_rows)

    density_choice = input("Choose density from:" + str(dens))
    n = [i for i, x in enumerate(dens) if x == density_choice]
    n = n[0] + 1
    print(n)

    temp_choice = input("Choose temp from:" + str(temps))
    t = [p for p, x in enumerate(temps) if x == temp_choice]
    t = t[0]
    print(t)

    evol = np.zeros((17, len(dens)))

    for n in range(1, 25, 1):

        lambda_list = []
        transition_energies = []
        for i, row in enumerate(ex_rows):
            lambda_list.append(df.iloc[row, 0].split()[0])
            transition_energies.append(6.63E-34*3E8*1E10/(1.6E-19*float(lambda_list[i].strip('A'))))

        PEC_list = []
        PEC_Rlist = []

        EX_PECs = np.zeros((len(lambda_list), len(temps)))
        REC_PECs = np.zeros((len(lambda_list), len(temps)))



        for i, row in enumerate(ex_rows):
            for trow in range(row+drows+1, row+drows+trows+1):
                PEC_list.extend(df.iloc[trow+(trows * n), 0].split())
            EX_PECs[i][:] = PEC_list
            PEC_list = []


        for j, row in enumerate(rec_rows):
            for trow in range(row+drows+1, row+drows+trows+1):
                PEC_Rlist.extend(df.iloc[trow+(trows * n), 0].split())
            REC_PECs[j][:] = PEC_Rlist
            PEC_Rlist = []

        trans = np.transpose(EX_PECs)
        transR = np.transpose(REC_PECs)

        newdf = pd.DataFrame(data=trans, columns=lambda_list)
        newdf['Temperature'] = temps

        newdfR = pd.DataFrame(data=transR, columns=lambda_list)
        newdfR['Temperature'] = temps

        No_Ne =  0.1

        fracdf = pd.DataFrame(data={'Temperature': temps})
        ratios = []
        for i, wavelength in enumerate(lambda_list):
            ratios.append(str(i+4)+'/'+str(i+3))
        ratios.pop()
        print(ratios)
        evoldf = pd.DataFrame(data={'Ratio': ratios})
        print(evoldf)
        for i, ratio in enumerate(ratios):
            if i < (len(lambda_list) - 1):
                fracdf[ratio] = (newdfR[lambda_list[i+1]] + (No_Ne * newdf[lambda_list[i+1]])) / (newdfR[lambda_list[i]] + (No_Ne * newdf[lambda_list[i]]))

        #print(fracdf)
        print(lambda_list)

        temps = np.array(temps)
        temp_axis = temps.astype(float)

        #print(evol)

        # transition_mins = []
        # transition_maxs = []

        for i, ratio in enumerate(ratios):

            if i < len(ratios) - 1:
                plt.plot(temp_axis, fracdf.iloc[:, i + 1].values, label='$B_{'+str(i+4)+'→2}$'+'/'+'$B_{'+str(i+3)+'→2}$')
                #plt.plot(temp_axis, fracdf.iloc[:, i+1].values, label='B(n='+str(i+4)+')'+'/'+'B(n='+str(i+3)+')')



            plt.xscale('log')
            plt.xlabel('Temperature in eV')
            plt.ylabel('Predicted Balmer line ratio')
            #plt.title('ne = '+str("{:.2e}".format(float(dens[n-1]) * 1E6))+' m^-3')
            plt.title('$n_e$ = ' + dens[n - 1] + ' /cm^3 $  (n_o$/$n_e$ = 0.1)')
            plt.legend(loc=1)
            plt.grid()
        plt.show()
        #print(fracdf[['Temperature', '5/4', '6/5', '7/6', '8/7']])



        print(fracdf)
        for l, ratio in enumerate(ratios):
            if l < 17:
                evol[l][n-1] = fracdf.iloc[t, l+1]


    #print(evol)

    trans_evol = np.transpose(evol)
    print(evol)
    print(trans_evol)


    for p, den in enumerate(dens):
        evoldf[den] = trans_evol[p, :]

    print(evoldf)
    dens = np.array(dens)
    dens_axis = dens.astype(float)

    for i, ratio in enumerate(ratios):

        if i < len(ratios) - 1:
            plt.plot(dens_axis, evoldf.iloc[i, 1:].values,
                     label='$B_{' + str(i + 4) + '→2}$' + '/' + '$B_{' + str(i + 3) + '→2}$')
            # plt.plot(temp_axis, fracdf.iloc[:, i+1].values, label='B(n='+str(i+4)+')'+'/'+'B(n='+str(i+3)+')')

        plt.xscale('log')
        plt.xlabel('Electron density, $n_e$ / cm^-3')
        plt.ylabel('Predicted Balmer line ratio')
        # plt.title('ne = '+str("{:.2e}".format(float(dens[n-1]) * 1E6))+' m^-3')
        plt.title('$T_e$ = ' + temp_choice + ' eV $  (n_o$/$n_e$ = 0.1)')
        plt.legend(loc=1)
        plt.grid()
    plt.show()

