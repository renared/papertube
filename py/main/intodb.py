import sqlite3
import os


DBfile = "D:/Yann/Desktop/stabien/papertube.db"
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
    t1 = time()
    for dirName, subdirList, fileList in os.walk(directory, topdown=False):
        for fname in fileList:
            if fname.endswith(".mp4") or fname.endswith(".m4v"):
                entree = {}
                for field in ["nomPapier","nomCondexp","nomSurface","diametre","longueur","largeur","dureeHold"]:
                    print(field,":")
                    entree[field]=copy[field] if field in copy else input()
                cur.execute("SELECT COUNT(*) FROM essai WHERE nomFichier=?", (fname,))
                if list(cur)[0][0] > 0 :
                    print(os.path.join(dirName, fname),"déjà dans la BD")
                    m+=1
                else :
                    print("Importation de",os.path.join(dirName, fname))
                    cur.execute("INSERT INTO essai(nomFichier,nomPapier,nomCondexp,nomSurface,diametre,longueur,largeur,dureeHold) VALUES(?,?,?,?,?,?,?,?)",(fname,entree['nomPapier'],entree['nomCondexp'],entree['nomSurface'],float(entree['diametre']),float(entree['longueur']),float(entree['largeur']),float(entree['dureeHold'])))
                    conn.commit()
                    n+=1
    t2 = time()
    print(m,"musiques étaient déjà importées dans la BD")
    print(n,"musiques ont bien été importées dans la BD")
    if DEBUG_TIME_GLOBAL_IMPORT and n>0 : print("=== Durée totale de l'importation :",t2-t1," === Durée moyenne :",(t2-t1)/n,"par fichier")