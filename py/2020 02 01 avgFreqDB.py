t,f=avgFreqDB(dureeHold=10,commentaire="var dureeHold")
plt.plot(t,f,label="10 s")
t,f=avgFreqDB(dureeHold=20,commentaire="var dureeHold")
plt.plot(t,f,label="20 s")
t,f=avgFreqDB(dureeHold=30,commentaire="var dureeHold")
plt.plot(t,f,label="30 s")
plt.legend()
plt.show()
