## test de régressions puissance, à puissance flottante puis à puissance -1, -1.5, -2


p=-1
t,f=avgFreqDB(dureeHold=10,commentaire="var dureeHold")
t,f=t,f
t2,f2,x0,a,r2=regressionPowF(t,f,power=p)
print("f(t) =",a,"* ( t -",x0,") ^",p,"\t r²=",r2)
plt.plot(t,f,label="10 s",linestyle="dotted")
plt.plot(t2,f2, label="10 s")

t,f=avgFreqDB(dureeHold=20,commentaire="var dureeHold")
t2,f2,x0,a,r2=regressionPowF(t,f,power=p)
print("f(t) =",a,"* ( t -",x0,") ^",p,"\t r²=",r2)
plt.plot(t,f,label="20 s",linestyle="dotted")
plt.plot(t2,f2, label="20 s")

t,f=avgFreqDB(dureeHold=30,commentaire="var dureeHold")
t2,f2,x0,a,r2=regressionPowF(t,f,power=p)
print("f(t) =",a,"* ( t -",x0,") ^",p,"\t r²=",r2)
plt.plot(t,f,label="30 s",linestyle="dotted")
plt.plot(t2,f2, label="30 s")

plt.title("PowF "+str(p))
plt.legend()
plt.show()

# plt.figure()
#
# p=-1.5
# t,f=avgFreqDB(dureeHold=10,commentaire="var dureeHold")
# t2,f2,x0,a,r2=regressionPowF(t,f,power=p)
# print("f(t) =",a,"* ( t -",x0,") ^",p)
# plt.plot(t,f,label="10 s",linestyle="dotted")
# plt.plot(t2,f2, label="10 s")
#
# t,f=avgFreqDB(dureeHold=20,commentaire="var dureeHold")
# t2,f2,x0,a,r2=regressionPowF(t,f,power=p)
# print("f(t) =",a,"* ( t -",x0,") ^",p)
# plt.plot(t,f,label="20 s",linestyle="dotted")
# plt.plot(t2,f2, label="20 s")
#
# t,f=avgFreqDB(dureeHold=30,commentaire="var dureeHold")
# t2,f2,x0,a,r2=regressionPowF(t,f,power=p)
# print("f(t) =",a,"* ( t -",x0,") ^",p)
# plt.plot(t,f,label="30 s",linestyle="dotted")
# plt.plot(t2,f2, label="30 s")
#
# plt.title("PowF "+str(p))
# plt.legend()
# plt.show()
#
# plt.figure()
#
# p=-2
# t,f=avgFreqDB(dureeHold=10,commentaire="var dureeHold")
# t2,f2,x0,a,r2=regressionPowF(t,f,power=p)
# print("f(t) =",a,"* ( t -",x0,") ^",p)
# plt.plot(t,f,label="10 s",linestyle="dotted")
# plt.plot(t2,f2, label="10 s")
#
# t,f=avgFreqDB(dureeHold=20,commentaire="var dureeHold")
# t2,f2,x0,a,r2=regressionPowF(t,f,power=p)
# print("f(t) =",a,"* ( t -",x0,") ^",p)
# plt.plot(t,f,label="20 s",linestyle="dotted")
# plt.plot(t2,f2, label="20 s")
#
# t,f=avgFreqDB(dureeHold=30,commentaire="var dureeHold")
# t2,f2,x0,a,r2=regressionPowF(t,f,power=p)
# print("f(t) =",a,"* ( t -",x0,") ^",p)
# plt.plot(t,f,label="30 s",linestyle="dotted")
# plt.plot(t2,f2, label="30 s")
#
# plt.title("PowF "+str(p))
# plt.legend()
# plt.show()

