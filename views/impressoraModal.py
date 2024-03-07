from envs import *
from scripts import verificarImpressora as impressora
from .submitModal import SUBMIT
from services.Services import Services
from scripts import econect

class modalImpressora:

    
    def __init__(self,telaPrincipal,servicos):          
        self.telaPrincipal=telaPrincipal
        self.servicos= servicos
        self.container = Frame(self.telaPrincipal, bg="#f2f2f2")
        self.container.pack(fill="both", expand="yes")

    def Main(self):

        Error = Label(self.container, text="", foreground='black', background='#f2f2f2')
        Error.place(relx=0.5, rely=0.40, anchor=CENTER) 

        # botaoCancelar = Button(self.container, text="cancelar", command= lambda: [Services.cancelar()], background='#dc3545', activebackground='darkred',highlightcolor="darkred", activeforeground='white', foreground='white', bd=0)
        # botaoCancelar.place(relx=0.5, rely=0.85, relwidth=0.2, relheight=0.08, anchor=CENTER)
        # botaoCancelar.bind('<Return>',lambda e: Services.cancelar())

        impressora.verificaImpressora(Error,self.servicos,self.telaPrincipal,self)
     
    def resultado(self,Error):

        self.telaPrincipal.withdraw()

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
        
        def result(widgets):
          
            if validarInput() == True:

                msg_retorno['text']=""

                if inputOpcao.get() == '1':
                    for x in widgets: x.destroy()
                    self.container.destroy()
                    SUBMIT(self.telaPrincipal,7,"Troquei de porta USB, mesmo assim não reconheceu",self.servicos).submitError()
                    return False
                
                for x in widgets: x.destroy()


                impressora.verificaImpressora(Error,self.servicos,self.telaPrincipal,self)
        
        label = Label(self.container, text="SEM RESPOSTA...\n",bg="#f2f2f2")
        label.place(relx=0.5, rely=0.17, relwidth=0.5, relheight=0.08, anchor=CENTER)           

        opcao1 = Label(self.container, text="1 - Troquei de porta USB\nmesmo assim não reconheceu",bg="#f2f2f2")
        opcao1.place(relx=0.5, rely=0.30, relwidth=0.5, relheight=0.08, anchor=CENTER)           

        opcao5 = Label(self.container, text="2 - Tentar novamente",bg="#f2f2f2")
        opcao5.place(relx=0.5, rely=0.40, relwidth=0.5, relheight=0.08, anchor=CENTER)

        labelinput = Label(self.container, text="Digite a opção e tecle ENTER:",bg="#f2f2f2")
        labelinput.place(relx=0.5, rely=0.60, relwidth=0.5, relheight=0.08, anchor=CENTER)

        inputOpcao=Entry(self.container, width=22, insertwidth= 2, justify="center",textvariable="1")
        inputOpcao.focus()
        inputOpcao.place(relx = 0.5, rely = 0.67, anchor = CENTER)
        inputOpcao.delete(0,END)
        inputOpcao.bind('<Return>',lambda e:result([opcao1,opcao5,labelinput,inputOpcao]))

        msg_retorno = Label(self.container, text="",foreground='#ff4444',background="#f2f2f2")
        msg_retorno.place(relx=0.5, rely=0.77, anchor=CENTER)

        self.telaPrincipal.deiconify()
    
    def resultadoFinal(self):  

        econect.pausaAplicacao()  

        self.telaPrincipal.withdraw()

        def validarInput():

            try:

                int(inputOpcao.get())
                if int(inputOpcao.get()) > 3 or int(inputOpcao.get()) <= 0: 
                    msg_retorno['text']="Opção inválida"
                    return False
            
            except: 
                
                msg_retorno['text']="Opção inválida"
                return False                   

            return True
        
        def result(widgets):
          
            if validarInput() == True:

                msg_retorno['text']=""

                if inputOpcao.get() == '1':
                    for x in widgets: x.destroy()
                    self.container.destroy()
                    SUBMIT(self.telaPrincipal,5,"Troquei de porta USB e voltou ao normal",self.servicos).submitError()
                    # return False
                if inputOpcao.get() == '2':
                    for x in widgets: x.destroy()
                    self.container.destroy()
                    SUBMIT(self.telaPrincipal,7,"Troquei de porta USB, mesmo assim não reconheceu",self.servicos).submitError()

                    
                    # return False
                
                for x in widgets: x.destroy() 

                self.telaPrincipal.iconify()

                sleep(2)

                econect.retornaAplicacao()

                sleep(10)

                return modalImpressora.resultadoFinal(self)

                # impressora.verificaImpressora(Error,self.servicos,self.telaPrincipal,self)

        label = Label(self.container, text="O que aconteceu?",bg="#f2f2f2",font=("Arial",15))
        label.place(relx=0.5, rely=0.07, relwidth=1, relheight=0.08, anchor=CENTER)           

        opcao1 = Label(self.container, text="1 - Realizei o teste e funcionou",bg="#f2f2f2")
        opcao1.place(relx=0.5, rely=0.20, relwidth=1, relheight=0.08, anchor=CENTER)           

        opcao2 = Label(self.container, text="2 - Realizei o teste e não funcionou",bg="#f2f2f2")
        opcao2.place(relx=0.53, rely=0.30, relwidth=1, relheight=0.08, anchor=CENTER)

        opcao3 = Label(self.container, text="3 - Não realizei o teste. Testar agora",bg="#f2f2f2")
        opcao3.place(relx=0.54, rely=0.40, relwidth=1, relheight=0.08, anchor=CENTER)

        labelinput = Label(self.container, text="Digite a opção (1,2 ou 3) e tecle ENTER:",bg="#f2f2f2")
        labelinput.place(relx=0.5, rely=0.55, relwidth=1, relheight=0.08, anchor=CENTER)

        inputOpcao=Entry(self.container, width=22, insertwidth= 2, justify="center",textvariable="1")
        inputOpcao.focus()
        inputOpcao.place(relx = 0.5, rely = 0.62, anchor = CENTER)
        inputOpcao.delete(0,END)
        inputOpcao.bind('<Return>',lambda e:result([label,opcao1,opcao2,opcao3,labelinput,inputOpcao]))

        msg_retorno = Label(self.container, text="",foreground='#ff4444',background="#f2f2f2")
        msg_retorno.place(relx=0.5, rely=0.73, anchor=CENTER)

        self.telaPrincipal.deiconify()
