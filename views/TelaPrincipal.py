from services.Services import Services
from envs import *
from scripts import printPDV as image
from scripts.ComandosPdv import ComandosPDV
# Tira print e salvar
image.print()
caminhoimagem=PASTALOCAL+'/img/print.png'
versao=os.popen("cat "+PASTALOCAL+"/release").read().rstrip('\n').split('-')[0]

class TelaPrincipal:

    def __init__(self):
        pass

    def masterFrame():

        masterFrame=Tk()
        masterFrame.geometry('400x350')
        masterFrame.title("AutoHelp NE")
        masterFrame.attributes("-topmost", True)
        masterFrame.resizable(False,False)
        masterFrame['background']='#f2f2f2'

        return masterFrame
    
    def topLevel():

        novoFrame=Toplevel()
        novoFrame.geometry('400x350')
        novoFrame.title("AutoHelp NE")
        novoFrame.attributes("-topmost", True)
        novoFrame.resizable(False,False)
        novoFrame['background']='#f2f2f2'

        return novoFrame
    

    def TelaPrincipal(matricula,nomesolicitante,tipo_usuario):

        # Janela principal
        telaPrincipal=TelaPrincipal.masterFrame()

        janela = Frame(telaPrincipal, bg="#f2f2f2")
        janela.pack(fill="both", expand="yes")
        
        textoNvl2 = Label(janela, text="Selecione a opção")
        textoNvl2.place(relx = 0.27, rely = 0.02)
        textoNvl2['background']='#f2f2f2'

        if tipo_usuario == 'fiscal':

            if Services.codImpressora() != '127':

                Nvl2 = ttk.Combobox(janela, height= 10, width=21, 
                values=["APLICAÇÃO TRAVADA",
                        "ERRO DE CARGA",
                        "ERRO DE IMPRESSÃO",
                        "ITENS NÃO CADASTRADOS",
                        "PINPAD NÃO CONECTADO",
                        "TRAVADO TELA ECONECT",])
                        # ,"OUTRO"])
                Nvl2.focus()

            else:   

                Nvl2 = ttk.Combobox(janela, height= 10, width=21, 
                values=["APLICAÇÃO TRAVADA",
                        "ERRO DE CARGA",
                        "ITENS NÃO CADASTRADOS",
                        "PINPAD NÃO CONECTADO",
                        "TRAVADO TELA ECONECT",])
                        # ,"OUTRO"])
                Nvl2.focus() 

        if tipo_usuario == 'ti':

            if Services.codImpressora() != '127':

                Nvl2 = ttk.Combobox(janela, height= 10, width=21, 
                values=["APLICAÇÃO TRAVADA",
                        "DUPLICIDADE NOTA SEFAZ",
                        "ERRO DE CARGA",
                        "ERRO DE IMPRESSÃO",
                        "ITENS NÃO CADASTRADOS",
                        "NOTA NÃO ENCONTRADA",
                        "PDV LENTO",
                        "PINPAD NÃO CONECTADO",
                        "TRAVADO TELA ECONECT"])
                        # ,"OUTRO"])
                Nvl2.focus()

            else:   

                Nvl2 = ttk.Combobox(janela, height= 10, width=21, 
                values=["APLICAÇÃO TRAVADA",
                        "DUPLICIDADE NOTA SEFAZ",
                        "ERRO DE CARGA",
                        "ITENS NÃO CADASTRADOS",
                        "NOTA NÃO ENCONTRADA",
                        "PDV LENTO",
                        "PINPAD NÃO CONECTADO",
                        "TRAVADO TELA ECONECT"])
                        # ,"OUTRO"])
                Nvl2.focus() 


        Nvl2.place(relx=0.5, rely=0.12, anchor = CENTER)
        ##Nvl2.bind("<FocusOut>", lambda e: categoriaChamado(Nvl2.get()))
        Nvl2.current(0)

        LabelMatricula = Label(janela, text="Matricula:")
        LabelMatricula.place(relx = 0.27, rely = 0.18)
        LabelMatricula['background']='#f2f2f2'

        DesMatricula=Entry(janela, width=22, insertwidth= 2, justify="center",text=matricula)
        DesMatricula.insert(0, matricula)
        DesMatricula.place(relx = 0.5, rely = 0.28, anchor = CENTER)

        LabelContato = Label(janela, text="Contato: (Fiscal)")
        LabelContato.place(relx = 0.27, rely = 0.34)
        LabelContato['background']='#f2f2f2'

        DesContato=Entry(janela, width=22, insertwidth= 2, justify="center")
        DesContato.place(relx = 0.5, rely = 0.44, anchor = CENTER)

        # Descriçao

        LabelDescricao = Label(janela, text="Por favor, seja acertivo na descrição:")
        LabelDescricao.place(relx=0.07, rely=0.50)
        LabelDescricao['background']='#f2f2f2'

        DescricaoEntrada=Text(janela, width=42)
        DescricaoEntrada.place(relx=0.06, rely=0.57, relheight=0.2)

        # mensagem de erro
        Error = Label(janela, text="")
        Error.place(relx=0.5, rely=0.92, anchor=CENTER)
        Error['foreground'] = '#ff4444'
        Error['background']= '#f2f2f2'  

         # mensagem de erro
        release = Label(janela, text="versao: "+versao,background="#f2f2f2",foreground="silver")
        release.place(relx=0, rely=0.94)                          
        
        #Comandos

        
        def submit(event):

            def isNumber():

                matricula = DesMatricula.get()

                try: 
                    int(matricula) 
                    return True
                
                except: return "Matrícula inválida"
                        
            categoria = Nvl2.get()
            matricula = DesMatricula.get()
            contato = DesContato.get()    
            descricao = (DescricaoEntrada.get("1.0","end")) 
        
            if(matricula != "" and descricao != "" and contato != ""):

                Servicos = Services(matricula,nomesolicitante,contato,categoria, descricao, caminhoimagem, 1, 'desc',datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                
                

                validaMatricula = 'True'##Servicos.validarMatricula()

                if isNumber() != True:

                    Error['text']=isNumber()

                    return False

                if validaMatricula == 'True':

                    janela.destroy()

                    ComandosPDV.switch(telaPrincipal, categoria, Servicos)

                else: validaMatricula
                                
            else:

                Error['text']="Por favor, Preencher todos os campos!"
                
        def cancelar(event):
            Services.cancelar()      
            
        botao = Button(janela, text="Cancelar", command=lambda: [cancelar])
        botao.place(relx=0.28, rely=0.79, relwidth=0.2, relheight=0.08)
        botao.bind('<Return>',cancelar)
        botao.bind('<Button-1>',cancelar)
        botao['background']='#dc3545'
        botao['highlightcolor']="black"
        botao['activebackground'] = '#bd2d3b'
        botao['activeforeground']= 'white'
        botao['foreground'] = 'white'
        botao['bd']=0

        botao2 = Button(janela, text="Solicitar", command=lambda:[submit])        
        botao2.place(relx=0.50, rely=0.79, relwidth=0.2, relheight=0.08)
        botao2.bind('<Button-1>',submit)
        botao2.bind('<Return>',submit)
        botao2['background']='#28a745'
        botao2['highlightcolor']='black'
        botao2['activebackground']='#208938'
        botao2['foreground'] = 'white'
        botao2['fg'] = 'white'
        botao2['bd']=0
        
        telaPrincipal.mainloop()  
    
    
    
        
