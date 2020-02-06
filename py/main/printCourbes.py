import csv
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal
import pywt
import os
import sqlite3
import tkinter as tk
from tkinter.messagebox import *
from tkinter.simpledialog import *
from processCourbes import *


root_window = tk.Tk()
root_window.withdraw()
directory='../../'
DBfile = "../../papertube.db"
conn = sqlite3.connect(DBfile)
cur = conn.cursor()
cur2 = conn.cursor()


# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt
import numpy as np

# Fixing random state for reproducibility
np.random.seed(19680801)

conditionCourbe = ['nomPapier', 'nomCondexp', 'nomSurface', 'diametre', 'longueur', 'largeur', 'dureeHold']
pltColors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']




## On récupère les données

# on veut récupérer les données en fonction des paramètres : L,l,ratio (à créer nous meme), Rayon, Thold, surface, type de papier
#et le tracer la fréquence en fonction de ces paramètres et du temps
# t = ('A4',)
# cur.execute('SELECT * FROM essai WHERE nomPapier=?', t)
# print cur.fetchone()


def selectData1(k):
    Lparam = []
    #On commence par récupérer les différentes valeurs de paramètre
    cur.execute("SELECT "+ conditionCourbe[k] +" FROM essai GROUP BY "+ conditionCourbe[k])
    for row in cur:
        Lparam.append(row[0])
    
    
    
    FileTab = []
    for param in Lparam:
        # print("SELECT nomFichier FROM essai  WHERE "+conditionCourbe[k]+" = '"+ str(param)+"'" )
        cur.execute("SELECT nomFichier FROM essai  WHERE "+conditionCourbe[k]+" = '"+ str(param)+"'" )
        subFileTab =[] #On range les mêmes fichier dans un sous tableau
        for row in cur :
            # print(row[0])
            cur2.execute('SELECT essai_res.fichierFreq FROM essai JOIN essai_res ON essai.id = essai_res.idEssai WHERE essai.nomFichier = ?', (row[0],))
            
            # print((cur2.fetchall())[0][0])
            file = cur2.fetchall()[0][0]
            # param = row[1]
            #print(file)
            # npzf = np.load(os.path.join(directory,file))
            # print(npzf)
            t,v = readData(os.path.join(directory,file), 'freq_t','freq')
            subFileTab.append([t,v])
        FileTab.append(subFileTab)
    return FileTab, Lparam

## On affiche

def printCourbes3D1(ax, k=4):
    # On affiche tout :
    tab, Lparam = selectData1(k) 
    
    # Ou on affiche les moyennes
    # tab = avgFreqDB(conditionCourbe[k])
    # tab = avgFreqDB(nomPapier="A4",diametre=0.002)
    
    TIME=[]
    FREQ=[]
    PARAM=[Laparam for i in range(len(TIME))]
    yticks = [i for i in range(len(tab))]
    
    for i in range(len(tab)):
        for j in range(len(tab[i])):
            
            e = tab[i][j] # On récupère les coordonnées
            xts = e[0]
            ys = e[1]
            FREQ.append(ys)
            TIME.append(xts)
            # You can provide either a single color or an array with the same length as
            # xs and ys. To demonstrate this, we color the first bar of each set cyan.
            print("xts :",xts)
            cs = ['b'] * len(xts)
            #cs[0] = 'c'
            param = Lparam[i]
            # Plot the bar graph given by xs and ys on the plane y=k with 80% opacity.
            ax.plot3D(xts, ys, zs=i, zdir='y', alpha=0.8)
        # ax.bar(xts, ys, zs=param, zdir='y', color=cs, alpha=0.8)
    
    # TIME, PARAM = np.meshgrid(TIME, PARAM)
    # ax.plot_wireframe(TIME, PARAM, FREQ, rstride=10, cstride=10)
    # 
    # plt.show()
    
    # colors = ['r', 'g', 'b', 'y']
    # yticks = [3, 2, 1, 0]
    # for c, k in zip(colors, yticks):
    #     # Generate the random data for the y=k 'layer'.
    #     xs = np.arange(20)
    #     
    #     ys = np.random.rand(20)
    # 
    #     # You can provide either a single color or an array with the same length as
    #     # xs and ys. To demonstrate this, we color the first bar of each set cyan.
    #     cs = [c] * len(xs)
    #     cs[0] = 'c'
    # 
    #     # Plot the bar graph given by xs and ys on the plane y=k with 80% opacity.
    #     ax.bar(xs, ys, zs=k, zdir='y', color=cs, alpha=0.8)
    
    
    
    # 
    # 
    ax.set_xlabel('Time')
    ax.set_ylabel(conditionCourbe[k])
    ax.set_zlabel('Frequency')
    
    # On the y axis let's only label the discrete values that we have data for.
    ax.set_yticks(yticks)
    ax.set_yticklabels(Lparam)
    
    # plt.show()


    
