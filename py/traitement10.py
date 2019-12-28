import csv
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal
import pywt

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
t = [tab[i][0] for i in range(len(tab))]
x = [tab[i][1] for i in range(len(tab))]
y = [tab[i][2] for i in range(len(tab))]
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


## amr
coeffs = pywt.wavedec(x,'coif1')
coeffs2 = pywt.wavedec(y,'coif1')
pks_x = signal.find_peaks(coeffs[-1],distance=2)[0]
pks_y = signal.find_peaks(coeffs2[-1],distance=2)[0]

fig, ax = plt.subplots(len(coeffs)+1, sharex=True)
for j in range(len(coeffs)):
    ax[j].plot(np.linspace(t[0],t[-1],num=len(coeffs[j])),coeffs[j])
ax[-2].scatter([np.linspace(t[0],t[-1],num=len(coeffs[-1]))[int(p)] for p in pks_x], [coeffs[-1][int(p)] for p in pks_x],color='orange',s=3)
ax[-1].plot(np.linspace(t[0],t[-1],num=len(x)),x)
plt.title("AMR sur x")

fig2, ax2 = plt.subplots(len(coeffs2)+1, sharex=True)
for j in range(len(coeffs2)):
    ax2[j].plot(np.linspace(t[0],t[-1],num=len(coeffs2[j])),coeffs2[j])
ax2[-1].plot(np.linspace(t[0],t[-1],num=len(y)),y)
plt.title("AMR sur y")

pks = [pk for pk in pks_x if pk in pks_y]
tpks = [np.linspace(t[0],t[-1],num=len(coeffs[-1]))[int(pk)] for pk in pks]
periode = [tpks[i+1]-tpks[i] for i in range(len(tpks)-1)]

plt.figure()
plt.plot(tpks[:-1],periode)


plt.figure()
plt.plot(t,x)
plt.plot(t,y)

fig_a,ax_a = plt.subplots(3,sharex=True)
ax_a[0].plot(t[:-1],v)
ax_a[1].plot(np.linspace(t[0],t[-1],num=len(coeffs[-1])),coeffs[-1])
moygeo = np.sqrt(np.abs(coeffs[-1]*coeffs2[-1]))
ax_a[2].plot(np.linspace(t[0],t[-1],num=len(moygeo)),moygeo)

plt.grid()
plt.show()