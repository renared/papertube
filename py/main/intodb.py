import sqlite3
import os

DBfile = "D:/Yann/Desktop/stabien/papertube.db"
conn = sqlite3.connect(DBfile)
cur = conn.cursor()

def intoDB(directory,sameConfAs=None):
    if sameConfAs!=None:
        cur.execute("SELECT COUNT(*) FROM essai WHERE nomFichier=?",(sameConfAs,))
        if list(cur)[0][0] > 0 :
            pass
        else : print("Le fichier de preset n'existe pas dans la DB.")

    m,n = 0,0
    t1 = time()
    for dirName, subdirList, fileList in os.walk(path, topdown=False):
        for fname in fileList:
            if fname.endswith(".wav"):
                cur.execute("SELECT COUNT(*) FROM songs WHERE filename=?", (fname,))
                if list(cur)[0][0] > 0 :
                    print(os.path.join(dirName, fname),"déjà dans la BD")
                    m+=1
                else :
                    print("Importation de",os.path.join(dirName, fname))
                    sampFreq, snd = wav.read(os.path.join(dirName, fname))
                    snd0 = downsample(mix_channels(snd),DOWNSAMPLING_FACTOR)
                    sampFreq0 = sampFreq//DOWNSAMPLING_FACTOR
                    t,f,Sxx = spectrogram(snd0, sampFreq0, FFTSIZE, OVERLAP)
                    pks = peaks(t,f,Sxx)
                    hts = hashpeaks(t,f,pks)
                    data = [(fname,)]
                    for item in data:
                        cur.execute("INSERT INTO songs(filename) VALUES(?)", item)
                    cur.execute("SELECT id FROM songs WHERE filename = ?", (fname,))
                    id = list(cur)[0][0]
                    for item in [(id, ht[0], ht[1]) for ht in hts]:
                        cur.execute("INSERT INTO hashes(idSong,t,h) VALUES(?,?,?)", item)
                    conn.commit()
                    n+=1
    t2 = time()
    print(m,"musiques étaient déjà importées dans la BD")
    print(n,"musiques ont bien été importées dans la BD")
    if DEBUG_TIME_GLOBAL_IMPORT and n>0 : print("=== Durée totale de l'importation :",t2-t1," === Durée moyenne :",(t2-t1)/n,"par fichier")