import sqlite3
import os
from time import time


DBfile = "../../papertube.db"
conn = sqlite3.connect(DBfile)
cur = conn.cursor()

def intoDB(directory,copy=[]):
    '''exemple : copy=['nomFichier','nomPapier','nomSurface'] # nomFichier en premier !!
    '''
    if len(copy)>0:
        cur.execute("SELECT COUNT(*) FROM essai WHERE nomFichier=?",(copy[0],))
        if list(cur)[0][0] > 0 :
            def sumStr(l):
                s=""
                for x in l:
                    s+=l
                    s+=','
                return s[:-1]
            buf = sumStr(copy)
            cur.execute("SELECT ? FROM essai WHERE nomFichier=?",(buf,copy[0]))
        else : print("Le fichier copy[0] n'existe pas dans la DB.")

    m,n = 0,0
    entree = {}
    for field in ["nomPapier","nomCondexp","nomSurface","diametre","longueur","largeur","dureeHold","commentaire"]:
        print(field,":")
        entree[field]=copy[field] if field in copy else input()
    for dirName, subdirList, fileList in os.walk("../../"+directory, topdown=False):
        for fname in fileList:
            if fname.endswith(".npz"):
                cur.execute("SELECT COUNT(*) FROM essai WHERE nomFichier=?", (directory+fname,))
                if list(cur)[0][0] > 0 :
                    print(os.path.join(dirName, fname),"déjà dans la BD")
                    m+=1
                else :
                    print("Importation de",os.path.join(dirName, fname))
                    cur.execute("INSERT INTO essai(nomFichier,nomPapier,nomCondexp,nomSurface,diametre,longueur,largeur,dureeHold,commentaire) VALUES(?,?,?,?,?,?,?,?,?)",(directory+fname,entree['nomPapier'],entree['nomCondexp'],entree['nomSurface'],float(entree['diametre']),float(entree['longueur']),float(entree['largeur']),float(entree['dureeHold']),entree['commentaire']))
                    conn.commit()
                    n+=1
    print(m,"musiques étaient déjà importées dans la BD")
    print(n,"musiques ont bien été importées dans la BD")
