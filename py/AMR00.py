import matplotlib.pyplot as plt
from scipy.io import wavfile as wav
from scipy import signal
import numpy as np
import sqlite3
import os
import pywt

CHUNK_SIZE = len(x)
CHUNK_OVERLAP = 0
PEAK_MIN_DIST = 0.1
PEAK_THRESHOLD = 0.2

def downsample(s, factor):
    return [s[i] for i in range(0,len(s),factor)]

def mix_channels(s):
    s = np.array(s).transpose()
    return (s[0]+s[1])/2

def normalize(s):
    l = np.array(s)
    minamp = np.amin(l)
    maxamp = np.amax(l)
    return 2*l/(maxamp-minamp)

def chunks(s, sampFreq, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunklen = size/(1+overlap)
    n_chunks = 0
    chunks = []
    t = []
    a = 0
    amax = len(s)-size
    s = normalize(s)
    while (a <= amax):
        b = a+size
        t.append(a/sampFreq)
        chunks.append( pywt.wavedec(s[a:b], "coif1")[1:] )
        n_chunks+=1
        a = b - int(overlap*size)
    return chunks

def peaks(chunks):
    chunks_scales_maxima = []
    for chunk in chunks:
        scales_maxima = []
        for scale in chunk:
            maxima = []
            sortedscale = sorted( [(i, abs(scale[i])) for i in range(len(scale))] ,key=lambda x: x[1],reverse=True)
            i = 0
            while len(maxima)<4 and i < len(scale):
                x = sortedscale[i][1]
                if x>=PEAK_THRESHOLD and CHUNK_OVERLAP/2 <= i/len(scale) <= 1-CHUNK_OVERLAP/2 :
                    cond = True
                    for j, y in maxima:
                        if abs(i-j)/len(scale) < 0.1 :
                            cond = False
                            break
                    if cond : maxima.append( (i, x) )
                i+=1
            scales_maxima.append(maxima)
        chunks_scales_maxima.append(scales_maxima)
        print(scales_maxima)
    pks = []
    for j in range(len(chunks_scales_maxima[0])) :
        l = []
        a = 0
        for k in range(len(chunks_scales_maxima)):
            b = a+CHUNK_SIZE
            l += [ ( x[0]+a, x[1] ) for x in chunks_scales_maxima[k][j] ]
            a = b - int(CHUNK_OVERLAP*CHUNK_SIZE)
        pks.append(l)
    return pks



#sampFreq, snd = wav.read('E:\\anthem_frag.wav')
snd0=signal.resample_poly(x,4,1)
sampFreq=60*4
sxx = chunks(snd0, sampFreq)
#plt.plot([tab[i][0] for i in range(len(v))],v)
#plt.plot(np.linspace(tab[0][0],tab[-1][0],num=len(snd0)),snd0)


#cA, cD = pywt.dwt(snd0, "coif1", levels=2)
l = pywt.wavedec(snd0, "coif1")
l = sxx[3]

fig, ax = plt.subplots(len(l)+1, sharex=True)
for j in range(len(l)):
    ax[j].plot(np.linspace(0,1,num=len(l[j])),l[j])
ax[-1].plot(np.linspace(0,1,num=len(x)),x)

plt.show()
#pks = peaks(sxx)