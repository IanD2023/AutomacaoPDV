from envs import *
from services.Services import Services
from scripts import subirNota as notas
from .submitModal import SUBMIT

class Nota:
     
    def __init__(self,tela_principal,servicos):
          
            self.tela_principal=tela_principal
            self.servicos=servicos
            self.container = Frame(self.tela_principal, bg="#f2f2f2")
            self.container.pack(fill="both", expand="yes")
     
    def main(self):
            
            Error = Label(self.container, text="", foreground='black', background='#f2f2f2')
            Error.place(relx=0.5, rely=0.40, anchor=CENTER) 

            def isNumber():

                Error['text']=""
                Error.update()
                numero_cupom = cupom.get()

                try: 
                    int(numero_cupom) 

                    if int(numero_cupom) <= 1:
                         
                         return "\n\nNota não encontrada"
                    
                    return True
                
                except: return "\n\nNota não encontrada"

            def subirnota(event):

                if isNumber() == True:        

                    numero_cupom = cupom.get()
                    
                    verificaNF=Services.notafiscal(numero_cupom)

                    if verificaNF == 'Error database':
                         
                        Error['foreground']="#dc3545"
                        Error['text'] = 'Erro de conexão'  

                        return False  

                    if verificaNF == 'cupom':
                         
                        # self.container.destroy()
                        Error['foreground']="#dc3545"
                        Error['text']="Por favor informar um número de Cupom Fiscal válido"

                        Error.update()

                        # SUBMIT(self.tela_principal,7,"A nota já está no concentrador, porém não aparece pro usuario",self.servicos).submitError()

                    else:

                        if verificaNF == '300':
                             
                            Error['foreground']="#dc3545"
                            Error['text'] = 'Já existe número de NF para este Cupom Fiscal'

                            return True

                        if verificaNF == True:

                            if notas.subirNota(Error,numero_cupom) == True:

                                self.container.destroy()
                                
                                SUBMIT(self.tela_principal,5,"A nota foi enviada pro concentrador da loja e posteriormente integrou na Cosinco e gerou nota",self.servicos).submitError()

                        else: 

                            self.container.destroy()

                            SUBMIT(self.tela_principal,7,"A nota já está na Consinco, porém não foi gerado número de nota.",self.servicos).submitError()

                else: 

                    Error['foreground']="#dc3545"
                    Error['text'] = isNumber()        
            
            LabelCupom = Label(self.tela_principal, text="Informe o número do cupom")
            LabelCupom.place(relx = 0.5, rely = 0.20, anchor = CENTER)
            LabelCupom['background']='#f2f2f2'

            cupom=Entry(self.tela_principal, width=22, insertwidth= 2, justify="center")
            cupom.focus()
            cupom.place(relx = 0.5, rely = 0.27, anchor = CENTER)
            cupom.bind('<Return>',subirnota)

            botaoCancelar = Button(self.container, text="cancelar", command= lambda: [Services.cancelar()], background='#dc3545', activebackground='darkred',highlightcolor="darkred", activeforeground='white', foreground='white', bd=0)
            botaoCancelar.place(relx=0.5, rely=0.85, relwidth=0.2, relheight=0.08, anchor=CENTER)
            botaoCancelar.bind('<Return>',lambda e: Services.cancelar())