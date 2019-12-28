import csv
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal
import pywt

directory='D:/Yann/Desktop/stabien/'
filename='8x20_60g (1).csv'
delimiter='\t'

def running_mean(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return (cumsum[N:] - cumsum[:-N]) / float(N)

def running_mean_mir(x,N):
    return running_mean([x[abs(i)] if i<len(x) else x[len(x)-i-1] for i in range(-N,len(x)+N)],N)[N:len(x)+N]


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
vx = [(tab[i+1][1]-tab[i][1])/(tab[i+1][0]-tab[i][0]) for i in range(len(tab)-1)]
vy = [(tab[i+1][2]-tab[i][2])/(tab[i+1][0]-tab[i][0]) for i in range(len(tab)-1)]
v = [np.sqrt(vx[i]**2+vy[i]**2) for i in range(len(vx))]

'''sos = signal.butter(10, 20, 'hp', fs=60, output='sos')
sig = [ v[abs(i)] for i in range(-80,len(v))]
filtered = signal.sosfilt(sos, sig)[80:]'''

moy = running_mean( [v[abs(i)] if i<len(v) else v[len(v)-i-1] for i in range(-80,len(v)+80)], 80 )[80:len(v)+80]
moy2 = running_mean( [v[abs(i)] if i<len(v) else v[len(v)-i-1] for i in range(-80,len(v)+80)], 10 )[80:len(v)+80]



cwtmatr, freqs = pywt.cwt(v,np.arange(1,10),'mexh')
plt.imshow(cwtmatr, extent=[0, 1, 1, 10], cmap='PRGn', aspect='auto',vmax=abs(cwtmatr).max(), vmin=-abs(cwtmatr).max())

thres=0.05
peaks = signal.find_peaks(cwtmatr[3],height=0)[0]
peaks = [p for p in peaks if cwtmatr[-1][int(p)]>0 and cwtmatr[3][int(p)]>abs(cwtmatr).max()*thres]

for p in peaks:
    plt.axvline(x=p/len(cwtmatr[3]),alpha=0.2)

plt.figure()
periode_apparente = [tab[peaks[i+1]][0]-tab[peaks[i]][0] for i in range(len(peaks)-1)]
periode_apparente_t = [tab[peaks[i]][0] for i in range(len(periode_apparente))]
plt.plot(periode_apparente_t,periode_apparente)

#plt.plot(periode_apparente_t,running_mean_mir(periode_apparente,3)) # ça n'a pas beaucoup de sens car on moyenne pour des temps espacés irrégulièrement


plt.figure()
plt.plot(v)
'''
plt.figure()
plt.plot(t,x)
plt.plot(t,y)'''

plt.grid()
plt.show()