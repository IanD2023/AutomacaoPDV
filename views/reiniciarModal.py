from envs import *
from views.submitModal import SUBMIT
from scripts import reiniciarPDV as pdv
from services.Services import Services

class reiniciarModal():
                
        def __init__(self,telaPrincipal,servicos):
                     
                     self.telaPrincipal=telaPrincipal
                     self.servicos= servicos
                     self.container = Frame(self.telaPrincipal, bg="#f2f2f2")
                     self.container.pack(fill="both", expand="yes")

        # def reiniciar(Error,servicos,tela_principal,abrirchamado):
        def start(self,abrirchamado,modulo):

            from views.impressoraModal import modalImpressora
            from views.pinpadModal import modalPinpad

            def validarInput():

                try:

                    int(inputOpcao.get())
                    if int(inputOpcao.get()) > 2 or int(inputOpcao.get()) <= 0: 
                        msg_retorno['text']="Opção inválida"
                        return False
                
                except: 
                    
                    msg_retorno['text']="Opção inválida"
                    return False                   

                return True
            
            def restartPDV():

                if validarInput():

                    if int(inputOpcao.get()) == 1:

                        if modulo == 'impressora':



                            self.container.destroy()
                            pdv.reiniciar(self.telaPrincipal,abrirchamado,self.servicos)

                            sleep(2)

                            modalImpressora(self.telaPrincipal,self.servicos).resultadoFinal()

                        if modulo == 'pinpad':



                            self.container.destroy()
                            pdv.reiniciar(self.telaPrincipal,abrirchamado,self.servicos)

                            sleep(2)

                            modalPinpad(self.telaPrincipal,self.servicos).resultadoFinal()  

                        self.container.destroy()
                        pdv.reiniciar(self.telaPrincipal,abrirchamado,self.servicos)     


                    else:
                         
                         Services.cancelar()


            Message = Label(self.container,text="""NÃO ESQUEÇA!\n\nAPROVAR OS VALORES DE CARTÃO NO SITEF\nCASO HAJA NECESSIDADE.
            \nDESEJA CONTINUAR?\n\n1-SIM\n2-NÃO""",bg="#f2f2f2")

            Message.place(relx=0.5, rely=0.24, relwidth=1, relheight=1, anchor=CENTER)

            labelinput = Label(self.container,text="Digite a opção e tecle ENTER:",bg="#f2f2f2")
            labelinput.place(relx=0.5, rely=0.60, relwidth=0.5, relheight=0.08, anchor=CENTER)

            inputOpcao=Entry(self.container, width=22, insertwidth= 2, justify="center",textvariable="1")
            inputOpcao.focus()
            inputOpcao.place(relx = 0.5, rely = 0.67, anchor = CENTER)
            inputOpcao.delete(0,END)
            inputOpcao.bind('<Return>',lambda e:restartPDV()) 

            # Error.place(relx=0.5, rely=0.27, anchor=CENTER) 

            msg_retorno = Label(self.container, text="",foreground='#ff4444',background="#f2f2f2")
            msg_retorno.place(relx=0.5, rely=0.77, anchor=CENTER) 

            # sleep(10)
                        
            # os.system('killall java -9')
            # # os.popen("DISPLAY=:0 xterm -e startpdv > /dev/null &")
            # sleep(2)

            # if abrirchamado == 'sim':

            #     # Error.destroy()

            #     SUBMIT(self.telaPrincipal,5,"O pdv estava travado, foi reiniciada a aplicação.",self.servicos).submitError()

                # Services.cancelar()