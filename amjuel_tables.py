import numpy as np
import math
from mat4py import loadmat

mat = loadmat('get_amjuel (4).mat')
print(mat["AMJ"].keys())




def amjuel_tables(type, table, ne, te):

    # limit grid for YACORA interpolation
    if te < 1:
        te = 1
    if te > 20:
        te = 20
    if ne < 5e18:
        ne = 5e18
    if ne > 1.5e20:
        ne = 1.5e20

    if type == "h4":
        sigmav = h4_rate(table, ne, te)
        return sigmav
    elif type == "h2":
        sigmav = h2_rate(table, te)
        return sigmav
    elif type == "h11":
        sigmav = h11_rate(table, te)
        return sigmav
    elif type == "h12":
        sigmav = h12_rate(table, ne, te)
        return sigmav


def h4_rate(h4_table, ne, Te):
    try:
        mat["AMJ"][h4_table]["table"]
    except KeyError:
        sigmav = math.nan
        return sigmav

    ne = ne/1e6
    temp = 0
    for i in range(0, 9):
        for j in range(0, 9):
            temp = temp + mat["AMJ"][h4_table]["table"][i][j]*(np.log(Te)**i)*(np.log(ne/1e8)**j)
    sigmav = 1e-6*np.exp(temp)
    return sigmav


def h2_rate(h2_table, Te):
    try:
        mat["AMJ"][h2_table]["table"]
    except KeyError:
        sigmav = math.nan
        return sigmav

    temp = 0
    for i in range(0, 9):
        temp = temp + mat["AMJ"][h2_table]["table"][i]*(np.log(Te)**i)
    sigmav = 1e-6*(np.exp(temp))
    return sigmav


def h11_rate(h11_table, Te):
    try:
        mat["AMJ"][h11_table]["table"]
    except KeyError:
        ratio = math.nan
        return ratio

    total = 0
    for i in range(0, 9):
        total = total + (mat["AMJ"][h11_table]["table"][i] * (np.log(Te) ** i))
    ratio = np.exp(total)
    return ratio


def h12_rate(h12_table, ne, Te):
    try:
        mat["AMJ"][h12_table]["table"]
    except KeyError:
        ratio = math.nan
        return ratio

    ne = ne/1e6
    total = 0
    for i in range(0, 9):
        for j in range(0, 9):
            total = total + mat["AMJ"][h12_table]["table"][i][j]*(np.log(Te)**i)*(np.log(ne/1e8)**j)
    ratio = np.exp(total)
    return ratio