## Avec avgFreqDB :

def selectData(k):
    Lparam = []
    #On commence par récupérer les différentes valeurs de paramètre
    cur.execute("SELECT "+ conditionCourbe[k] +" FROM essai GROUP BY "+ conditionCourbe[k])
    print("pom",conditionCourbe[k])
    for row in cur:
        Lparam.append(row[0])

    FileTab = []
    for param in Lparam:
        add = 1
        # switch = {0:   avgFreqDB(nomPapier=param),  1:   avgFreqDB(nomCondexp=param), 2:   avgFreqDB(nomSurface=param), 3:   avgFreqDB(diametre=param), 4:   avgFreqDB(longueur=param), 5:   avgFreqDB(largeur=param), 6:   avgFreqDB(dureeHold=param)}
        # Renvoie trop d'erreurs
        # switch(k){
        # 
        #     case 0:  tab = avgFreqDB(nomPapier=param); break;
        #     case 1:  tab = avgFreqDB(nomCondexp=param); break;
        #     case 2:  tab = avgFreqDB(nomSurface=param); break;
        #     case 3:  tab = avgFreqDB(diametre=param); break;
        #     case 4:  tab = avgFreqDB(longueur=param); break;
        #     case 5:  tab = avgFreqDB(largeur=param); break;
        #     case 6:  tab = avgFreqDB(dureeHold=param); break;
        # } #NE MARCHE PAS EN PYTHON
           
        # tab = switch[k]()   
        
        # if k==0:
        #     tab = avgFreqDB(nomPapier=param)
        # if k==1:
        #     tab = avgFreqDB(nomCondexp=param)
        # if k==2:
        #     tab = avgFreqDB(nomSurface=param)
        # if k==3:
        #     tab = avgFreqDB(diametre=param)
        # if k==4:
        #     tab = avgFreqDB(longueur=param)
        # if k==5:
        #     tab = avgFreqDB(largeur=param)
        # if k==6:
        #     tab = avgFreqDB(dureeHold=param)
        #    
        
        if k==0:
            if (param != 'clairefontaine'):
                tab = avgFreqDB(nomPapier=param, commentaire="var papier")
            else:
                add=0
        if k==1:
            tab = avgFreqDB(nomCondexp=param)
        if k==2:
            if (param == 'nesquik'):
                tab = avgFreqDB(nomSurface=param, largeur=0.02, commentaire="var largeur")
            elif(param == 'null'):
                tab = avgFreqDB(nomSurface=param)
            else:
                tab = avgFreqDB(nomSurface=param, commentaire="var surface")
        if k==3:
            if(param == 0.002):
                tab = avgFreqDB(diametre=param, largeur=0.03, commentaire="var largeur")
            else:
                tab = avgFreqDB(diametre=param, commentaire="var diametre")
        if k==4:
            if (param == 0.16 or param == 0.2):
                add = 0
            else:
                tab = avgFreqDB(longueur=param, commentaire="var longueur")
        if k==5:
            tab = avgFreqDB(largeur=param, commentaire="var largeur")
        if k==6:
            tab = avgFreqDB(dureeHold=param, commentaire="var dureeHold")
        
        
        
        # print(tab)
        if add:
            FileTab.append([tab[0],tab[1],tab[2]])
    
    
    return FileTab, Lparam


# FileTab = [[t,v],[t,v]] : liste des times + event


# Larger example that inserts many records at a time
# purchases = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
#              ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
#              ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
#             ]
# c.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)

# To retrieve data after executing a SELECT statement, you can either treat the cursor as an iterator, call the cursor’s fetchone() method to retrieve a single matching row, or call fetchall() to get a list of the matching rows.

# This example uses the iterator form:
# 
# >>> for row in c.execute('SELECT * FROM stocks ORDER BY price'):
#         print row
# 
# (u'2006-01-05', u'BUY', u'RHAT', 100, 35.14)
# (u'2006-03-28', u'BUY', u'IBM', 1000, 45.0)
# (u'2006-04-06', u'SELL', u'IBM', 500, 53.0)
# (u'2006-04-05', u'BUY', u'MSFT', 1000, 72.0)









## Nouvelle affichage avec avgFreqDB


