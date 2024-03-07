import os          
import sys
from datetime import *
from time import *
from tkinter import *
from scripts import econect

class CloseAplication:

    def __init__(self):
        pass


    def start():

        Janela=Tk()
        Janela.geometry('300x200')
        Janela.title("AutoHelp NE")
        Janela.attributes("-topmost", True)
        Janela.resizable(False,False)
        Janela['background']='#f2f2f2'


        def cancelar():

            econect.retornaAplicacao()

            sys.exit()

        def closeallwindow():

            os.system('killJanela')

        textoNvl2 = Label(Janela, text="Já existe uma instância em execução\nDeseja interromper?")
        textoNvl2.place(relx = 0.15, rely = 0.10)
        textoNvl2['background']='#f2f2f2'

        botao2 = Button(Janela, text="SIM", command=lambda:[],background='#28a745',highlightcolor='#208938',activebackground='#208938',foreground='white',bd=0)     
        botao2.place(relx=0.07, rely=0.70, relwidth=0.4, relheight=0.15)
        botao2.bind('<Return>',lambda e: closeallwindow())

        botao = Button(Janela, text="NÃO",background='#dc3545',highlightcolor="#973030",activebackground='#bd2d3b',activeforeground='white',bd=0,foreground='white')
        botao.place(relx=0.55, rely=0.70, relwidth=0.4, relheight=0.15)
        botao.bind('<Return>',lambda e: cancelar())



        econect.pausaAplicacao()


        Janela.mainloop()