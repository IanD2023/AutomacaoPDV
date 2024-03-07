import requests
import json
import os
from envs import *

def verificarVersao():
        

        versao=os.popen("cat "+PASTALOCAL+"/release").read().rstrip('\n')

        print(versao)
        try:

            url = LINKMONITOR+'/atualizacoes'

            json = {
                'versaoCli':versao
                }
            
            response=requests.post(url, data=json)


            if response.status_code == 300:

                print("Versão Atualizada!")  

                return False
            

            os.system("cp "+PASTALOCAL+"/envs.py /home/")

            with open(PASTALOCAL+'/atualizacao', 'wb') as f:

                f.write(response.content)   

            os.system("cd "+PASTALOCAL+";unzip -o -q atualizacao")
            os.system("rm "+PASTALOCAL+"/atualizacao")
            os.system("cp /home/envs.py "+PASTALOCAL)

            print("Atualização realizada com sucesso!")

            sleep(5)

            return True
        
        except Exception as erro: 

            print(str(erro))
            return False
        