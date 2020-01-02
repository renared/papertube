import csv
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal
import pywt
import os

## dernier usage : ajustement find_peaks_kuhn, test seuils /fig_peaks1/ /fig_freq1/

directory='D:/Yann/Desktop/stabien/'
filename='8x20_60g (1).csv'
delimiter=';'

def read_csv(filepath, delimiter):
    tab = []
    with open(filepath, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=delimiter, quotechar='|')
        for row in spamreader:
            tab.append(row)
    tab = tab[2:]
    for i in range(len(tab)):
        for j in range(len(tab[0])):
            tab[i][j]=float(tab[i][j].replace(',','.'))
    return np.array(tab)

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
        plt.figure(figsize=(25,5))
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

def nombre_pics_porte(t,peaks,t0,T):
    n=0
    for p in peaks:
        if t0-T/2<t[p]<t0+T/2:
            n+=1
    return n

def running_freq(t,num,peaks,T):
    f_t = np.linspace(t[0]+T/2,t[-1]-T/2,num=num)
    f = [nombre_pics_porte(t,peaks,t0,T)/T for t0 in f_t]
    return f_t, f

def find_peaks_kuhn(v,thres=0.05,graphCWT=False,graphPeaks=False):
    cwtmatr, freqs = pywt.cwt(v,np.arange(1,10),'mexh')
    peaks = signal.find_peaks(cwtmatr[3],height=0)[0]
    vpeaks = sorted([abs(cwtmatr[3][p]) for p in peaks],reverse=True)
    peaks = [p for p in peaks if cwtmatr[-1][int(p)]>0 and cwtmatr[3][int(p)]>np.average(vpeaks)*thres]

    if graphCWT:
        plt.figure(figsize=(25,5))
        plt.imshow(cwtmatr, extent=[0, 1, 1, 10], cmap='PRGn', aspect='auto',vmax=abs(cwtmatr).max(), vmin=-abs(cwtmatr).max())
        if graphPeaks:
            for p in peaks:
                plt.axvline(x=p/len(cwtmatr[3]),alpha=0.2)
        plt.title("thres="+str(thres))
    return peaks

# tab = read_csv(directory+filename, delimiter)
#
# #tab = np.array(tab[2:])
# t = [tab[i][0] for i in range(len(tab))]
# x = [tab[i][1] for i in range(len(tab))]
# y = [tab[i][2] for i in range(len(tab))]
# v = vitesse(t,x,y)
# for thres in [0.01]:
#     peaks=find_peaks(v,thres=thres,graphCWT=True,graphPeaks=True)
#     periode_apparente(t,peaks,graph=True,graphThres=thres)

for dirName, subdirList, fileList in os.walk(directory, topdown=False):
        for fname in fileList:
            if fname.endswith(".csv"):
                tab = read_csv(os.path.join(dirName, fname), delimiter)
                t = [tab[i][0] for i in range(len(tab))]
                x = [tab[i][1] for i in range(len(tab))]
                y = [tab[i][2] for i in range(len(tab))]
                v = vitesse(t,x,y)
                for thres in [0.01,0.02,0.05,0.1,0.15,0.25,0.4,0.5]:
                    peaks=find_peaks_kuhn(v,thres=thres,graphCWT=True,graphPeaks=True)
                    plt.title(fname+" ; thres="+str(thres))
                    plt.savefig(fname=directory+"fig_peaks1/"+fname+"_freq"+str(int(thres*100))+".png",bbox_inches='tight',pad_inches=0)
                    #per_t,per=periode_apparente(t,peaks)
                    freq_t,freq=running_freq(t,int(t[-1]-t[0]),peaks,10)
                    plt.figure()
                    #plt.scatter(per_t,per,c=per_t,cmap='plasma')
                    plt.plot(freq_t,freq)
                    plt.ylim(0,3)
                    plt.ylabel("Jerk frequency (Hz)")
                    plt.xlabel("Time (s)")
                    plt.title(fname+" ; thres="+str(thres))
                    plt.savefig(fname=directory+"fig_freq1/"+fname+"_freq"+str(int(thres*100))+".png",bbox_inches='tight',pad_inches=0)
                    plt.close()
#plt.show()