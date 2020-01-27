import cv2 as cv
import numpy as np
import pywt
import scipy.signal as signal
import matplotlib.pyplot as plt
import os

inputdir='video/'
outputdir='video_data/'


def processDir(inputdir,outputdir,squaresize=0):
    q=0 # déjà existants
    r=0 # nouveaux
    inputdir="../../"+inputdir
    outputdir="../../"+outputdir
    for dirName, subdirList, fileList in os.walk(inputdir, topdown=False):
            for fname in fileList:
                if fname.endswith(".mp4"):
                    print(fname,end=' ')
                    if os.path.isfile(outputdir+fname+"_data.npz") :
                        q+=1
                        print("already processed")
                    else :
                        print("...",end=' ')
                        full = os.path.join(dirName, fname)
                        cap = cv.VideoCapture(full)

                        ret,frame = cap.read()
                        frame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
                        fps = cap.get(cv.CAP_PROP_FPS)
                        w=cap.get(cv.CAP_PROP_FRAME_WIDTH)
                        h=cap.get(cv.CAP_PROP_FRAME_HEIGHT)
                        old_frame = frame
                        d2 = []

                        if squaresize<=0 : x1,y1,x2,y2=0,0,int(w),int(h)
                        else : x1,y1,x2,y2 = int(w/2-squaresize/2), int(h/2-squaresize/2), int(w/2+squaresize/2), int(h/2+squaresize/2)

                        while (1):
                            ret, frame = cap.read()
                            if ret==True:
                                frame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
                                d2.append(np.sum(np.square(frame[x1:x2,y1:y2]-old_frame[x1:x2,y1:y2])))
                                old_frame = frame
                            else:
                                break

                        t=np.linspace(0,(len(d2)+1)/fps,num=len(d2)+1)[1:]
                        np.savez(outputdir+"/"+fname+"_data", t=t, d2=d2)
                        r+=1
                        print("OK")
    print(q, "were already processed,",r,"new files.")