import os
from services.conexaoMYSQL import Mysql
from envs import *
from views.containerModal import containerModal
from services.Services import Services
from views.submitModal import SUBMIT

def buscaDia():

            caminho="/usr/socin/econect/pdv/movimento/"
            hoje = date.today()
            mesatual=hoje.month

            while 1:

                if mesatual == hoje.month:

                    cupons=os.popen('ls -l '+caminho+str(hoje.day)+'/movimento_*_*_*_*_0_112*').read().rstrip('\n')

                    if cupons != "":

                        data=cupons.rsplit('\n')[0].rsplit("_")[1]

                        date_movimento = datetime.strptime(data,'%d%m%Y').date()

                        if date_movimento == hoje:
                            
                            return date_movimento.day

                        else: 
                        
                            hoje = hoje - timedelta(1)
                            
                    else: hoje = hoje - timedelta(1)

                else : 
                     print("Nenhum movimento no mês encontrado")

                     return False
            
def corrigirSequencia(recovery,tela_principal,servicos):


    try:

        modal=containerModal(tela_principal)
        modal.Main()

        dia=buscaDia()
        caminho="/usr/socin/econect/pdv/movimento/"
        conexaoBancoM=Mysql(IPCONC,USUARIOBD,SENHABD,"concentrador")
        conexaoBancoLocal=Mysql("localhost",USUARIOBD,SENHABD,'pdv')
        testaBanco=conexaoBancoLocal.testaBanco('pdv')

        modal.Error['text']="Aguarde..."
        modal.Error.update()

        if testaBanco != 0:
            
            modal.Error['foreground']="red"

            
            modal.Error['text']="Erro ao consultar dados\nFavor entrar em contato com o suporte TI DEV"

            return False     

        if dia != False:

            maiorCupom=0
            maiorLot=0
            cupons=os.popen('cd '+caminho+str(dia)+'/;grep "Cupom:" movimento_*_*_*_*_0_112*').read().split('\n')
            
            ##Busca o maior cupom no pdv
            for x in cupons:

                if len(x) > 0:

                    num_nfc=x.rsplit(" ")[14]
                    
                    if int(num_nfc) > maiorCupom: 

                        maiorCupom=int(num_nfc)

            ##Busca o maior lot no pdv
            lots=os.popen('cd '+caminho+str(dia)+'/;grep "N.:" movimento_*_*_*_*_0_112*').read().rsplit('\n')
            
            for i in lots:

                    if len(i) > 0:

                        num_lot=i.rsplit("N.:")[1]

                        if int(num_lot.rsplit(' ')[0]) > maiorLot: 

                            maiorLot=int(num_lot.rsplit(' ')[0])

            ##Busca o maior cupom e lot no Matriz                 

            maiorCupomMatriz=conexaoBancoM.sql("select max(numero_cupom) from capa_cupom_venda where numero_loja = "+NUMEROLOJA+" and numero_pdv = "+PDV)
            
            maiorLotMatriz=conexaoBancoM.sql("select max(num_lot) from mov_nfc where num_loj = "+NUMEROLOJA+" and num_pdv = "+PDV+" and num_lot > "+str(maiorLot))

            print(maiorCupomMatriz,maiorLotMatriz,maiorCupom,maiorLot)
            """Compara os dados do Matriz e do PDV"""
        ## print("Maior cupom pdv:",maiorCupom, "Maior cupom Matriz: ",maiorCupomMatriz, "Maior lot pdv: ",maiorLot,"Maior lot Matriz: ",maiorLotMatriz)

            if int(maiorCupom) > int(maiorCupomMatriz):

                numeroCupom=(int(maiorCupom)+2)
                
                conexaoBancoLocal.sql("update controle_sequencia set sequencia = "+str(numeroCupom)+" where tipo_sequencia = 1")
                modal.Error['text']=("Numero cupom alterado com info do PDV")

            else:

                numeroCupom=(int(maiorCupomMatriz)+2)
                
                conexaoBancoLocal.sql("update controle_sequencia set sequencia = "+str(numeroCupom)+" where tipo_sequencia = 1")  
                modal.Error['text']=("Numero cupom alterado com info da Matriz")

            if maiorLotMatriz != 'NULL':

                if int(maiorLot) > int(maiorLotMatriz):

                    numeroCupom=(int(maiorLot)+2)
                    
                    conexaoBancoLocal.sql("update ctr_num_nfc set num = "+str(numeroCupom)+" where sre = 0")
                    modal.Error['text']=("Numero lot alterado com info do PDV")

                else:

                    numeroCupom=(int(maiorLotMatriz)+2)
                    
                    conexaoBancoLocal.sql("update ctr_num_nfc set num = "+str(numeroCupom)+" where sre = 0")
                    modal.Error['text']=("Numero lot alterado com info da Matriz")

            else: 

                numeroCupom=(int(maiorLot)+2)

                conexaoBancoLocal.sql("update ctr_num_nfc set num = "+str(numeroCupom)+" where sre = 0")  
                modal.Error['text']=("Numero lot alterado com info da Matriz")

        else:
            
            print("CONSULTANDO O MAIOR NUMERO DE CUPOM")
            maiorCupomMatriz=conexaoBancoM.sql("select max(numero_cupom) from capa_cupom_venda where numero_loja = "+NUMEROLOJA+" and numero_pdv = "+PDV)
            
            print("CONSULTANDO O MAIOR NUMERO DE LOT")
            maiorLotMatriz=conexaoBancoM.sql("select max(num_lot) from mov_nfc where num_loj = "+NUMEROLOJA+" and num_pdv = "+PDV)
            
            if maiorCupomMatriz != "":

                numeroCupom=(int(maiorCupomMatriz)+2)
                
                print("ALTERA A SEQUENCIA DO CUPOM")
                conexaoBancoLocal.sql("update controle_sequencia set sequencia = "+str(numeroCupom)+" where tipo_sequencia = 1")

            if maiorLotMatriz != "":

                numeroCupom=(int(maiorLotMatriz)+2)

                print("ALTERA A SEQUENCIA DO LOT")
                conexaoBancoLocal.sql("update ctr_num_nfc set num = "+str(numeroCupom)+" where sre = 0")

        modal.Error['text']="AJuste Realizado!\nTecle Esc, em seguida insira seu usuario e senha (Fiscal).\nFinalize a venda novamente..."
        modal.Error.update()
        sleep(17)

        if recovery == False:

            # SUBMIT(tela_principal,5,"Foi corrigida a sequencia do PDV",servicos).submitError()
            modal.container.destroy()
            SUBMIT(tela_principal,5,"Foi corrigida a sequencia do PDV",servicos).submitError()    
            Services.cancelar()

        # else:

        #     SUBMIT(tela_principal,5,"Foi corrigida a sequencia do PDV",servicos).submitError()    

    except Exception as erro:

        print(erro)        
        
        SUBMIT(tela_principal,7,"Erro ao corrigir sequencia do PDV",servicos).submitError()