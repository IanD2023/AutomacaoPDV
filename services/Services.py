import requests
import base64
import json 
import os
from envs import *
from scripts import econect
from services.conexaoMYSQL import Mysql
from services.Logs import createLog

class Services:

    def __init__(self):
        pass    
    
    def __init__(self,matricula,nomesolicitante,contato,cat2,descricao, caminhoimagem, status, msg_retorno,tempoinicio):
        self.matricula = matricula
        self.nomesolicitante = nomesolicitante
        self.contato=contato
        self.cat2 = cat2
        self.descricao=descricao
        self.caminhoimagem=caminhoimagem
        self.status = status
        self.msg_retorno=msg_retorno
        self.tempoinicio=tempoinicio

    def categoria(self):

        categorias={"ERRO DE CARGA":"Falha no Banco de Dados","APLICAÇÃO TRAVADA":"Configurar PDV","PDV LENTO":"Configurar PDV","TRAVADO TELA ECONECT":"Falha no Banco de Dados",
                     "ITENS NÃO CADASTRADOS":"Falha no Banco de Dados","DUPLICIDADE NOTA SEFAZ":"Corrigir Rejeição Sefaz","PINPAD NÃO CONECTADO":"Erro de PIN PAD","ERRO DE IMPRESSÃO":"Erro de Impressão","NOTA NÃO ENCONTRADA":"Nota Fiscal Não Encontrada",
                     "OUTRO":"OUTROS"}
        
        return categorias[self.cat2]


    def Enviar(self):

        url = LINKMONITOR+'/chamados'
        # url = 'http://localhost:3005/chamados'

        if self.status == 4: descricao = self.cat2
        else: descricao= self.categoria()

        try:

            #Enviando para o servidor
            with open(self.caminhoimagem, 'rb') as f:
                im_bytes = f.read()        
                im_b64 = base64.b64encode(im_bytes).decode("utf8")
            
            json = {
            'descricao': descricao,
            'solicitante' : self.matricula,
            'contato' : self.contato,
            'nome_loja' : NOMELOJA,
            'numero_loja' : NUMEROLOJA,
            'pdv' : PDV,
            'status' : self.status,
            'observacao': self.descricao,
            'media': im_b64,
            'msg_retorno':self.msg_retorno
            }      
            
            #Enviando para o servidor        
            ##requests.post(url, json=json) 
            x=requests.post(url, data=json,timeout=30)
            
            #Deletar Captura da tela
            path = self.caminhoimagem
            os.remove(path)
            print(x.json())
            
            return x.json()['msg_retorno']
        
        except Exception as erro:
    
            print(erro)

            createLog('monitor', 'Erro ao enviar informaçoes ao servidor' + str(erro))

            return False
         
                        
    def Submit(self):    
       
        if(self.cat2 and self.matricula and self.descricao):

            #Enviando para o servidor
            if Services.Enviar(self) != False:
                                             
                sleep(1)                    
                               
                return True
            
            else:
                
                return 'Erro ao enviar dados!'

    def notafiscal(cupom):

     concLoja=Mysql(IPCONC,USUARIOBD,SENHABD,"concentrador")

     if concLoja.testaBanco("concentrador"):
         
         createLog('notafiscal', 'ERRO AO ACESSAR O BANCO DO SERVIDOR DA LOJA')
         
         return 'Error database'
     
     else:
        ##.sql('select cod_hdw from cfg_ipr_pdv where cod_pdv = '+PDV)
        # print(concLoja.sql("select * from capa_cupom_venda where numero_cupom = "+cupom+" and numero_pdv = "+PDV+" and string_retorno = '65'"))

        if (concLoja.sql("select * from capa_cupom_venda where numero_cupom = "+cupom+" and numero_pdv = "+PDV+" and string_retorno = '65'") != ""):

                    return 'cupom'
 

        url = LINKMONITOR+'/buscanota'

        json = {
            'loja': NUMEROLOJA,
            'pdv' : PDV,
            'cupom' : cupom 
            }
        
        x=requests.post(url, data=json,timeout=30)

        print(x.status_code)

        if x.status_code == 200:

            print("Não está na consinco")
        
            if(concLoja.sql("select * from capa_cupom_venda where numero_cupom = "+cupom+" and numero_pdv = "+PDV) != ""):
                
                print("Ja está no concentrador da loja")

                return False
            
            else: 
                
                print("Não está na consinco")
                print("Não está no concentrador da loja")

                return True

        else: 
            
            return '300'

    def validarMatricula(usuariopdv):

        try:

            url = LINKMONITOR+'/validacoes'

            json = {
                'usuariopdv': usuariopdv
                }
            
            x=requests.post(url, data=json,timeout=30)
            print(x.text)

            if x.text == 'False':

                return "Matrícula não encontrada"

            return x.json()['msg_retorno']
        
        
        except: 

            createLog('validarmatricula', 'ERRO AO ACESSAR O BANCO DO SERVIDOR MONITOR')
            
            return ""

    def codImpressora():
    
         cod_impressora=Mysql(IPCONC,USUARIOBD,SENHABD,"concentrador").sql('select cod_hdw from cfg_ipr_pdv where cod_pdv = '+PDV)

         return cod_impressora
        
    def cancelar(): 

        econect.retornaAplicacao()

        sys.exit()

        #except SystemExit:

         #   print('Programa finalizado com a exceção SystemExit')

        ##os.system("killall python3")     

    

