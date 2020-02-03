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
from scipy.stats import linregress

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
    print("## Requête : SELECT essai_res.fichierFreq FROM essai_res JOIN essai ON essai.id=essai_res.idEssai WHERE "+where)
    cur.execute("SELECT essai_res.fichierFreq FROM essai_res JOIN essai ON essai.id=essai_res.idEssai WHERE "+where)
    tab=list(cur)
    tf=[]
    for line in tab :
        t,f = readFreq(line[0])
        tf.append((t,f))
    return averageData(tf)

def regressionExp(t,f):
    phi = lambda x,x0,a,b:a*np.exp((x-x0)*b)
    popt,pcov=curve_fit(phi, t, f,bounds=((-200,0,float("-inf")),(200,float("+inf"),0)) , p0=(0,1,-1))
    return t,np.array([phi(x,*popt) for x in t]),popt

def regressionPow(t,f):
    phi = lambda x,x0,a,b:a*(x-x0)**b
    popt,pcov=curve_fit(phi, t, f,bounds=((-10,-10000,-4),(5,10000,4)) , p0=(0,1,-1))
    return t,np.array([phi(x,*popt) for x in t]),popt

def regressionPowF(t,f,power=-1):
    phi = lambda x,x0,a : a*(x-x0)**power
    popt,pcov=curve_fit(phi, t, f,bounds=((-5,-10000),(t[0],10000)) , p0=(0,1))
    f2 = np.array([phi(x,*popt) for x in t])
    r_squared = 1 - np.sum((f-f2)**2)/np.sum((f-np.average(f))**2)
    return t,f2,*popt,r_squared

def regressionT(t,f):
    def phi(x,a1,b1,a2,b2,x1,x2):
        return ( a1*x+b1 ) * (x<=x1) + ( (a2*x2+b2-a1*x1-b1)*(x-x1)/(x2-x1) + a1*x1+b1 ) * (x1<x)*(x<x2) + ( a2*x+b2 ) * (x>=x2)
        T=1/f
    popt, pcov = curve_fit( phi, t, T, p0=(1,0,1,0,t[len(t)//2],t[-1]) )
    T2 = np.array([phi(x,*popt) for x in t])
    i_c = np.searchsorted(t,x_c)
    r1_squared = 1 - np.sum((T[:i_c]-T2[:i_c])**2)/np.sum((T[:i_c]-np.average(T[:i_c]))**2)
    r2_squared = 1 - np.sum((T[i_c:]-T2[i_c:])**2)/np.sum((T[i_c:]-np.average(T[i_c:]))**2)
    print("i_c=",i_c,"; r²=",r1_squared)
    print("i_c=",i_c,"; r²=",r2_squared)

    return t,T2,*popt



'''def regressionT(t,f):
    ## bilan des travaux : f=a/(t-t0), on choisit donc d'étudier en période et non fréquence
    r_squared_min=0.9
    r_squared_min2=0.82
    T = 1/f[:-1]
    j=len(T)
    r_value=0
    phi = lambda x,a,b : a*x+b
    while (j>0 and r_value**2<r_squared_min):
        a1,b1,r_value,p_value,std_err = linregress(t[:j],T[:j])
        j-=1
    plt.plot(t[:j],phi(t[:j],a1,b1))

    k=j
    r_value=0
    while (k<len(T)-1 and r_value**2<r_squared_min2):
        a2,b2,r_value,p_value,std_err = linregress(t[k:-1],T[k:])
        k+=1
    plt.plot(t[k:],phi(t[k:],a2,b2))

    t_c = (b2-b1)/(a1-a2)
    plt.scatter(t_c,phi(t_c,a2,b2),s=50)'''


'''def regressionPowF(t,f,power=-1):
    phi = lambda x,x0,a : a*(x-x0)**power
    slope,intercept,r_value,p_value,std_err = linregress(t[:-1],np.power(f[:-1],1/power)) # jusqu'à -1 car nul
    # print(np.power(f,1/power))
    # print(slope)
    # print(intercept)
    a = slope**p
    x0 = -intercept/slope
    return t,np.array([phi(x,x0,a) for x in t]),x0,a,r_value**2'''

