from envs import *
from views.submitModal import SUBMIT
from services.Services import Services

def reiniciar(tela_principal,abrirchamado,servicos):

    # Error.place(relx=0.5, rely=0.27, anchor=CENTER) 

    # Error['text']= """NÃO ESQUEÇA!\n\nAPROVAR OS VALORES DE CARTÃO NO SITEF\nCASO HAJA NECESSIDADE.
    # \nDESEJA CONTINUAR?\n1-SIM\n2-NÃO"""


    # labelinput = Label(tela_principal,text="Digite a opção e tecle ENTER:",bg="#f2f2f2")
    # labelinput.place(relx=0.5, rely=0.60, relwidth=0.5, relheight=0.08, anchor=CENTER)

    # inputOpcao=Entry(tela_principal, width=22, insertwidth= 2, justify="center",textvariable="1")
    # inputOpcao.focus()
    # inputOpcao.place(relx = 0.5, rely = 0.67, anchor = CENTER)
    # inputOpcao.delete(0,END)
    # inputOpcao.bind('<Return>',lambda e:result())
                
    os.system('killall java -9')
    os.popen("DISPLAY=:0 xterm -e startpdv > /dev/null &")
    sleep(2)

    if abrirchamado == 'sim':

        print("abrindo chamado no glpi")

        SUBMIT(tela_principal,5,"O pdv estava travado, foi reiniciada a aplicação.",servicos).submitError()

        Services.cancelar()