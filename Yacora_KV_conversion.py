import numpy as np
import scipy.io as spio
from scipy.interpolate import interp2d, LinearNDInterpolator, interpn

#np.set_printoptions(threshold=np.inf)

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

        points = (data['Te'], data['TiH2p'], data['TiHm'], data['nel'])
        pnts1 = np.log10([val for sublist in points[0] for val in sublist])
        pnts2 = np.log10([val for sublist in points[1] for val in sublist])
        pnts3 = np.log10([val for sublist in points[2] for val in sublist])
        pnts4 = np.log10([val for sublist in points[3] for val in sublist])
        for i in range(0, len(N)):
            PECv[i][:] = interp5L((pnts1, pnts2, pnts3, pnts4), data['PEC'][:, :, :, :, N[i]-1], (Ne, TiHmP, TiHpP, Tev))

        # for i in range(0, len(N)):
        #     coords = []
        #     for j in range(0, len(data['Te'])):
        #         for k in range(0, len(data['TiH2p'])):
        #             for l in range(0, len(data['TiHm'])):
        #                 for m in range(0, len(data['nel'])):
        #                     coords.append((np.log10(data['nel'][m][0]), np.log10(data['TiHm'][l][0]), np.log10(data['TiH2p'][k][0]), np.log10(data['Te'][j][0])))
        #     PECv[i][:] = interp4L(coords, np.ravel(data['PEC'][:, :, :, :, N[i]-1]), Ne, TiHmP, TiHpP, Tev)
        print(type + ' PEC = ' + str(PECv))
        return


def interp2L(coords, V, xN, yN):
    F = LinearNDInterpolator(coords, np.log10(V))
    return 10 ** F(np.log10(xN), np.log10(yN))



def interp4L(coords, V, xN, yN, xN1, xN2):
    F = LinearNDInterpolator(coords, np.log10(V))
    return 10 ** F(np.log10(xN), np.log10(yN), np.log10(xN1), np.log10(xN2))


def interp5L(points, V, point):
    pnt = np.array(point)
    pnt_ = np.log10(pnt)
    pnt__ = pnt_.tolist()
    pnt___ = np.array([val for sublist in pnt__ for val in sublist])
    # F = LinearNDInterpolator(coords, np.log10(V))
    # return 10 ** F(np.log10(xN), np.log10(yN), np.log10(xN1), np.log10(xN2))
    return 10 ** interpn(points, np.log10(V), pnt___)

TECPEC_Yacora('H2', [6], [2e20], [0.8], None, None)
TECPEC_Yacora('H2p', [1], [1.5e18], [1], None, None)
TECPEC_Yacora('H3p', [4], [1.5e19], [1], None, None)
TECPEC_Yacora('HmHp', [6], [1.8e19], [1], [3], [2])
TECPEC_Yacora('HmH2p', [5], [2e19], [1], [2.2], [1])