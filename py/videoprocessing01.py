import cv2 as cv
import numpy as np
import pywt
import scipy.signal as signal
import matplotlib.pyplot as plt

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

def diff2(im1,im2,x1,y1,x2,y2):
    s=0
    for i in range(x1,x2):
        for j in range(y1,y2):
            s+=(im2[i][j]-im1[i][j])**2
    return s
            
cap = cv.VideoCapture("D:/Dossier personnel/Desktop/stabien/8x20_60g (1).mp4")
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

pks = find_peaks(d2,thres=0,graphCWT=True,graphPeaks=True)
plt.show()