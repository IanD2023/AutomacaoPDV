from envs import *
from services.Services import Services
from services.ApiGLPI import APIGLPI
from services.Logs import createLog

class SUBMIT:
     
    def __init__(self,tela_principal,status,msg,servicos):
          
          self.tela_principal=tela_principal
          self.status=status
          self.msg=msg
          self.servicos=servicos

    def submitError(self):

            NovaModal = Frame(self.tela_principal, bg="#f2f2f2")
            NovaModal.pack(fill="both", expand="yes")

            ChamadoGLPI = APIGLPI(name=self.servicos.cat2,content=self.servicos.descricao,status='1', urgency='5',type='1',
                                  descricao=self.msg,contato=self.servicos.contato,nomesolicitante=self.servicos.nomesolicitante,
                                  matricula_solicitante=self.servicos.matricula,tempoinicio="",tempofim="")
            # name ,content,status, urgency,type 

            """se o status retornar erro aparecera a mensagem de retorno ao contrario sera exibido apenas um obrigado"""

            

            if self.status == 7:

                self.servicos.status=self.status
                self.servicos.msg_retorno=self.msg

                # numero_ticket=''
                numero_ticket=ChamadoGLPI.Enviar()

                if numero_ticket == False:
                     
                     Error = Label(NovaModal, text="Erro ao criar chamado. Contate a equipe de suporte", background='#f2f2f2')
                     Error.place(relx=0.5, rely=0.40, anchor=CENTER) 
                     NovaModal.update()

                     createLog('submit','ERRO AO CRIAR CHAMADO, NÃO FOI POSSIVEL ACESSAR O SERVIDOR GLPI')

                     Services.cancelar()

                     sys.exit()

                Error = Label(NovaModal, text="Esta situação será analisada pela equipe de suporte\nno ticket #"+str(numero_ticket['id']), background='#f2f2f2')
                Error.place(relx=0.5, rely=0.40, anchor=CENTER) 
                NovaModal.update() 
                sleep(10)
                Services.cancelar()

                sys.exit()
                
            if self.status == 4:
                  
                self.servicos.status=self.status
                self.servicos.msg_retorno=self.msg

                Error = Label(NovaModal, text="Aguarde...", background='#f2f2f2')
                Error.place(relx=0.5, rely=0.40, anchor=CENTER)

                numero_ticket=''

                Error['text']=("Ticket #"+str(numero_ticket)+" criado com sucesso!")
                NovaModal.update() 

                sleep(10)

                Services.cancelar()

                sys.exit()


            Error = Label(NovaModal, text="Obrigado :)", background='#f2f2f2',font=("Arial",17),foreground='black')
            Error.place(relx=0.5, rely=0.40, anchor=CENTER)
            NovaModal.update()

            # self.servicos.status=self.status
            # self.servicos.msg_retorno="Sucesso"
            
            numero_ticket=self.servicos.Enviar()

            ChamadoGLPI.status = '5'
            ChamadoGLPI.tempoinicio=self.servicos.tempoinicio
            ChamadoGLPI.tempofim=datetime.now().strftime('%Y-%m-%d %H:%M:%S')


            if ChamadoGLPI.Enviar() == False:
                 
                Error['text'] = "Erro ao criar chamado. Contate a equipe de suporte."

                createLog('submit','ERRO AO CRIAR CHAMADO, NÃO FOI POSSIVEL ACESSAR O SERVIDOR GLPI')

            sleep(2)

            Services.cancelar()