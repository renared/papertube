import csv
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal
import pywt
import os
import sqlite3
import tkinter as tk
from tkinter.messagebox import *
from tkinter.simpledialog import *
from scipy.optimize import curve_fit

root_window = tk.Tk()
root_window.withdraw()
directory='../../'
DBfile = "../../papertube.db"
conn = sqlite3.connect(DBfile)
cur = conn.cursor()

def find_peaks(v,thres=0.05,graphCWT=False,graphPeaks=False):
    cwtmatr, freqs = pywt.cwt(v,np.arange(1,10),'mexh')
    peaks = signal.find_peaks(cwtmatr[3],height=0)[0]
    peaks = [p for p in peaks if cwtmatr[-1][int(p)]>0 and cwtmatr[3][int(p)]>abs(cwtmatr).max()*thres]

    if graphCWT:
        plt.figure(figsize=(18,4))
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
        plt.figure(figsize=(18,4))
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

def processDataDir_old(directory):
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

def processDataDir(directory,freqdir="res/freq/",fig_peaks_dir="fig_peaks_main/",fig_freq_dir="fig_freq_main/"):
    for dirName, subdirList, fileList in os.walk("../../"+directory, topdown=False):
            for fname in fileList:
                if fname.endswith("_data.npz"):
                    cur.execute("SELECT id FROM essai WHERE nomFichier=?",(directory+fname,))
                    l = list(cur)
                    if len(l)==0 :
                        print("Le fichier d'essai correspondant à",fname,"n'a pas préalablement été importé.")
                    else :
                        if len(l)>1 : print("Attention, plusieurs essais ont le même nom de fichier (",fname,").")
                        print("Fichier :",fname)
                        npzf = np.load(os.path.join(dirName, fname))
                        t = npzf['t']
                        v = npzf['d2']
                        peaks=find_peaks_kuhn(v,thres=0.5,graphCWT=True,graphPeaks=True)
                        plt.title(fname)
                        fig=plt.gcf()
                        plt.show()
                        plt.pause(1)
                        while (not(askyesno(fname,"La détection des pics est-elle correcte ?"))):
                            plt.close()
                            s = askfloat(fname,"Choisir un seuil",minvalue=0.0,maxvalue=1.0)
                            peaks=find_peaks(v,thres=s,graphCWT=True,graphPeaks=True)
                            plt.title(fname)
                            fig=plt.gcf()
                            plt.show()
                            plt.pause(1)
                        if fig_peaks_dir!=None : fig.savefig(fname="../../"+fig_peaks_dir+fname+"_peaks"+".png",bbox_inches='tight',pad_inches=0)
                        plt.close()
                        freq_t,freq=running_freq(t,int(t[-1]-t[0]),peaks,14)
                        if fig_freq_dir!=None:
                            plt.figure(figsize=(16,8))
                            plt.plot(freq_t,freq)
                            plt.ylim(0,3)
                            plt.ylabel("Jerk frequency (Hz)")
                            plt.xlabel("Time (s)")
                            plt.title(fname)
                            plt.savefig(fname="../../"+fig_freq_dir+fname+"_freq"+".png",bbox_inches='tight',pad_inches=0)
                        plt.close()
                        try:
                            os.makedirs("../../"+freqdir)
                        except:
                            pass
                        np.savez("../../"+freqdir+fname+"_freq",freq_t=freq_t,freq=freq)
                        if os.path.exists("../../"+freqdir+fname+"_freq"+".npz"):
                            cur.execute("INSERT INTO essai_res(idEssai,fichierFreq) VALUES(?,?)",(l[0][0],freqdir+fname+"_freq"+".npz"))
                            conn.commit()
                        else:
                            print("N'a pas correctement sauvegardé",fname+"_freq.npz")


def readData(datafname,t="t",sig="d2"):
    npzf = np.load(datafname)
    return npzf[t], npzf[sig]
def readFreq(path):
    t,f = readData("../../"+path,t="freq_t",sig="freq")
    for i in range(len(f)):
            if f[i]==0.:
                t = t[:i+1]
                f = f[:i+1]
                break
    return t,f


