import csv
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal

def normalize_2d(l):
    l = np.array(l)
    minamp = np.amin(l)
    maxamp = np.amax(l)
    return (l-minamp)/(maxamp-minamp)

def spectrogram(s, sampFreq, fftsize=8192, overlap=0.25):
    chunklen = fftsize/(1+overlap)
    n_chunks = 0
    window = signal.blackmanharris(fftsize)
    chunks = []
    t = []
    a = 0
    amax = len(s)-fftsize
    while (a <= amax):
        b = a+fftsize
        t.append(a/sampFreq)
        chunks.append(20*np.log10( np.maximum([0.004 for i in range(fftsize//2+1)],np.abs(np.fft.rfft(window*s[a:b])))))
        n_chunks+=1
        a = b - int(overlap*fftsize)
    f = np.fft.rfftfreq(fftsize,1/sampFreq)
    chunks = normalize_2d(chunks)
    return np.array(t),np.array(f),np.array(chunks)

def running_mean(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return (cumsum[N:] - cumsum[:-N]) / float(N)


tab = []

with open('D:/Yann/Desktop/stabien/8x20_60g (1).csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
    for row in spamreader:
        #print(', '.join(row))
        tab.append(row)

for i in range(2,len(tab)):
    for j in range(3):
        tab[i][j]=float(tab[i][j].replace(',','.'))

tab = np.array(tab[2:])
vx = [(tab[i+1][1]-tab[i][1])/(tab[i+1][0]-tab[i][0]) for i in range(len(tab)-1)]
vy = [(tab[i+1][2]-tab[i][2])/(tab[i+1][0]-tab[i][0]) for i in range(len(tab)-1)]
v = [np.sqrt(vx[i]**2+vy[i]**2) for i in range(len(vx))]

'''sos = signal.butter(10, 20, 'hp', fs=60, output='sos')
sig = [ v[abs(i)] for i in range(-80,len(v))]
filtered = signal.sosfilt(sos, sig)[80:]'''

moy = running_mean( [v[abs(i)] if i<len(v) else v[len(v)-i-1] for i in range(-80,len(v)+80)], 80 )[80:len(v)+80]
moy2 = running_mean( [v[abs(i)] if i<len(v) else v[len(v)-i-1] for i in range(-80,len(v)+80)], 10 )[80:len(v)+80]

#plt.plot([x[0] for x in tab][:-1], v)
#plt.plot([x[0] for x in tab][:-1], moy2-moy)
#plt.plot([x[0] for x in tab][:-1], moy2)

thresholded = [0.02 if moy2[i]-moy[i]>0.002 else 0 for i in range(len(moy))]
#plt.plot([x[0] for x in tab][:-1], thresholded)

#pks,_ = signal.find_peaks(moy2,height=0.002,distance=0.2/(tab[1][0]-tab[0][0]))
#plt.scatter([tab[x][0] for x in pks], [moy2[x] for x in pks])

pks = signal.find_peaks_cwt(v,[3])
threshold=0.002
pks = [p for p in pks if moy2[p]>=threshold]
#plt.scatter([tab[x][0] for x in pks], [moy2[x] for x in pks],color='red')
periode_apparente = [tab[pks[i+1]][0]-tab[pks[i]][0] for i in range(len(pks)-1)]
plt.plot([tab[pks[i]][0] for i in range(len(periode_apparente))],periode_apparente)

plt.grid()
plt.show()