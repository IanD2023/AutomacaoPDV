
from envs import *
from views.TelaPrincipal import TelaPrincipal
from scripts.login import Login
from services.Services import Services as servicos

class modalLogin:

      def __init__(self) -> None:
            pass
      
      def main():

        def validarInput():

            try:

                int(inputUsuario.get())
                int(inputSenha.get())

            except: 
                
                Error['text']="Usuário não encontrado"
                return False                   

            return True

        def login():
             
            usuario=inputUsuario.get()
            senha=inputSenha.get()
            Error['text']=""
            Error.update()

            if usuario and senha:

                if validarInput() == True:

                    data_solicitante = Login(usuario,senha).main(Error)

                    if data_solicitante != False:

                        telaPrincipal.destroy()  

                        TelaPrincipal.TelaPrincipal(servicos.validarMatricula(usuario),data_solicitante['nome'],data_solicitante['tipo_usuario'])
            
        telaPrincipal=TelaPrincipal.masterFrame()

        janela = Frame(telaPrincipal, bg="#f2f2f2")
        janela.pack(fill="both", expand="yes")

        labelUsuario = Label(janela, text="Usuário",background='#f2f2f2')
        labelUsuario.place(relx = 0.27, rely = 0.20)

        inputUsuario=Entry(janela, width=22, insertwidth= 2, justify="center")
        inputUsuario.focus()
        inputUsuario.place(relx = 0.5, rely = 0.30, anchor = CENTER)
        inputUsuario.bind('<Return>',lambda e:login())

        labelSenha = Label(janela, text="Senha",background='#f2f2f2')
        labelSenha.place(relx = 0.27, rely = 0.38)

        inputSenha=Entry(janela, width=22, insertwidth= 2, justify="center",show="*")
        inputSenha.place(relx = 0.5, rely = 0.47, anchor = CENTER)
        inputSenha.bind('<Return>',lambda e:login())

        botao = Button(janela, text="Cancelar",background='#dc3545',highlightcolor="black",
                       activebackground='#bd2d3b',activeforeground='white',bd=0,foreground='white')
        botao.place(relx=0.28, rely=0.79, relwidth=0.2, relheight=0.08)
        botao.bind('<Return>',lambda e: servicos.cancelar())

        botao2 = Button(janela, text="Entrar", command=lambda:[],background='#28a745',highlightcolor='black',
                        activebackground='#208938',foreground='white',bd=0)     
        botao2.place(relx=0.50, rely=0.79, relwidth=0.2, relheight=0.08)
        botao2.bind('<Return>',lambda e:login())

        Error = Label(janela, text="",foreground='#ff4444',background='#f2f2f2')
        Error.place(relx=0.5, rely=0.92, anchor=CENTER)

        telaPrincipal.mainloop()
