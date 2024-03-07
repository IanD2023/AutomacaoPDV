import os
import base64
import requests
from envs import *

numeroVersao = input("Informe o nome da versão: (nomeversao-comentario)\n")

os.system(f"echo {numeroVersao} > release")
os.system(f"zip -r -o -q {numeroVersao}.zip *")

with open(numeroVersao+".zip", 'rb') as f:
                
                im_bytes = f.read()    

                data = base64.b64encode(im_bytes).decode("utf8")

url = LINKMONITOR+'/atualizacoes'

json = {'numero_atualizacao': numeroVersao,'nova_atualizacao': data} 


x=requests.post(url, json=json)

print("fazendo requisicao")

print(x.text)

os.system('rm -r '+numeroVersao+'.zip')



##except: print("Erro ao fazer deploy")