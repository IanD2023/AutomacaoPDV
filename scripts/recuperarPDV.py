import os
from envs import *
from services.conexaoMYSQL import Mysql
from .recovery import *
from services.FilesModify import FilesModify as files
from views.submitModal import SUBMIT
from services.Logs import createLog

def rodarComando(nome,comando):

    x=0

    while os.system(comando) != 0:
        
        print(nome+" tentativa "+str(x))

        # if x >= 5:

            ##if nome == 'dados_adicionais_detalhe':

            # os.system('mysql -u '+USUARIOBDROOT+' -p'+SENHABDROOT+' pdv -e "delete from pdv.'+nome+' order by data_venda desc limit 100000"')
            
            # if nome == 'backup':
                
            #     os.system('mysql -u '+USUARIOBDROOT+' -p'+SENHABDROOT+' pdv -e "delete from produto"')
            #     os.system('mysql -u '+USUARIOBDROOT+' -p'+SENHABDROOT+' pdv -e "delete from plano_produto"')
            #     os.system('mysql -u '+USUARIOBDROOT+' -p'+SENHABDROOT+' pdv -e "delete from ean"')

        if x >= 5:

            print(nome+" NUMERO DE TENTATIVAS EXCEDIDAS")

            return False
        
        sleep(2)

        x+=1

    print("SUCESSO")

    return True    

def atualizaTela(Error,conn,progresso,x):

    while 1:

        qtdTabelas=conn.sql(
                    '''SELECT count(*) AS TOTALNUMBEROFTABLES 
                    FROM INFORMATION_SCHEMA.TABLES 
                    WHERE TABLE_SCHEMA = "pdv"''')
        
        print("lendo banco de dados")

        if qtdTabelas:

            porcent=(int(int(qtdTabelas)*x)+progresso)
        
            if int(qtdTabelas) > 787:
                print("completo")

                Error['text']=str(porcent)+"%\naguarde..."
                Error.update()

                return True

            Error['text']=str(porcent)+"%\naguarde..."
            Error.update()

        sleep(2)    

      

