## test de régressions puissance, à puissance flottante puis à puissance -1, -1.5, -2

t,f=avgFreqDB(dureeHold=10,commentaire="var dureeHold")
t2,f2,popt=regressionPow(t,f)
print("f(t) =",popt[1],"* ( t -",popt[0],") ^",popt[2])
plt.plot(t,f,label="10 s",linestyle="dotted")
plt.plot(t2,f2, label="10 s")

t,f=avgFreqDB(dureeHold=20,commentaire="var dureeHold")
t2,f2,popt=regressionPow(t,f)
print("f(t) =",popt[1],"* ( t -",popt[0],") ^",popt[2])
plt.plot(t,f,label="20 s",linestyle="dotted")
plt.plot(t2,f2, label="20 s")

t,f=avgFreqDB(dureeHold=30,commentaire="var dureeHold")
t2,f2,popt=regressionPow(t,f)
print("f(t) =",popt[1],"* ( t -",popt[0],") ^",popt[2])
plt.plot(t,f,label="30 s",linestyle="dotted")
plt.plot(t2,f2, label="30 s")

plt.title("Pow")
plt.legend()
plt.show()

plt.figure()

p=-1
t,f=avgFreqDB(dureeHold=10,commentaire="var dureeHold")
t2,f2,popt=regressionPowF(t,f,power=p)
print("f(t) =",popt[1],"* ( t -",popt[0],") ^",p)
plt.plot(t,f,label="10 s",linestyle="dotted")
plt.plot(t2,f2, label="10 s")

t,f=avgFreqDB(dureeHold=20,commentaire="var dureeHold")
t2,f2,popt=regressionPowF(t,f,power=p)
print("f(t) =",popt[1],"* ( t -",popt[0],") ^",p)
plt.plot(t,f,label="20 s",linestyle="dotted")
plt.plot(t2,f2, label="20 s")

t,f=avgFreqDB(dureeHold=30,commentaire="var dureeHold")
t2,f2,popt=regressionPowF(t,f,power=p)
print("f(t) =",popt[1],"* ( t -",popt[0],") ^",p)
plt.plot(t,f,label="30 s",linestyle="dotted")
plt.plot(t2,f2, label="30 s")

plt.title("PowF "+str(p))
plt.legend()
plt.show()

plt.figure()

p=-1.5
t,f=avgFreqDB(dureeHold=10,commentaire="var dureeHold")
t2,f2,popt=regressionPowF(t,f,power=p)
print("f(t) =",popt[1],"* ( t -",popt[0],") ^",p)
plt.plot(t,f,label="10 s",linestyle="dotted")
plt.plot(t2,f2, label="10 s")

t,f=avgFreqDB(dureeHold=20,commentaire="var dureeHold")
t2,f2,popt=regressionPowF(t,f,power=p)
print("f(t) =",popt[1],"* ( t -",popt[0],") ^",p)
plt.plot(t,f,label="20 s",linestyle="dotted")
plt.plot(t2,f2, label="20 s")

t,f=avgFreqDB(dureeHold=30,commentaire="var dureeHold")
t2,f2,popt=regressionPowF(t,f,power=p)
print("f(t) =",popt[1],"* ( t -",popt[0],") ^",p)
plt.plot(t,f,label="30 s",linestyle="dotted")
plt.plot(t2,f2, label="30 s")

plt.title("PowF "+str(p))
plt.legend()
plt.show()

plt.figure()

p=-2
t,f=avgFreqDB(dureeHold=10,commentaire="var dureeHold")
t2,f2,popt=regressionPowF(t,f,power=p)
print("f(t) =",popt[1],"* ( t -",popt[0],") ^",p)
plt.plot(t,f,label="10 s",linestyle="dotted")
plt.plot(t2,f2, label="10 s")

t,f=avgFreqDB(dureeHold=20,commentaire="var dureeHold")
t2,f2,popt=regressionPowF(t,f,power=p)
print("f(t) =",popt[1],"* ( t -",popt[0],") ^",p)
plt.plot(t,f,label="20 s",linestyle="dotted")
plt.plot(t2,f2, label="20 s")

t,f=avgFreqDB(dureeHold=30,commentaire="var dureeHold")
t2,f2,popt=regressionPowF(t,f,power=p)
print("f(t) =",popt[1],"* ( t -",popt[0],") ^",p)
plt.plot(t,f,label="30 s",linestyle="dotted")
plt.plot(t2,f2, label="30 s")

plt.title("PowF "+str(p))
plt.legend()
plt.show()

