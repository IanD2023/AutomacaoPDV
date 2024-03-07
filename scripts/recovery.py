import os
from envs import *
from services.conexaoMYSQL import Mysql
from scripts import corrigirSequencia as cupom
from views.submitModal import SUBMIT
from services.Logs import createLog

class recoveryPDV:

    def __init__(self,modo,container,tela_principal,servicos):

        self.modo=modo
        self.container=container.container
        self.Error=container.Error
        self.tela_principal=tela_principal
        self.servicos=servicos

    def rodarComando(self,nome,comando):

        x=0

        while os.system(comando) != 0:
            
            print(nome+" tentativa "+str(x))

            if x >= 5:

                print(nome+" NUMERO DE TENTATIVAS EXCEDIDAS")

                return False
            
            sleep(2)

            x+=1

        print("SUCESSO")

        return True     

    def carga(self):

        connBancoLocal=Mysql('localhost',USUARIOBDROOT,SENHABDROOT,'pdv')

        while connBancoLocal.sql('select situacao_carga from controle_carga_pdv where situacao_carga = 9') == "":

            self.Error['text']="Aguarde... o pdv esta recebendo carga"
            self.Error.update()

            sleep(4)

        while connBancoLocal.sql('select numero_cupom_inicial from controle_movimento') == "":

            self.Error['text']="Aguardando iniciar o dia..."
            self.Error.update()

            sleep(4)   
        # hoje =  ("'"+str(date.today())+"'")

        self.container.destroy()
        cupom.corrigirSequencia(True,self.tela_principal,self.servicos)

        sys.exit()

        # connBancoLocal.sql('update controle_movimento set sequencia_operador = 2 where numero_pdv = '+PDV)    
        # connBancoLocal.sql('update movimento_entrada_operador set sequencia_operador = 2 where data_movimento = '+hoje+'"')    
        # connBancoLocal.sql('update exp_imp_movimento set sequencia_operador = 2 data_movimento = '+hoje+'"')    

    def recovery(self):

        print("Iniciando Recovery")

        self.Error['text']="\n\nAguarde..."

        try:

            os.system('cd /var/lib/mysql/; rm -r pdv;rm ib_buffer_pool;rm ibdata1;rm ib_logfile0;rm ib_logfile1;rm ibtmp1')

        except Exception as error:    

            print(error)

            createLog('recovery', ''' '''+str(error)+''' '''  )

        print("Arquivos excluidos")
        self.Error['text']="30%\n\nAguarde..."
        sleep(2)

        if os.system("service mysql restart") != 0:

            print("Erro ao reiniciar o banco após fazer o recovery")
            createLog('recovery','ERRO AO REINICIAR O BANCO APOS FAZER O RECOVERY, O PROCESSO SERA ENCERRADO')

            # return False

        sleep(2)
        print("Recriando o banco")
        self.Error['text']="50%\n\nAguarde..."
        recriaBanco=os.system("cd /usr/socin/econect/pdv/sql/;mysql -u "+USUARIOBDROOT+" -p"+SENHABDROOT+" -A -f < pdv.sql")
        sleep(2)
            
        if recriaBanco == 0:

            # print("ARQUIVO PDV.SQL IMPORTADO")
            self.Error['text']="90%\n\nAguarde..."
            self.Error.update()

            ##if os.popen('ls /usr/socin/econect/pdv/properties/Ips.properties').read().rstrip('\n') == "":

            os.system("echo 'IpPdv="+IP+"\nIpConc="+IPCONC+"' > /usr/socin/econect/pdv/properties/Ips.properties")

            self.Error['text']="100%\n\nAguarde..."
            self.Error['font']=("Arial", 15)  
            sleep(5)
            self.Error['text']="Ajuste finalizado!\nA aplicação irá iniciar em instantes..."
            sleep(5)
            print("PROCESSO FINALIZADO")
            os.popen("DISPLAY=:0 xterm -e startpdv > /dev/null &")
            sleep(5)
            self.carga()

        else:

            print("ERRO AO FAZER O RECOVERY VIA TERMINAL")
            # self.Error['text']="Não foi possível realizar o ajuste\nEsta situação será analisada pela equipe de suporte."
            sleep(10)
            self.container.destroy()
            SUBMIT(self.tela_principal,7,"ERRO AO FAZER O RECOVERY VIA TERMINAL",self.servicos).submitError()

            sys.exit()


    # def executeRecovery(self):

    #     self.recovery()
        
    #     # thread = threading.Thread(name='recovery'+str(datetime.now()), target=self.recovery)
    #     # thread.start()






    # def executeBackup(self):

    #     self.backup()
        
        # thread = threading.Thread(name='backup'+str(datetime.now()), target=self.backup)
        # thread.start()

    def backup(self):

        print("INICIANDO BACKUP")

        recriaBanco=self.rodarComando('sourcepdv',"cd /usr/socin/econect/pdv/sql/;mysql -u "+USUARIOBDROOT+" -p"+SENHABDROOT+" -A -f < pdv.sql")

        if recriaBanco != True:

            print('Erro ao recriar a database com o comando source pdv')

            createLog('recovery','ERRO AO RECRIAR A DATABASE COM O COMANDO SOURCE PDV, O PROCESSO SERA ENCERRADO')

            SUBMIT(self.tela_principal,7,"ERRO AO REALIZAR O COMANDO SOURCE PDV",self.servicos).submitError(0)

            sys.exit()

        # os.system('cd /var/lib/mysql/; rm -r pdv;rm ib_buffer_pool;rm ibdata1;rm ib_logfile0;rm ib_logfile1;rm ibtmp1')

        # sleep(2)
        # os.system("service mysql restart")
        # sleep(2)
        self.Error['text']="70%\naguarde..." 
        self.Error.update()
        os.system("cd "+PASTALOCAL)

        # criarbancopdv=os.system('mysql -u root -pB4nc0my5q1 -e "CREATE DATABASE IF NOT EXISTS pdv"')

        # if criarbancopdv == 0:
            
        os.system("echo 'INICIANDO O RECOVERY'")
        
        recuper_bkp=self.rodarComando('backup',"mysql -u "+USUARIOBDROOT+" -p"+SENHABDROOT+" pdv < "+PASTALOCAL+"/dumps/bkp_pdv.sql")
            
        if recuper_bkp == True:

            os.system("echo 'BACKUP IMPORTADO COM SUCESSO'")

            os.system('mysql -u '+USUARIOBD+' -p'+SENHABD+' pdv -e "delete from controle_carga_pdv"')

            if self.modo == 1:
                    
                os.system('mysql -u '+USUARIOBD+' -p'+SENHABD+' pdv -e "delete from pdv"')

            self.Error['text']="100%\naguarde..."  
            self.Error.update()
            sleep(1)
            self.Error['text']="Ajuste finalizado!\nA aplicação irá iniciar em instantes..."
            self.Error.update()
            sleep(5)
            os.popen("DISPLAY=:0 xterm -e startpdv > /dev/null &")
            sleep(2)

            self.container.destroy()

            SUBMIT(self.tela_principal,5,"SUCESSO AO REALIZAR O BACKUP",self.servicos).submitError()
                    
                    ##os.system(EXIT)

        else:

            print("ERRO AO RECUPERAR BACKUP")

            createLog('recovery','ERRO AO RECUPERAR BACKUP, O PROCESSO SERA FEITO DE FORMA MANUAL, VERIFIQUE O ARQUIVO bkp_pdv.sql NA PASTA dumps/')
            self.Error['text']="100%\naguarde..." 
            self.Error.update()
            sleep(1)
            self.Error['text']="Ajuste finalizado!\nA aplicação irá iniciar em instantes..."
            self.Error.update()
            sleep(5)
            os.popen("DISPLAY=:0 xterm -e startpdv > /dev/null &")
            sleep(2)

            self.container.destroy() 

            # self.recovery()

            # self.Error['text']="Não foi possível realizar o ajuste\nEsta situação será analisada pela equipe de suporte."
            # sleep(10)
            # self.container.destroy()
            SUBMIT(self.tela_principal,7,"ERRO AO RECUPERAR O ARQUIVO bkp_pdv.sql NA PASTA dumps/",self.servicos).submitError()

            # sys.exit()


