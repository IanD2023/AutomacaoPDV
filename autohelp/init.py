import os          
import sys
from datetime import *
from time import *
from tkinter import *
from econect import *
import threading


def start():

    Janela=Tk()
    Janela.geometry('300x100')
    Janela.title("AutoHelp NE")
    Janela.attributes("-topmost", True)
    Janela.resizable(False,False)
    Janela['background']='#f2f2f2'


    def cancelar():

        # retornaAplicacao()

        exit()

    def closeallwindow():

        sleep(5)

        # retornaAplicacao()

        # os.system('killJanela')

        sys.exit()

    textoNvl2 = Label(Janela, text="Já existe uma instância em execução\nAguarde por favor")
    textoNvl2.place(relx = 0.10, rely = 0.20)
    textoNvl2['background']='#f2f2f2'

    # botao2 = Button(Janela, text="SIM", command=lambda:[],background='#28a745',highlightcolor='black',activebackground='#208938',foreground='white',bd=0)     
    # botao2.place(relx=0.07, rely=0.70, relwidth=0.4, relheight=0.15)
    # botao2.bind('<Return>',lambda e: closeallwindow())

    # botao = Button(Janela, text="NÃO",background='#dc3545',highlightcolor="black",activebackground='#bd2d3b',activeforeground='white',bd=0,foreground='white')
    # botao.place(relx=0.55, rely=0.70, relwidth=0.4, relheight=0.15)
    # botao.bind('<Return>',lambda e: cancelar())



    # # pausaAplicacao()
    # thread = threading.Thread(name=f'autohelp', target=closeallwindow())
    # thread.start()  

    # closeallwindow()


    Janela.mainloop()


thread = threading.Thread(name=f'autohelp', target=start)
thread.start()
sleep(5)

os.system('killJanela')