import numpy as np
import scipy.io as spio
from scipy.interpolate import interp2d, LinearNDInterpolator, interpn


def TECPEC_Yacora(type, N, Ne, Tev, TiHmP, TiHpP):
    #return PECv
    data = spio.loadmat('Yacora_data_' + type + '.mat')
    Ne = np.clip(Ne, min(data['nel']), max(data['nel']))
    Tev = np.clip(Tev, min(data['Te']), max(data['Te']))


    if type != 'HmHp' and type != 'HmH2p':
        PECv = np.zeros((len(N), len(Ne)))
        PECv[PECv == 0] = np.nan
        for i in range(0, len(N)):
            coords = []
            for j in range(0, len(data['nel'])):
                for k in range(0, len(data['Te'])):
                    coords.append((np.log10(data['nel'][j][0]), np.log10(data['Te'][k][0])))
            PECv[i, :] = interp2L(coords, np.ravel(data['PEC'][:, :, N[i]-1]), Ne, Tev)
        print(type + ' PEC = ' + str(PECv))
        return

    elif type == 'HmHp':
        TiHmP = [element * 11600 for element in TiHmP]
        TiHpP = [element * 11600 for element in TiHpP]
        TiHmP = np.clip(TiHmP, min(data['TiHmP'][0]), max(data['TiHmP'][0]))
        TiHpP = np.clip(TiHpP, min(data['TiHpP'][0]), max(data['TiHpP'][0]))

        AdjF = interp2d(data['TiHmP'], data['TiHpP'], data['AdjF'])
        p=AdjF(TiHmP, TiHpP)
        PECv = np.zeros((len(N), len(Ne)))
        PECv[PECv == 0] = np.nan
        for i in range(0, len(N)):
            coords = []
            for j in range(0, len(data['Te'])):
                for k in range(0, len(data['nel'])):
                    coords.append((np.log10(data['nel'][k][0]), np.log10(data['Te'][j][0])))
            PECv[i, :] = p * interp2L(coords, np.ravel(data['PEC'][:, :, N[i]-1]), Ne, Tev)
        print(type + ' PEC = ' + str(PECv))
        return

    elif type == 'HmH2p':
        TiHmP = [element * 11600 for element in TiHmP]
        TiHpP = [element * 11600 for element in TiHpP]
        TiHmP = np.clip(TiHmP, min(data['TiHm']), max(data['TiHm']))
        TiHpP = np.clip(TiHpP, min(data['TiH2p']), max(data['TiH2p']))

        PECv = np.zeros((len(N), len(Ne)))
        PECv[PECv == 0] = np.nan

        points = (data['nel'], data['TiHm'], data['TiH2p'], data['Te'])
        pnts1 = np.log10([val for sublist in points[0] for val in sublist])
        pnts2 = np.log10([val for sublist in points[1] for val in sublist])
        pnts3 = np.log10([val for sublist in points[2] for val in sublist])
        pnts4 = np.log10([val for sublist in points[3] for val in sublist])
        for i in range(0, len(N)):
            PECv[i][:] = interpN((pnts1, pnts2, pnts3, pnts4), data['PEC'][:, :, :, :, N[i]-1], (Ne, TiHmP, TiHpP, Tev))
        print(type + ' PEC = ' + str(PECv))
        return


def interp2L(coords, V, xN, yN):
    F = LinearNDInterpolator(coords, np.log10(V))
    return 10 ** F(np.log10(xN), np.log10(yN))


def interpN(points, V, point):
    pnt = np.log10(np.asarray(point).reshape(4))
    return 10 ** interpn(points, np.log10(V), pnt)



TECPEC_Yacora('H2', [4], [5e20], [0.15], None, None)
TECPEC_Yacora('H2p', [6], [6e19], [0.32], None, None)
TECPEC_Yacora('H3p', [1], [7e18], [18], None, None)
TECPEC_Yacora('HmHp', [3], [6.1e21], [0.169], [3.5], [4.1])
TECPEC_Yacora('HmH2p', [5], [4.5e19], [1.2], [1.2], [5.1])

