# Import Module
from services.FTP import FTP
from envs import *
from services.conexaoMYSQL import Mysql
from services.Logs import createLog


def buscaDia(numero_cupom):

        caminho="/usr/socin/econect/pdv/movimento/"
        hoje = date.today()
        mesatual=hoje.month

        while 1:

            if mesatual == hoje.month:

                cupons=os.popen('ls '+caminho+str(hoje.day)+'/movimento_'+str(hoje.strftime('%d%m%Y'))+'_'+str(NUMEROLOJA)+'_'+str(PDV)+'_'+numero_cupom+'_*').read().rstrip('\n')

                if cupons != "":

                    return caminho+str(hoje.day)
                                            
                else: hoje = hoje - timedelta(1)

            else: 
                    
                    print("Nenhum movimento no mês encontrado")

                    return False

def subirNota(Error,numero_cupom):
        
    #concentrador=Mysql(IPCONC,USUARIOBD,SENHABD,"concentrador")
    #query=concentrador.sql("select * from capa_cupom_venda where numero_pdv="+PDV+" and numero_cupom = "+numero_cupom+" ")
        
    ftp_server =FTP(IPCONC,USUARIOFTP,SENHAFTP).conexao()
    ftp_server.cwd("/recepcao/")
    pasta=buscaDia(numero_cupom)

    if pasta:
                    
        arquivos=os.popen('cd /usr/socin/econect/pdv/movimento/; ls * | grep "'+numero_cupom+'"').read().rsplit("\n")
        
        os.chdir(pasta)
                
        for x in arquivos: #174113

            if x:

                with open(x, "rb") as file:

                        # Command for Uploading the file "STOR filename"
                        if ftp_server.storbinary("STOR "+x, file):

                            Error['text']="\n\nNota enviada!\n\nEm alguns minutos..\nVerifique no painel de notas."
                            Error.update()

                            ##SUBMIT(tela_principal,5,"A nota foi enviada pro concentrador da loja e posteriormente integrou na Cosinco e gerou nota")

                        else: 
                            
                            Error['text']="\n\nERRO"
                            createLog('subir nota','ERRO AO ENVIAR ARQUIVO AO SERVIDOR DA LOJA '+str(x))
                            # return False

                     #ftp_server.close()  
        
        # Error['text']="\n\nNota enviada!\n\nVerifique no painel de notas."
        # Error.update()
        sleep(2)
        return True
    
    else: 

        Error['foreground']="#dc3545"
        Error['text']="\n\nNota não encontrada"

        return False
##FTP(HOSTNAME,USUARIO,SENHA,PASTA).enviararquivo(PASTA,"/recepcao/")