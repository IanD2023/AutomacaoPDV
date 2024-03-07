from envs import *
from services.Services import Services
from views.reiniciarModal import reiniciarModal

def verificaImpressora(Error,servicos,tela_principal,modal_impressora):

    from views.impressoraModal import modalImpressora

    def impConectada(tipo_impressora):
        
        Error['text']=("Impressoa "+tipo_impressora+" conectada\n\nAo iniciar a aplicação\nFaça um teste de impressão")
        Error.update()

        sleep(5)

        # PDV.reiniciar(Error,servicos,tela_principal,"nao")
        modal_impressora.container.destroy()

        restartpdv = reiniciarModal(tela_principal,servicos)

        restartpdv.start('nao','impressora')

        # sleep(10)

        # modalImpressora(tela_principal,servicos).resultadoFinal()

        # modal_impressora.resultadoFinal(Error)

    def verificarConectado():

        cod_impressora=Services.codImpressora()
        
        #cod_impressora = '129'
        x=1   

        if cod_impressora == '129':

            impressora = '"Seiko Epson"'
            tipo_impressora="EPSON"
            
        if cod_impressora == "127":

            impressora = '"0b1b:0003"'
            tipo_impressora="BEMATECH"
        if cod_impressora == "176":

            impressora = '"1fc9:2016"'
            tipo_impressora="ELGIN"    
            

        while os.popen('lsusb | grep '+impressora).read().rstrip('\n') == "":

            # Error.update()

            if x < 10:

                Error['text'] = "\n\n\n\nImpressora "+tipo_impressora+" desconectada\n\nTroque de porta USB\n\nverificando se está conectada... "+str(60-x)+" s"
                Error.update()
            else:

                Error['text']=""
                Error.update()

                lbl.destroy()
                modal_impressora.resultado(Error)

                return False 

                        
            x+=1

            sleep(2)
        lbl.destroy()    

        impConectada(tipo_impressora)   


    from scripts import imagensGIF as imagem

    lbl = imagem.imagemDemonstracao()

    lbl.place(relx=0.5, rely=0.2, relwidth=0.5, relheight=0.3,anchor=CENTER)

    lbl.load(PASTALOCAL+'/img/usb1.gif')
    # img=threading.Thread(name="imagem",target=lbl.load('usb1.gif'))
    # img.start()
        
    img=threading.Thread(name="imagem",target=verificarConectado)
    img.start()    