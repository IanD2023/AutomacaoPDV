from envs import *

def print():
 
    printTela=os.system("DISPLAY=:0 gnome-screenshot -f "+PASTALOCAL+"/img/print.png")
    if printTela == 0: return True
    else: return False