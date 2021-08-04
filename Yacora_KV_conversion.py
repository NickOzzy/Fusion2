import numpy as np
import scipy.io as spio
from scipy.interpolate import interp2d, RegularGridInterpolator, interpn

np.set_printoptions(threshold=np.inf)

def TECPEC_Yacora(type, N, Ne, Tev, TiHmP, TiHpP):
    #return PECv
    data = spio.loadmat('Yacora_data_' + type + '.mat')
    Ne = np.clip(Ne, min(data['nel']), max(data['nel']))
    Tev = np.clip(Tev, min(data['Te']), max(data['Te']))


    if type != 'HmHp' and type != 'HmH2p':
        PECv = np.zeros(len(N), len(Ne))
        PECv[PECv == 0] = np.nan
        for i in range(0,len(N)-1):
            PECv[i][:] = interp2L(['nel'], data['Te'], np.squeeze(data['PEC'][:][:][N[i]]), Ne, Tev)
        return

    elif type == 'HmHp':
        TiHmP = TiHmP[:]*11600
        TiHpP = TiHpP[:]*11600
        TiHmP = np.clip(TiHmP, min(data['TiHmP']), max(data['TiHmP']))
        TiHpP = np.clip(TiHpP, min(data['TiHpP']), max(data['TiHpP']))

        AdjF = interp2d((data['TiHmP'], data['TiHpP']), data['AdjF'], (TiHmP, TiHpP))
        PECv = np.zeros(len(N), len(Ne))
        PECv[PECv == 0] = np.nan
        for i in range(0,len(N-1)):
            PECv[i][:] = AdjF * interp2L(['nel'], data['Te'], np.squeeze(data['PEC'][:][:][N[i]]), Ne, Tev)
        return

    elif type == 'HmH2p':

        TiHmP = TiHmP[:] * 11600
        TiHpP = TiHpP[:] * 11600
        TiHmP = np.clip(TiHmP, min(data['TiHm']), max(data['TiHm']))
        TiHpP = np.clip(TiHpP, min(data['TiH2P']), max(data['TiH2P']))

        PECv = np.zeros(len(N), len(Ne))
        PECv[PECv == 0] = np.nan

        for i in range(0,len(N-1))
            PECv[i][:] = interp4L(data['nel'], data['TiHm'], data['TiH2p'], data['Te'], np.squeeze(data['PEC'][:][:][:][:][N(i)]), Ne, TiHmP, TiHpP, Tev)
        return


def interp2L(x, y, V, xN, yN):
    F = RegularGridInterpolator((np.log10(x), np.log10(y)), np.log10(V))
    return 10 ** F(np.log10(xN), np.log10(yN))

def interp4L(x, y, x1, x2, V, xN, yN, xN1, xN2):
    point = np.array(np.log10(xN), np.log10(yN), np.log10(xN1), np.log10(xN2))
    return 10 ** interpn(np.array((np.log10(x), np.log10(y), np.log10(x1), np.log10(x2))), np.log10(V), point)