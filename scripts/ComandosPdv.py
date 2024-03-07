from envs import *
from datetime import *
from time import *
from scripts import corrigirSequencia as sequencia
from scripts import recuperarPDV as recPDV
import scripts.reiniciarPDV as PDV
from views.pinpadModal import  modalPinpad
from views.impressoraModal import  modalImpressora
from views.subirNotaModal import  Nota
from views.containerModal import containerModal
from views.abrirChamadoModal import abrirChamado
from views.reiniciarModal import reiniciarModal

class ComandosPDV:

        def __init__(self):
                pass
    
        ##Swith dos scripts
        def switch(tela_principal,categoria,servicos): 

            """Scripts PINPAD"""
            if(categoria == "PINPAD NÃO CONECTADO"): 

                modalPinpad(tela_principal,servicos).Main()
                
            """Scripts Aplicaocao travada"""
            if (categoria == "APLICAÇÃO TRAVADA"):

                # modal=containerModal(tela_principal)
                # modal.Main()
                # modal.botaoCancelar.destroy()
                # PDV.reiniciar(modal.Error,servicos,tela_principal,"sim")

                reiniciarModal(tela_principal,servicos).start("sim",'aplicacao travada')

            """Scripts correcao de sequencia"""       
            if (categoria == "DUPLICIDADE NOTA SEFAZ"):

                sequencia.corrigirSequencia(False,tela_principal,servicos)

            """Scripts verificacao de impressora"""       
            if (categoria == "ERRO DE IMPRESSÃO"):

                modalImpressora(tela_principal,servicos).Main()

            """Scripts corrigir o banco do PDV"""       
            if (categoria == "ERRO DE CARGA" or categoria == "PDV LENTO" or categoria == "TRAVADO TELA ECONECT" or categoria == "ITENS NÃO CADASTRADOS" or categoria == "FULL RECOVERY"):
                
               ## modals.modalRecovery(tela_aviso)   
                if categoria == "PDV LENTO": forcarCarga=2

                else: forcarCarga= 1

                modal=containerModal(tela_principal)
                modal.Main()
                
                modal.Error['font']=("Arial", 17)

                recPDV.recuperarPDV(forcarCarga,modal,tela_principal,servicos) 

            """Scripts subir nota"""       
            if (categoria == "NOTA NÃO ENCONTRADA"):
                  
                Nota(tela_principal,servicos).main()


            # if (categoria == "OUTRO"):
                 
            #      abrirChamado(tela_principal,servicos).Main()
                 

                                  
        
                  
        