def plotFreq(dir,plotAll=True,plotAvg=True):
    tf = []
    for dirName, subdirList, fileList in os.walk("../../"+dir, topdown=False):
            for fname in fileList:
                if fname.endswith("_freq.npz"):
                    t,f = readFreq(dir+fname)
                    if plotAvg:tf.append((t,f))
                    if plotAll:plt.plot(t,f)
    if plotAvg:
        t2,f2 = averageData(tf)
        plt.plot(t2,f2)

def avgFreq(dir):
    tf = []
    for dirName, subdirList, fileList in os.walk("../../"+dir, topdown=False):
            for fname in fileList:
                if fname.endswith("_freq.npz"):
                    t,f = readFreq(dir+fname)
                    tf.append((t,f))
    t2,f2 = averageData(tf)
    return t2,f2

def processDataDirPlus(*subfolders_of_video_data):
    for sub in subfolders_of_video_data:
        s = "" if sub.endswith("/") else "/"
        processDataDir("video_data/"+sub+s,"res/freq/"+sub+s)

def averageData(l):
    '''
     args : tuples (t,sig)
     10 Hz
    '''
    m=float("+inf")
    M=float("-inf")
    Hz=0
    for t,f in l:
        if (t[0]<m) : m=t[0]
        if (t[-1]>M) : M=t[-1]
        c = len(t)/(t[-1]-t[0])
        if c>Hz:Hz=c
    t2 = np.linspace(m,M,num=int(Hz*(M-m)))
    moy=[0 for x in t2]
    for t,f in l:
        for i in range(len(t2)):
            moy[i]+=np.interp(t2[i],t,f,right=0.0)
    return t2, np.array(moy)/len(l)

def avgFreqDB(**kwargs):
    ## exemple : avgFreqDB(nomPapier="A4",diametre=0.002)
    nomFichier = kwargs.get('nomFichier',None)
    nomPapier = kwargs.get("nomPapier",None)
    nomCondexp = kwargs.get("nomCondexp",None)
    nomSurface = kwargs.get("nomSurface",None)
    diametre = kwargs.get("diametre",None)
    longueur = kwargs.get("longueur",None)
    largeur = kwargs.get("largeur",None)
    dureeHold = kwargs.get("dureeHold",None)
    commentaire = kwargs.get("commentaire",None)

    where=""
    if nomFichier!=None:where+=" AND essai.nomFichier='"+nomFichier+"'"
    if nomPapier!=None:where+=" AND essai.nomPapier='"+nomPapier+"'"
    if nomCondexp!=None:where+=" AND essai.nomCondexp='"+nomCondexp+"'"
    if nomSurface!=None:where+=" AND essai.nomFichier='"+nomSurface+"'"
    if diametre!=None:where+=" AND essai.diametre="+str(diametre)
    if longueur!=None:where+=" AND essai.longueur="+str(longueur)
    if largeur!=None:where+=" AND essai.largeur="+str(largeur)
    if dureeHold!=None:where+=" AND essai.dureeHold="+str(dureeHold)
    if commentaire!=None:where+=" AND essai.commentaire='"+commentaire+"'"
    where=where[5:]
    print("Requête : SELECT essai_res.fichierFreq FROM essai_res JOIN essai ON essai.id=essai_res.idEssai WHERE "+where)
    cur.execute("SELECT essai_res.fichierFreq FROM essai_res JOIN essai ON essai.id=essai_res.idEssai WHERE "+where)
    tab=list(cur)
    tf=[]
    for line in tab :
        t,f = readFreq(line[0])
        tf.append((t,f))
    return averageData(tf)

def regression(t,f,fonction="exp"):
    if fonction=="exp":
        phi = lambda x,x0,a,b:a*np.exp((x-x0)*b)
        popt,pcov=curve_fit(phi, t, f,bounds=((-100,0,float("-inf")),(100,float("+inf"),0)) , p0=(0,1,-1))
    elif fonction=="pow":
        phi = lambda x,x0,a,b:a*(x-x0)**b
        popt,pcov=curve_fit(phi, t, f,bounds=((-100,float("-inf"),float("-inf")),(100,float("+inf"),float("+inf"))) , p0=(0,1,-1))
    return t,np.array([phi(x,popt[0],popt[1],popt[2]) for x in t]),popt