import numpy as np
import pandas as pd
from scipy import signal, interpolate, spatial


#NDSI：归一化光谱指数；DSI：差值光谱指数；RSI：比值光谱指数
def ndsi_r2(refle, param, interval=5):
    r2 = pd.DataFrame([])
    refle = refle.iloc[:, range(0, refle.shape[1], interval)]
    for i in refle.columns:
        ndsi = refle.sub(refle[i], axis=0) / refle.add(refle[i], axis=0)
        r2[i] = ndsi.corrwith(param)
    r2.index = r2.columns
    return r2**2


def dsi_r2(refle, param, interval=5):
    r2 = pd.DataFrame([])
    refle = refle.iloc[:, range(0, refle.shape[1], interval)]
    for i in refle.columns:
        dsi = refle.sub(refle[i], axis=0)
        r2[i] = dsi.corrwith(param)
    r2.index = r2.columns
    return r2**2


def rsi_r2(refle, param, interval=5):
    r2 = pd.DataFrame([])
    refle = refle.iloc[:, range(0, refle.shape[1], interval)]
    for i in refle.columns:
        rsi = refle.div(refle[i], axis=0)
        r2[i] = rsi.corrwith(param)
    r2.index = r2.columns
    return r2**2


#列出n个R2最大值及其波段组合
def r2_max(r2, n=20):
    r2 = r2.stack()
    ls = list()
    for i in range(n):
        ls.append([r2.idxmax(), r2.max()])
        r2[r2.idxmax()] = 0
    return ls


def vegindex(refle, L=0.5):
    #Soil Adjusted Vegetation Index
    savi = (refle[800] - refle[670]) / (refle[800] + refle[670] + L) * (1 + L)
    #Normalized Difference NIR/Red Normalized Difference Vegetation Index, Calibrated NDVI - CDVI
    ndvi = (refle[800] - refle[680]) / (refle[800] + refle[680])

    ci = refle[675] * refle[690] / refle[683]**2
    ci2 = refle[760] / refle[700] - 1
    dd = (refle[749] - refle[720]) - (refle[701] - refle[672])
    ddn = (refle[710] - refle[660] - refle[760]) * 2
    mcari = ((refle[700] - refle[670]) - 0.2 *
             (refle[700] - refle[550])) * refle[700] / refle[670]
    mcari2 = ((refle[750] - refle[705]) - 0.2 *
              (refle[750] - refle[705])) * refle[750] / refle[705]
    osavi = 1.16 * (refle[800] - refle[670]) / (refle[800] + refle[670] + 0.16)
    osavi2 = 1.16 * (refle[750] - refle[705]) / (refle[750] + refle[705] +
                                                 0.16)
    mcari_osavi = mcari / osavi
    mcari2_osavi2 = mcari2 / osavi2
    mnd705 = (refle[750] - refle[705]) / (refle[750] + refle[705] -
                                          refle[445] * 2)
    mpri = (refle[515] - refle[530]) / (refle[515] + refle[530])
    pri = (refle[531] - refle[570]) / (refle[531] + refle[570])
    pri_ci2 = pri * ci2
    rdvi = (refle[800] - refle[670]) / np.sqrt(refle[800] + refle[670])
    pri_norm = -1 * pri / (rdvi * refle[700] / refle[670])
    ndvi3 = (refle[682] - refle[553]) / (refle[682] + refle[553])
    sr8 = refle[515] / refle[550]
    tcari = ((refle[700] - refle[670]) - 0.2 *
             (refle[700] - refle[550]) * refle[700] / refle[670]) * 3
    tcari_osavi = tcari / osavi
    tcari2 = ((refle[750] - refle[705]) - 0.2 *
              (refle[750] - refle[550]) * refle[750] / refle[705]) * 3
    tcari2_osavi2 = tcari2 / osavi2
    tgi = -0.5 * (190 * (refle[670] - refle[550]) - 120 *
                  (refle[670] - refle[480]))

    vis = pd.DataFrame({
        'ASVI': savi,
        'NDVI': ndvi,
        'CI': ci,
        'CI2': ci2,
        'DD': dd,
        'DDn': ddn,
        'MCARI': mcari,
        'MCARI2': mcari2,
        'OSAVI': osavi,
        'OSAVI2': osavi2,
        'MCARI/OSAVI': mcari_osavi,
        'MCARI2/OSAVI2': mcari2_osavi2,
        'mND705': mnd705,
        'MPRI': mpri,
        'PRI': pri,
        'PRI_norm': pri_norm,
        'PRI*CI2': pri_ci2,
        'NDVI3': ndvi3,
        'SR8': sr8,
        'TCARI': tcari,
        'TCARI2': tcari2,
        'TCARI/OSAVI': tcari_osavi,
        'TCARI2/OSAVI2': tcari2_osavi2,
        'TGI': tgi
    })
