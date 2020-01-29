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

root_window = tk.Tk()
root_window.withdraw()
directory='../../'
DBfile = "../../papertube.db"
conn = sqlite3.connect(DBfile)
cur = conn.cursor()



# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt
import numpy as np

# Fixing random state for reproducibility
np.random.seed(19680801)



## On récupère les données

# on veut récupérer les données en fonction des paramètres : L,l,ratio (à créer nous meme), Rayon, Thold, surface, type de papier
#et le tracer la fréquence en fonction de ces paramètres et du temps
t = ('A4',)
c.execute('SELECT * FROM essai WHERE nomPapier=?', t)
print c.fetchone()




cur.execute('SELECT essai_res.fichierFreq FROM essai JOIN essai_res ON essai.id = essai_res.idEssai WHERE essai.id = ?', t)

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





## On affiche
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

colors = ['r', 'g', 'b', 'y']
yticks = [3, 2, 1, 0]
for c, k in zip(colors, yticks):
    # Generate the random data for the y=k 'layer'.
    xs = np.arange(20)
    ys = np.random.rand(20)

    # You can provide either a single color or an array with the same length as
    # xs and ys. To demonstrate this, we color the first bar of each set cyan.
    cs = [c] * len(xs)
    cs[0] = 'c'

    # Plot the bar graph given by xs and ys on the plane y=k with 80% opacity.
    ax.bar(xs, ys, zs=k, zdir='y', color=cs, alpha=0.8)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# On the y axis let's only label the discrete values that we have data for.
ax.set_yticks(yticks)

plt.show()