def recuperarPDV(modo,containermodal,tela_principal,servicos):
    
    containermodal.botaoCancelar= 'disabled'
    # conn=Mysql("localhost",USUARIOBDROOT,SENHABDROOT,"")
    # testaBanco=conn.testaBanco("pdv")
    containermodal.Error['text'] = "Aguarde..."
    containermodal.Error.update()

    os.system('cp -r /etc/mysql/mysql.conf.d/mysqld.cnf '+PASTALOCAL+'/dependencias/os/')
    os.system('echo "innodb_force_recovery = 6" >> /etc/mysql/mysql.conf.d/mysqld.cnf')

    if os.system('service mysql restart') != 0:
          
        print("Erro ao reiniciar o Serviço Mysql")

        createLog('recovery','ERRO AO REINICIAR O SERVICE MYSQL APOS ALTERACAO DO ARQUIVO: mysqld.cnf')

        # SUBMIT(tela_principal,7,"ERRO AO REINICIAR O SERVICE MYSQL APOS ALTERACAO DO ARQUIVO: mysqld.cnf",servicos).submitError()

        if os.system('cp -r '+PASTALOCAL+'/dependencias/os/mysqld.cnf /etc/mysql/mysql.conf.d/') != 0:
                    
                    os.system('echo "Erro ao restaurar arquivo de recuperacao do banco"')

                    createLog('recovery','ERRO AO RESTAURAR O ARQUIVO DE CONFIGURACAO DO MYSQL, O PROCESSO SERA FINALIZADO')
                 
                    SUBMIT(tela_principal,7,"ERRO AO RESTAURAR O ARQUIVO DE CONFIGURACAO DO MYSQL, O PROCESSO SERA FINALIZADO",servicos).submitError()

                    return False

                    # sys.exit()

        if os.system('service mysql restart') != 0:
                
                os.system('echo "Erro ao reiniciar o Serviço Mysql reiniciado"')

                createLog('recovery','ERRO AO REINICIAR O SERVICE MYSQL APOS RESTAURACAO DO ARQUIVO: mysqld.cnf, O PROCESSO SERA FINALIZADO')
                # return False
                SUBMIT(tela_principal,7,"ERRO AO REINICIAR O SERVICE MYSQL APOS RESTAURACAO DO ARQUIVO: mysqld.cnf, O PROCESSO SERA FINALIZADO",servicos).submitError()

                return False

                # sys.exit()

        print("ARQUIVO MYSQLD.CONF RESTAURADO")
        createLog('recovery','ARQUIVO MYSQLD.CONF RESTAURADO')      

        print("ERRO AO MODIFICAR O ARQUIVO DE CONFIGURACAO MYSQL, O PROCESSO DE RECUPERACAO SERA FEITO DE FORMA MANUAL")

        createLog('recovery','ERRO AO MODIFICAR O ARQUIVO DE CONFIGURACAO MYSQL, O PROCESSO DE RECUPERACAO SERA FEITO DE FORMA MANUAL')

        containermodal.Error['text']="Aguarde..."
        containermodal.Error.update()
        # os.system('killall java -9')
        # conn.sql("drop database pdv")

        recoveryPDV(0,containermodal,tela_principal,servicos).recovery() 

        sys.exit()
          
    print("Arquivo mysqld.conf modificado")   

    os.system('killall java -9')

    containermodal.Error['text']="40%\naguarde..."

    fazerBackup=rodarComando('backup',"mysqldump -u "+USUARIOBDROOT+" -p"+SENHABDROOT+" pdv > "+PASTALOCAL+"/dumps/bkp_pdv.sql")

    if fazerBackup == True:

        print("BACKUP REALIZADO COM SUCESSO")

        containermodal.Error['text']="50%\naguarde..."

        containermodal.Error.update()

        if os.system('cp -r '+PASTALOCAL+'/dependencias/os/mysqld.cnf /etc/mysql/mysql.conf.d/') != 0:
                 
                    os.system('echo "Erro ao restaurar arquivo de recuperacao do banco"')

                    SUBMIT(tela_principal,7,"ERRO AO RESTAURAR O ARQUIVO DE CONFIGURACAO DO MYSQL",servicos).submitError()

                    # sys.exit()

        if os.system('service mysql restart') != 0:

                os.system('echo "Erro ao reiniciar o Serviço Mysql reiniciado"')

                SUBMIT(tela_principal,7,"ERRO AO REINICIAR O SERVICE MYSQL APOS ALTERACAO DO ARQUIVO",servicos).submitError()

        print("ARQUIVO MYSQLD.CONF RESTAURADO")

        # conn.sql("drop database pdv")
        recoveryPDV(modo,containermodal,tela_principal,servicos).backup()
        # atualizaTela(containermodal.Error,conn,progresso=40,x=0.071)
            #atualizaTela(Error,conn)  
        
    else:

        if os.system('cp -r '+PASTALOCAL+'/dependencias/os/mysqld.cnf /etc/mysql/mysql.conf.d/') != 0:
                    
                    os.system('echo "Erro ao restaurar arquivo de recuperacao do banco"')

                    createLog('recovery','ERRO AO RESTAURAR O ARQUIVO DE CONFIGURACAO DO MYSQL APOS O BACKUP, O PROCESSO SERA FINALIZADO')

                 
                    SUBMIT(tela_principal,7,"ERRO AO RESTAURAR O ARQUIVO DE CONFIGURACAO DO MYSQL APOS O BACKUP, O PROCESSO SERA FINALIZADO",servicos).submitError()

                    sys.exit()

        if os.system('service mysql restart') != 0:
                
                os.system('echo "Erro ao reiniciar o Serviço Mysql reiniciado"')
                createLog('recovery','ERRO AO REINICIAR O SERVICO MYSQL APOS O BACKUP, O PROCESSO SERA FINALIZADO')

                SUBMIT(tela_principal,7,"ERRO AO REINICIAR O SERVICO MYSQL APOS O BACKUP, O PROCESSO SERA FINALIZADO",servicos).submitError()

                # return False
                sys.exit()

        print("ARQUIVO MYSQLD.CONF RESTAURADO")
        createLog('recovery','ARQUIVO MYSQLD.CONF RESTAURADO')


        print("NÃO FOI POSSIVEL REALIZAR O BACKUP, O PROCESSO DE RECUPERACAO SERA FEITO DE FORMA MANUAL")

        createLog('recovery','NÃO FOI POSSIVEL REALIZAR O BACKUP, O PROCESSO DE RECUPERACAO SERA FEITO DE FORMA MANUAL')

        containermodal.Error['text']="Aguarde..."
        containermodal.Error.update()
        # os.system('killall java -9')
        # conn.sql("drop database pdv")

        recoveryPDV(0,containermodal,tela_principal,servicos).recovery() 
