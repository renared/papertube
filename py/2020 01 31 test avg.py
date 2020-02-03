## Attention c'est codé à la pisse
os.chdir("D:/Yann/Desktop/stabien/py/")
subfolders = [ f.path[3:] for f in os.scandir("../res/freq/") if f.is_dir() ]
for subfolder in subfolders:
    plt.figure(figsize=(16,8))
    plotFreq("stabien/"+subfolder+"/",plotAll=False)
    plt.xlim(0,90)
    plt.ylim(0,2)
    plt.ylabel("Jerk frequency (Hz)")
    plt.xlabel("Time (s)")
    plt.title(subfolder)
    plt.savefig(fname="../fig_freq_avg_main/"+subfolder.replace("res/freq/","")+"_freq"+".png",bbox_inches='tight',pad_inches=0)
    plt.close()