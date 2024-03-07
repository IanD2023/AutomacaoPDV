from envs import *
from scripts import verificarImpressora as impressora
from .submitModal import SUBMIT
from services.Services import Services

class abrirChamado:
    
    def __init__(self,telaPrincipal,servicos):          
        self.telaPrincipal=telaPrincipal
        self.servicos= servicos
        self.container = Frame(self.telaPrincipal, bg="#f2f2f2")
        self.container.pack(fill="both", expand="yes")

    def Main(self):

        labelCategoria = Label(self.container, text="Selecione uma opção:", foreground='black', background='#f2f2f2')
        labelCategoria.place(relx=0.5, rely=0.20, anchor=CENTER)
        categoriaSolis = ttk.Combobox(self.container, height= 10, width=35, 
        values=["SUPORTE PDV","SUPORTE INFRA","SUPORTE CONSINCO"])
        categoriaSolis.focus()
        categoriaSolis.place(relx=0.5, rely=0.27, anchor = CENTER)
        categoriaSolis.current(0)
        
        labelSubCategoria = Label(self.container, text="Categoria:", foreground='black', background='#f2f2f2')
        labelSubCategoria.place(relx=0.5, rely=0.37, anchor=CENTER)
        subcategoriaSolis = ttk.Combobox(self.container, height= 10, width=35, 
        values=[])
        subcategoriaSolis.place(relx=0.5, rely=0.44, anchor = CENTER)

        botaoCancelar = Button(self.container, text="Cancelar", command=lambda: [ Services.cancelar()])
        botaoCancelar.place(relx=0.28, rely=0.79, relwidth=0.2, relheight=0.08)
        botaoCancelar.bind('<Button-1>', lambda e: Services.cancelar())
        botaoCancelar['background']='#dc3545'
        botaoCancelar['highlightcolor']="#973030"
        botaoCancelar['activebackground'] = '#bd2d3b'
        botaoCancelar['activeforeground']= 'white'
        botaoCancelar['foreground'] = 'white'
        botaoCancelar['bd']=0

        botaoSubmit = Button(self.container, text="Enviar")        
        botaoSubmit.place(relx=0.50, rely=0.79, relwidth=0.2, relheight=0.08)
        botaoSubmit.bind('<Return>',lambda e: submit())
        botaoSubmit['background']='#28a745'
        botaoSubmit['highlightcolor']='#208938'
        botaoSubmit['activebackground']='#208938'
        botaoSubmit['foreground'] = 'white'
        botaoSubmit['fg'] = 'white'
        botaoSubmit['bd']=0

        categoriaSolis.bind("<FocusOut>", lambda e: self.categoriaChamado(subcategoriaSolis,categoriaSolis.get()))

        def submit():

            self.servicos.cat2 = subcategoriaSolis.get()
            categoria =categoriaSolis.get() 
            self.container.destroy()
            SUBMIT(self.telaPrincipal,4,categoria,self.servicos).submitError()

    def categoriaChamado(self,subcategoriaSolis,suporte):

        linhas = open(PASTALOCAL+"/dependencias/abrirchamado/"+suporte).readlines()
        categorias = []

        for linha in linhas:

            categorias.append(linha.rstrip('\n'))  

        subcategoriaSolis['value'] = categorias
