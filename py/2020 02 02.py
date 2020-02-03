t,f=avgFreqDB(dureeHold=10,commentaire="var dureeHold")
t2,f2,popt=regression(t,f,fonction="pow")
plt.plot(t,f,label="10 s",linestyle="dotted")
plt.plot(t2,f2, label="10 s")

t,f=avgFreqDB(dureeHold=20,commentaire="var dureeHold")
t2,f2,popt=regression(t,f,fonction="pow")
plt.plot(t,f,label="20 s",linestyle="dotted")
plt.plot(t2,f2, label="20 s")

t,f=avgFreqDB(dureeHold=30,commentaire="var dureeHold")
t2,f2,popt=regression(t,f,fonction="pow")
plt.plot(t,f,label="30 s",linestyle="dotted")
plt.plot(t2,f2, label="30 s")

plt.legend()
plt.show()
