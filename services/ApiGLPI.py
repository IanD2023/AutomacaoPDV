import requests
from services.Logs import createLog
import json
import os
from envs import *

class APIGLPI:
   
    def __init__(self,matricula_solicitante, nomesolicitante, contato, name ,content,status, urgency,type,descricao,tempoinicio,tempofim):

        self.matriculasolicitante = matricula_solicitante
        self.nomesolicitante = nomesolicitante
        self.contato = contato
        self.name = name
        self.content= content
        self.users_id_requester= USERS_ID_REQUESTER
        self.status = status
        self.type = type
        self.itilcategories_id = ITILCATEGORIES_ID
        self.urgency=urgency
        self.descricao = descricao
        self.tempoinicio = tempoinicio
        self.tempofim = tempofim
   
    def initSession(self):
        try:
            
            url = LINKGLPI+'/apirest.php/initSession'
            headers = {'App-Token': "eTZS6o2UgNYr7T6t3gQboumkAXFdFuh19DdWNDmo", 'Authorization': "user_token G78ohyT9CEpSFnopLqWEg23DR9hcL7AsEW2anDng"}
        
            x=requests.get(url, headers=headers,timeout=30) 
            sessintoken = x.json()['session_token']
            print(sessintoken)
            
            return sessintoken
    
        except  Exception as erro:
            print(erro)
            
            return False
             
             
    def Enviar(self):

        url = LINKGLPI+'/apirest.php/Ticket'
        tokenAutorization = self.initSession()
        
        if tokenAutorization == False:

            print('TOKEN DESATUALIZADO')

            return False
        
      
        headers = {'App-Token': "eTZS6o2UgNYr7T6t3gQboumkAXFdFuh19DdWNDmo", 'Session-Token':tokenAutorization }
        
        
        try:
            
            
            json = {
                'input': {
                    'name': self.name,      

                    'content': '''
                                  Loja: '''+NOMELOJA+'''\n
                                  Número do PDV: '''+PDV+'''\n
                                  Nome do Solicitante: '''+self.nomesolicitante+'''\n
                                  Matricula: '''+self.matriculasolicitante+'''\n
                                  Contato: '''+self.contato+'''\n
                                  Detalhes: '''+self.descricao+'''\n
                                  Descrição: '''+ self.content,  

                    '_users_id_requester': self.users_id_requester,
                    'status': self.status,                             
                    'itilcategories_id': self.itilcategories_id,                  
                    'urgency': self.urgency, 
                    'type': self.type,
                    'time_to_own': self.tempofim,
                    'time_to_resolve': self.tempofim # self.tempofim, #"2024-03-06 11:30:20",                     
                }
            }    
            
          
            x=requests.post(url, json=json,headers=headers,timeout=30)

            print(x.json())

            createLog('ChamadoGLPI',self.tempofim+self.tempoinicio)
            
                       
            return x.json()
        
        except Exception as erro:
    
            print(erro)

            createLog('ChamadoGLPI',str(erro))

            return False 
        
#APIGLPI('10772', 'IAN DANILO VIEIRA BARROS', contato, name ,content,status, urgency,type,descricao,tempoinicio,tempofim).Enviar()


    

