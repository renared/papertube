## test regressionT1

t,f=avgFreqDB(dureeHold=10,commentaire="var dureeHold")
t,f=t[:-1],f[:-1]
T = 1/f
t2,T2,a1,b1,r_squared = regressionT1(t,f)
# t2,f2,x0,a,r2=regressionPowF(t,f,power=p)
print("coeffs a1=",a1,"; r²=",r_squared)
plt.plot(t,T,label="10 s",linestyle="dotted")
plt.plot(t2,T2, label="10 s")

t,f=avgFreqDB(dureeHold=20,commentaire="var dureeHold")
t,f=t[:-1],f[:-1]
T = 1/f
t2,T2,a1,b1,r_squared = regressionT1(t,f)
# t2,f2,x0,a,r2=regressionPowF(t,f,power=p)
print("coeffs a1=",a1,"; r²=",r_squared)
plt.plot(t,T,label="20 s",linestyle="dotted")
plt.plot(t2,T2, label="20 s")

t,f=avgFreqDB(dureeHold=30,commentaire="var dureeHold")
t,f=t[:-1],f[:-1]
T = 1/f
t2,T2,a1,b1,r_squared = regressionT1(t,f)
# t2,f2,x0,a,r2=regressionPowF(t,f,power=p)
print("coeffs a1=",a1,"; r²=",r_squared)
plt.plot(t,T,label="30 s",linestyle="dotted")
plt.plot(t2,T2, label="30 s")

plt.legend()
plt.show()