def printCourbes3D(ax, k=4):
    # On affiche tout :
    tab, Lparam = selectData(k) 
    
    # Ou on affiche les moyennes
    # tab = avgFreqDB(conditionCourbe[k])
    # tab = avgFreqDB(nomPapier="A4",diametre=0.002)
    # print(tab)
    TIME=[]
    FREQ=[]
    PARAM=[Laparam for i in range(len(TIME))]
    yticks = [i for i in range(len(tab))]
    
    for i in range(len(tab)):
            
        xts, ys, yvar = tab[i] # e : tableau des [[T],[V]]
        FREQ.append(ys)
        TIME.append(xts)
        # You can provide either a single color or an array with the same length as
        # xs and ys. To demonstrate this, we color the first bar of each set cyan.
        # print(FREQ,len(FREQ))
        # print("xts :",xts)
        cs = ['b'] * len(xts)
        #cs[0] = 'c'
        param = Lparam[i]
        zs = i
        # Plot the bar graph given by xs and ys on the plane y=k with 80% opacity.
        ax.plot3D(xts, ys, zs=i, zdir='y', c=pltColors[i], alpha=0.8, label = param)
        ax.plot3D(xts, yvar, zs=i, zdir='y',c=pltColors[i], alpha=0.4, linestyle='dashed')
        # ax.contourf(xts,zs=i,[ys-yvar,ys+yvar], zdir ='y',alpha=0.2)
        # ax.bar(xts, ys, zs=param, zdir='y', color=cs, alpha=0.8)
    ax.set_title(conditionCourbe[k]) #Optionel => Déjà dans les y
    # ax.legend() #Pas besoin => Déjà dans les y
    ax.set_xlabel('Time')
    ax.set_ylabel(conditionCourbe[k])
    ax.set_zlabel('Frequency')
    
    # On the y axis let's only label the discrete values that we have data for.
    ax.set_yticks(yticks)
    ax.set_yticklabels(Lparam)
    
    # plt.show()


def printCourbes2D(dim3=0):
    fig = plt.figure()

    for k in [ u for u in range(0,len(conditionCourbe)) if u != 1 ]:
        print(k)
        tab, Lparam = selectData(k) 
        if k ==0:
            # ax = fig.add_subplot(2,(len(conditionCourbe)-1)/2+1,k+1)
            ax = fig.add_subplot(2,(len(conditionCourbe)-1)/2,k+1)
        else:
            ax = fig.add_subplot(2,(len(conditionCourbe)-1)/2,k)
        TIME=[]
        FREQ=[]
        PARAM=[Laparam for i in range(len(TIME))]
        yticks = [i for i in range(len(tab))]
        
        for i in range(len(tab)):
            # for j in range(len(tab[i])):
            
            xts, ys, yvar = tab[i] # e : tableau des [[T],[V]]
            FREQ.append(ys)
            TIME.append(xts)
            # You can provide either a single color or an array with the same length as
            # xs and ys. To demonstrate this, we color the first bar of each set cyan.=
            cs = ['b'] * len(xts)
            #cs[0] = 'c'
            param = Lparam[i]
            # # Soit on affiche la moy en freq
            # ax.plot(xts, ys, pltColors[i], alpha=0.8, label = param)
            # # ax.plot(xts, yvar, pltColors[i]+':', alpha=0.8)
            # ax.fill_between(xts,ys-yvar/2,ys+yvar/2,color = pltColors[i],alpha=0.2)
            # 
            #Soit on affiche les reg en periode
            
            xts,ys=xts[:-1],ys[:-1]
            T = 1/ys
            err = T/(1+yvar[:-1]*T)    # calcul de l'erreur sur T à partir de l'erreur sur f
            t2,T2,a1,b1,r_squared = regressionT1(xts,ys)
                        
            ax.plot(t2, T2, pltColors[i], alpha=0.8, label = param)
            # ax.fill_between(xts,ys-yvar/2,ys+yvar/2,color = pltColors[i],alpha=0.2)
                
            
        ax.set_title(conditionCourbe[k])
        ax.legend()
        ax.set_xlabel('Time')
        ax.set_ylabel('Frequency')
    
    # On the y axis let's only label the discrete values that we have data for.
    # ax.set_yticks(yticks)
    # ax.set_yticklabels(Lparam)
    # plt.tight_layout()
    plt.show()




##Affichage final

fig = plt.figure()
for k in range(len(conditionCourbe)):
    ax = fig.add_subplot(2,len(conditionCourbe)/2+1,k+1, projection='3d')
    
    printCourbes3D(ax, k)
    

plt.show()
printCourbes2D()

### Test
# fig = plt.figure()
# for k in range(4,5):
#     ax = fig.add_subplot(2,len(conditionCourbe)/2+1,k+1, projection='3d')
#     printCourbes3D(ax, k)
# plt.show()


