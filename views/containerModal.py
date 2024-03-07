from envs import *
from services.Services import Services

class containerModal:

    def __init__(self, TelaPrincipal):
        self.telaPrincipal = TelaPrincipal 
        self.container = Frame(self.telaPrincipal, bg="#f2f2f2")
        self.container.pack(fill="both", expand="yes")
        self.Error=Label()
        self.botaoCancelar=Label()

    def Main(self):  

        self.Error = Label(self.container, text="", foreground='black', background='#f2f2f2')
        self.Error.place(relx=0.5, rely=0.40, anchor=CENTER) 
        

        self.botaoCancelar = Button(self.container, text="cancelar", command= lambda: [Services.cancelar()], background='#dc3545', activebackground='darkred',highlightcolor="darkred", activeforeground='white', foreground='white', bd=0)
        self.botaoCancelar.place(relx=0.5, rely=0.85, relwidth=0.2, relheight=0.08, anchor=CENTER)
        self.botaoCancelar.bind('<Return>',lambda e: Services.cancelar())
            






        
           
   