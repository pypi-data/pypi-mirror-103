import numpy as np
import pandas as pd
from scipy import signal, interpolate, spatial


#变量标准化
def snv(refle):
    if isinstance(refle, pd.core.frame.DataFrame):
        cols = refle.columns
        refle = refle.to_numpy()
    snv_values = (refle - refle.mean(axis=0).reshape(
        -1, refle.shape[1])) / refle.std(axis=0).reshape(-1, refle.shape[1])
    if 'cols' in locals().keys():
        snv_values = pd.DataFrame(snv_values)
        snv_values.columns = cols
    return snv_values


#d阶导数
def derivative(refle, windows=5, poly=3, d=1):
    if isinstance(refle, pd.core.frame.DataFrame):
        cols = refle.columns
        refle = refle.to_numpy()
    deriv = np.zeros(refle.shape, dtype=float)
    deriv[:, 0:2] = refle[:, 0:2]
    deriv[:, -2:] = refle[:, -2:]
    for j in range(refle.shape[0]):
        for i in range(2, refle.shape[1] - 2):
            x = refle[j][(i - 2):(i + 3)]
            c = signal.savgol_coeffs(windows, poly, deriv=d, use="dot")
            deriv[j, i] = c.dot(x)
    if 'cols' in locals().keys():
        deriv = pd.DataFrame(deriv)
        deriv.columns = cols
    return deriv


#多元散射校正
def msc(refle):
    if isinstance(refle, pd.core.frame.DataFrame):
        cols = refle.columns
        refle = refle.to_numpy()
    mean_values = np.mean(refle, axis=0)
    msc_value = np.zeros(refle.shape, dtype=float)
    for i in range(refle.shape[0]):
        m, b = np.polyfit(mean_values, refle[i], 1)
        msc_value[i] = (refle[i] - b) * m
    if 'cols' in locals().keys():
        msc_value = pd.DataFrame(msc_value)
        msc_value.columns = cols
    return msc_value


#连续统去除
def cr_line(refle, wavelength=range(400, 1001)):
    n_band = len(wavelength)
    refledata = pd.DataFrame({'wavelength': wavelength, 'refle': refle})
    envelope = spatial.ConvexHull(refledata)
    f1 = interpolate.interp1d(envelope.points[[0, -1], 0],
                              envelope.points[[0, -1], 1])
    filter_band = f1([envelope.vertices + wavelength[0]
                      ]) <= envelope.points[envelope.vertices, 1]
    filter_band = filter_band.ravel()
    f = interpolate.interp1d(
        envelope.points[envelope.vertices[filter_band], 0],
        envelope.points[envelope.vertices[filter_band], 1])
    return f(wavelength)

def cr(refle, wavelength=range(400, 1001), type='bd'):
    cr_lines = pd.DataFrame([])
    for i in range(refle.shape[0]):
        cr_lines[i] = cr_line(refle.iloc[i,:], wavelength)
    cr_lines.index = wavelength
    cr_lines = cr_lines.T
    
    cr_raw = refle / cr_lines
    bd = 1 - cr_raw
    bdr = bd.apply(lambda x:x/x.max(),axis=1)
    nbdi = bd.apply(lambda x:x - x.max(),axis=1) / bd.apply(lambda x:x + x.max(),axis=1)
    if type == 'raw':
        return cr_raw
    elif type == 'bd':
        return bd
    elif type == 'bdr':
        return bdr
    elif type == 'nbdi':
        return nbdi
    elif type == 'all':
        return cr_raw, bd, bdr, nbdi