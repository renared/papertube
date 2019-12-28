import csv
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal
import pywt

directory='D:/Yann/Desktop/stabien/'
filename='3x16_70g.csv'
delimiter=';'

def running_mean(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return (cumsum[N:] - cumsum[:-N]) / float(N)

def running_mean_mir(x,N):
    return running_mean([x[abs(i)] if i<len(x) else x[len(x)-i-1] for i in range(-N,len(x)+N)],N)[N:len(x)+N]

def vitesse(t,x,y,graph=False):
    vx = [(x[i+1]-x[i])/(t[i+1]-t[i]) for i in range(len(tab)-1)]
    vy = [(y[i+1]-y[i])/(t[i+1]-t[i]) for i in range(len(tab)-1)]
    v = [np.sqrt(vx[i]**2+vy[i]**2) for i in range(len(vx))]
    v.append(v[-1])
    if graph:
        plt.figure()
        plt.plot(t,v)
        plt.title("Vitesse")
    return v

def find_peaks(v,thres=0.05,graphCWT=False,graphPeaks=False):
    cwtmatr, freqs = pywt.cwt(v,np.arange(1,10),'mexh')
    peaks = signal.find_peaks(cwtmatr[3],height=0)[0]
    peaks = [p for p in peaks if cwtmatr[-1][int(p)]>0 and cwtmatr[3][int(p)]>abs(cwtmatr).max()*thres]

    if graphCWT:
        plt.figure()
        plt.imshow(cwtmatr, extent=[0, 1, 1, 10], cmap='PRGn', aspect='auto',vmax=abs(cwtmatr).max(), vmin=-abs(cwtmatr).max())
        if graphPeaks:
            for p in peaks:
                plt.axvline(x=p/len(cwtmatr[3]),alpha=0.2)
        plt.title("thres="+str(thres))
    return peaks

def periode_apparente(t,peaks,graph=False,graphThres=None):
    per = [t[peaks[i+1]]-t[peaks[i]] for i in range(len(peaks)-1)]
    per_t = [t[peaks[i+1]] for i in range(len(per))]
    if graph:
        plt.figure()
        plt.plot(per_t,per)
        if graphThres!=None:plt.title("thres="+str(graphThres))
    return per_t,per

tab = []

with open(directory+filename, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=delimiter, quotechar='|')
    for row in spamreader:
        #print(', '.join(row))
        tab.append(row)

for i in range(2,len(tab)):
    for j in range(len(tab[i])):
        tab[i][j]=float(tab[i][j].replace(',','.'))

tab = np.array(tab[2:])
t = [tab[i][0] for i in range(len(tab))]
x = [tab[i][1] for i in range(len(tab))]
y = [tab[i][2] for i in range(len(tab))]
v = vitesse(t,x,y)
for thres in [0.02,0.05,0.01,0.02,0.03,0.04,0.05,0.1]:
    peaks=find_peaks(v,thres=thres)
    periode_apparente(t,peaks,graph=True,graphThres=thres)


plt.show()