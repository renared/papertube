import csv
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal
import pywt
import os

directory='D:/Yann/Desktop/stabien/'

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

def find_peaks_kuhn(v,thres=0.5,graphCWT=False,graphPeaks=False):
    cwtmatr, freqs = pywt.cwt(v,np.arange(1,10),'mexh')
    peaks = signal.find_peaks(cwtmatr[3],height=0)[0]
    vpeaks = sorted([abs(cwtmatr[3][p]) for p in peaks],reverse=True)
    peaks = [p for p in peaks if cwtmatr[-1][int(p)]>0 and cwtmatr[3][int(p)]>np.average(vpeaks[2:])*thres] # np.average(vpeaks[2:len(vpeaks)//10])*thres

    if graphCWT:
        plt.figure(figsize=(25,5))
        plt.imshow(cwtmatr, extent=[0, 1, 1, 10], cmap='PRGn', aspect='auto',vmax=abs(cwtmatr).max(), vmin=-abs(cwtmatr).max())
        if graphPeaks:
            for p in peaks:
                plt.axvline(x=p/len(cwtmatr[3]),alpha=0.2)
        plt.title("thres="+str(thres))
    return peaks

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

def processDataDir(directory):
    for dirName, subdirList, fileList in os.walk(directory, topdown=False):
            for fname in fileList:
                if fname.endswith("_data.npz"):
                    npzf = np.load(os.path.join(dirName, fname))
                    t = npzf['t']
                    v = npzf['d2']
                    peaks=find_peaks_kuhn(v,thres=0.5,graphCWT=True,graphPeaks=True)
                    plt.title(fname)
                    plt.savefig(fname="../../fig_peaks_main/"+fname+"_peaks"+".png",bbox_inches='tight',pad_inches=0)
                    plt.close()
                    freq_t,freq=running_freq(t,int(t[-1]-t[0]),peaks,8)
                    plt.figure(figsize=(16,8))
                    plt.plot(freq_t,freq)
                    plt.ylim(0,5)
                    plt.ylabel("Jerk frequency (Hz)")
                    plt.xlabel("Time (s)")
                    plt.title(fname)
                    plt.savefig(fname="../../fig_freq_main/"+fname+"_freq"+".png",bbox_inches='tight',pad_inches=0)
                    plt.close()
#plt.show()

def readData(datafname):
    npzf = np.load(datafname)
    return npzf['t'], npzf['d2']