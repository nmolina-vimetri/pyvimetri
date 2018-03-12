
import statistics as std
import numpy as np

def correlation(data, mask):
    re = data - np.nanmedian(data)
    corr = np.convolve(re, mask, 'same')
    xer = -re[:] + corr[:]
    rer0 = re - np.nanmedian(re)
    out0 = -xer + np.nanmedian(xer)
    return rer0, out0

def threshold_limit(data, threshold, value):
    for k in range(1, len(data)):
        if data[k] <= threshold:
           out[k] = value
        else:
           out[k] = data[k]
    return out

def init_matrix(rain):
    mtx_init = []
    a, b = rain.shape
    row =  4 * b
    column =int(len(rain)/4)
    for a in range(row):
        mtx_init.append([])
        for b in range(column):
            mtx_init[a].append(1)
    return mtx_init

def aperture(data, window):
    ers = erosion(data, window)
    return dilation(ers, window)

def closure(data, window):
    dlt = dilation(data, window)
    return erosion(dlt, window)

def erosion(data, window):
    xer = []
    ls = len(data)
    p1 = window-1
    p2 = p1/2
    a = np.zeros((1, ls+p1))
    a[p2+1:s+p2] = data
    for i in range(1, p2):
        a[i] = data[1]
    for j in range(1, p2):
        a[s+j+p2] = data[s]
    b = np.zeros(1, window)
    for i in range(p2+1, s+p2):
        for j in range(0, p2):
            b[j+1] = a[i+j]
        for j in range(1, p2):
            b[j+(p2+1)] = a[i-j]
        z = min(b)
        xer[i-p2] = z
    return xer

def dilation(data, nsample):
    xdl = []
    ls = len(data)
    w1 = nsample-1
    w2 = w1/2
    a = np.zeros(1, ls+w1)
    a[w2+1:ls+w2] = data
    for i in range(1, w2):
        a[i] = data[1]
    for j in range(1, w2):
        a[ls+j+w2] = data[ls]
    b = np.zeros(1, nsample)
    for i in range(w2+1, ls+w2):
        for j in range(0, w2):
            b[j+1] = a[i+j]
        for j in range(1, w2):
            b[j+(w2+1)] = a[i-j]
        z = max(b)
        xdl[i-w2] = z
    return xdl

def downhat(data, window):
    cls = closure(data, window)
    return data[:]-cls[:]

def tophat(data, window):
    apt = aperture(data, window)
    return data[:]-apt[:]

def rsl_normalization(x):
    aux = []
    mean_rsl = std.mean(x)
    std_rsl = std.stdev(x)
    for k in range(0, len(x)):
        rsl = (x[k] - mean_rsl)/std_rsl
        aux.append(abs(rsl))
    return aux