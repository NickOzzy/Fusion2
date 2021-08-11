import numpy as np
import scipy.io as spio
from scipy.interpolate import interp2d, LinearNDInterpolator, interpn, RegularGridInterpolator, griddata

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
            PECv[i,:] = interp2L(data['nel'], data['Te'], np.squeeze(data['PEC'][:][:][N[i]]), Ne, Tev)
        return PECv

    elif type == 'HmHp':
        TiHmP = [element * 11600 for element in TiHmP]
        TiHpP = [element * 11600 for element in TiHpP]
        TiHmP = np.clip(TiHmP, min(TiHmP), max(TiHmP))
        TiHpP = np.clip(TiHpP, min(TiHpP), max(TiHpP))

        AdjF = interp2d(data['TiHmP'], data['TiHpP'], data['AdjF'])
        p=AdjF(TiHmP, TiHpP)
        PECv = np.zeros((len(N), len(Ne)))
        PECv[PECv == 0] = np.nan
        for i in range(0,len(N)):
            PECv[i, :] = interp2L(data['nel'], data['Te'], data['PEC'][:, :, N[i]], Ne, Tev)
            #PECv[i,:] = AdjF(TiHmP, TiHpP) * interp2L(data['nel'], data['Te'], np.squeeze(data['PEC'][:,:,N[i]]), Ne, Tev)
        return

    elif type == 'HmH2p':

        TiHmP = [element * 11600 for element in TiHmP]
        TiHpP = [element * 11600 for element in TiHpP]
        TiHmP = np.clip(TiHmP, min(data['TiHm']), max(data['TiHm']))
        TiHpP = np.clip(TiHpP, min(data['TiH2p']), max(data['TiH2p']))

        PECv = np.zeros((len(N), len(Ne)))
        PECv[PECv == 0] = np.nan

        for i in range(0, len(N)):
            PECv[i][:] = interp4L(data['nel'], data['TiHm'], data['TiH2p'], data['Te'], data['PEC'][:,:,:,:,N[i]], Ne, TiHmP, TiHpP, Tev)
        return


def interp2L(x, y, V, xN, yN):
    point = (np.log10(xN), np.log10(yN))
    #F = griddata((np.log10(x), np.log10(y)), np.log10(V), point)
    #return 10 ** F(np.log10(xN), np.log10(yN))
    return 10 ** griddata((np.log10(x), np.log10(y)), np.log10(V), point)


def interp4L(x, y, x1, x2, V, xN, yN, xN1, xN2):
    point = ((np.ravel(np.log10(xN)), np.ravel(np.log10(yN)), np.ravel(np.log10(xN1)), np.ravel(np.log10(xN2))))
    return 10 ** interpn((np.ravel(np.log10(x)), np.ravel(np.log10(y)), np.ravel(np.log10(x1)), np.ravel(np.log10(x2))), np.log10(V), point)

#print(TECPEC_Yacora('H2', [4], [2e19], [1], None, None))
#print(TECPEC_Yacora('H2p', [4], [2e19], [1], None, None))
#print(TECPEC_Yacora('H3p', [3], [2e19], [1], None, None))
print(TECPEC_Yacora('HmHp', [4], [2e19], [1], [2.2], [1]))
#print(TECPEC_Yacora('HmHp', 5, 2e19, 1, 2.2, 1))