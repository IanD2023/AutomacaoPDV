from pynput.keyboard import Controller, GlobalHotKeys
import os
import sys

keyboard = Controller()

def Janela():


    if os.system('ls /usr/bin/startJanela') != 0 or os.system('ls /usr/bin/killJanela') != 0:


        os.system('chmod 777 -R /root/JanelaGLPI/dependencias/os/startJanela')
        os.system('chmod 777 -R /root/JanelaGLPI/dependencias/os/killJanela')

        os.system('cp /root/JanelaGLPI/dependencias/os/startJanela /usr/bin/')
        os.system('cp /root/JanelaGLPI/dependencias/os/killJanela /usr/bin/')

    os.system("DISPLAY=:0 openbox --reconfigure")
    os.system('startJanela')

with GlobalHotKeys({'<ctrl>+h': Janela}) as h: h.join()