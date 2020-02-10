n'hésitez pas à demander à contribuer

Team Phelma du papier : Bastien Imbert (bastien.imbert@phelma.grenoble-inp.fr) et Yann "renared" Bourdin (yann.bourdin@phelma.grenoble-inp.fr)

# Papertube !

**Bien tout lire (rapidement en diagonale) avant de commencer à filmer et tout**

## ;)

![avgFreqDB](avgFreqDB.png)

## encore mieux

![régression puissance -1](regInv-dureeHold.png)

```
## Requête : SELECT essai_res.fichierFreq FROM essai_res JOIN essai ON essai.id=essai_res.idEssai WHERE essai.dureeHold=10 AND essai.commentaire='var dureeHold'
f(t) = 205.59395303722056 * ( t - -9.999999999999998 ) ^ -1.9948046630990899
## Requête : SELECT essai_res.fichierFreq FROM essai_res JOIN essai ON essai.id=essai_res.idEssai WHERE essai.dureeHold=20 AND essai.commentaire='var dureeHold'
f(t) = 8.868841529746348 * ( t - -2.4704196493778166 ) ^ -1.1686063122505885
## Requête : SELECT essai_res.fichierFreq FROM essai_res JOIN essai ON essai.id=essai_res.idEssai WHERE essai.dureeHold=30 AND essai.commentaire='var dureeHold'
f(t) = 57.31657958578606 * ( t - -9.757247726630192 ) ^ -1.5497302376553097
## Requête : SELECT essai_res.fichierFreq FROM essai_res JOIN essai ON essai.id=essai_res.idEssai WHERE essai.dureeHold=10 AND essai.commentaire='var dureeHold'
f(t) = 4.042290968674672 * ( t - 1.7897873373044655 ) ^ -1
## Requête : SELECT essai_res.fichierFreq FROM essai_res JOIN essai ON essai.id=essai_res.idEssai WHERE essai.dureeHold=20 AND essai.commentaire='var dureeHold'
f(t) = 4.521889441139854 * ( t - 0.15469416702223085 ) ^ -1
## Requête : SELECT essai_res.fichierFreq FROM essai_res JOIN essai ON essai.id=essai_res.idEssai WHERE essai.dureeHold=30 AND essai.commentaire='var dureeHold'
f(t) = 5.7058103099254875 * ( t - -0.3296897430589148 ) ^ -1
## Requête : SELECT essai_res.fichierFreq FROM essai_res JOIN essai ON essai.id=essai_res.idEssai WHERE essai.dureeHold=10 AND essai.commentaire='var dureeHold'
f(t) = 26.907751456855838 * ( t - -3.9975011877780298 ) ^ -1.5
## Requête : SELECT essai_res.fichierFreq FROM essai_res JOIN essai ON essai.id=essai_res.idEssai WHERE essai.dureeHold=20 AND essai.commentaire='var dureeHold'
f(t) = 36.20676056227471 * ( t - -8.167936841364964 ) ^ -1.5
## Requête : SELECT essai_res.fichierFreq FROM essai_res JOIN essai ON essai.id=essai_res.idEssai WHERE essai.dureeHold=30 AND essai.commentaire='var dureeHold'
f(t) = 46.02118801703095 * ( t - -8.845055089020091 ) ^ -1.5
## Requête : SELECT essai_res.fichierFreq FROM essai_res JOIN essai ON essai.id=essai_res.idEssai WHERE essai.dureeHold=10 AND essai.commentaire='var dureeHold'
f(t) = 208.96137136483904 * ( t - -9.99999999999988 ) ^ -2
## Requête : SELECT essai_res.fichierFreq FROM essai_res JOIN essai ON essai.id=essai_res.idEssai WHERE essai.dureeHold=20 AND essai.commentaire='var dureeHold'
f(t) = 199.4733327953145 * ( t - -9.999999999999998 ) ^ -2
## Requête : SELECT essai_res.fichierFreq FROM essai_res JOIN essai ON essai.id=essai_res.idEssai WHERE essai.dureeHold=30 AND essai.commentaire='var dureeHold'
f(t) = 241.37173073076082 * ( t - -9.999999999999998 ) ^ -2
```

## Keskifofer

### Stream caméra vers pc

Avec Droidcam X Pro (payant, faut passer par Aptoide)

dans les paramètres de l'appli, activer le Boost FPS (désactiver si la vidéo lag/desync), désactiver la limitation de FPS

sur VLC, ouvrir un flux réseau (Ctrl+N), mettre le "http://ip:4747/video" comme dit dans l'appli

sur VLC, personnaliser l'interface pour mettre le bouton Enregistrer dans la barre d'outils, puis enregistrer la vidéo avec ce bouton (débuter l'enregistrement au déroulement de la feuille, le stopper s'il n'y a pas eu d'à-coup depuis 14s)...

### Prérequis

il faut pip install les modules suivants :
```
pyWavelets
opencv-python
```
si tu n'as pas Anaconda, il te restera peut être à installer scipy, csv, sqlite, tkinter...

Logiciels : SQLite DB Browser, *Handbrake*

### Git

si tu ne l'as pas déjà fait, clone le projet.
avec git sur WSL on aurait fait comme ça :
```
cd /mnt/lettre-du-disque/chemin-windows-vers-tes-documents
git clone https://gitlab.ensimag.fr/bourdiny/papertube.git
```
pull au cas où à chaque fois que tu reviens sur le projet

commit régulièrement (`git commit -m "description du commit"`)

push régulièrement

### [Ancienne méthode] Pré-traitement des vidéos, avec Handbrake

comme dit sur Discord :
![handbrake.png](handbrake.png)
si possible, la vidéo doit commencer après que la feuille ait été relachée, une fois qu'elle est "à l'équilibre" prête à jerk, et s'arrêter vite après le dernier à-coup.
fais un sous-dossier dans video/ (que j'appelerai ici *banane*) et mets toutes les vidéos à traiter dedans

**Remarque importante** : mieux vaut faire un sous-dossier pour chaque série de mesures d'un même paramétrage de papier, par exemple un sous-dossier "01" peut-être ta première série où tu as testé plusieurs fois un papier A4, 2x20, surface carton, ...
ça sera beaucoup plus pratique pour mettre à jour la base de données (DB)

### Utilisation, avec Pyzo

#### Remarque concernant les chemins de fichiers
ils n'ont normalement pas besoin d'être changés :d

ouvre main.py, fais Ctrl+Shift+E (Run file as script)

#### Vidéo -> courbe

placer les vidéos dans des sous-dossiers (par ex "banane") de video_data/ (un sous-dossier pour une série de mesures identiques)
dans Pyzo,
```
processDirPlus("banane","clémentine","cornichon")
```

#### Importation dans la DB : papertube.db

```
intoDB("video/banane")
```

cela te demandera de renseigner tous les paramètres relatifs à ta série de mesures (tous les fichiers dans *banane/* auront les mêmes paramètres) ; je te conseille de jeter un oeil à la structure de la DB

#### Courbes -> graphiques d'à-coups et fréquence

s'ils n'existent pas, il faut créer les dossiers fig_peaks_main et fig_freq_main à la racine du projet
```
processDataDirPlus("banane","clémentine","cornichon")
```

je viens de changer la fonction, il faut pour chaque fichier vérifier si la détection des pics est correcte, au cas où il faudrait définir le seuil manuellement, puis ça met à jour la DB

tu retrouveras (par défaut) dans fig_peaks_main/ et fig_freq_main/ les résultats (respectivement les graphes de détection des à-coups, les courbes temps-fréquence)

**Remarque de fin** : ne pas oublier dans les chemins de dossiers le '/' à la fin !
