import cv2 as cv
import numpy as np
import pywt
import scipy.signal as signal
import matplotlib.pyplot as plt
FNAME = "D:/Dossier personnel/Desktop/stabien/8x20_60g (1).mp4"
FPS = 60

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
            
cap = cv.VideoCapture(FNAME)
ret,frame = cap.read()
frame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
old_frame = frame
d2 = []
while (1):
    ret, frame = cap.read()
    if ret==True:
        frame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
        #cv.imshow('frame',frame)
        #cv.waitKey(int(1/120*1000))
        #d2.append(diff2(frame,old_frame,500,600,700,800))
        d2.append(np.sum(np.square(frame[439:600,762:913]-old_frame[439:600,762:913])))
        old_frame = frame
    else:
        break

t=np.linspace(0,(len(d2)+1)/FPS,num=len(d2)+1)
peaks = find_peaks(d2,thres=0.01,graphCWT=True,graphPeaks=True)
freq_t,freq=running_freq(t,int(t[-1]-t[0]),peaks,10)
plt.figure()
plt.plot(freq_t,freq)
plt.show()