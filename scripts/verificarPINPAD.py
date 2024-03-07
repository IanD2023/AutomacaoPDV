import os
from time import *
from tkinter import *
from envs import *
from views.reiniciarModal import reiniciarModal


def verificarPinPad(Error,modal,pinpadmodal,widgts):
            
         
            from scripts import imagensGIF as imagem
            from views.pinpadModal import modalPinpad

            lbl = imagem.imagemDemonstracao()

            lbl.place(relx=0.5, rely=0.2, relwidth=0.5, relheight=0.3,anchor=CENTER)

            lbl.load(PASTALOCAL+'/img/usb1.gif')

            for x in widgts: x.destroy()
            
            
            def verificarConectado():
                 
                x=1

                while os.popen('lsusb | grep "GERTEC"').read().rstrip('\n') == "":

                    if x < 5:
                        
                        Error['text'] = "Verificando se está conectado... "+str(60-x)+" s"
                        
                    else: 

                        lbl.destroy()
                        Error['text'] = ""
                        
                        pinpadmodal.resultado(Error)

                        return False
                    
                    x+=1
                    Error.update()

                    sleep(2)

                lbl.destroy()    

                rodarUdev(Error)   

                return True   


            def rodarUdev(Error):            

                #Roda o comando UDEV
                os.system('''echo 'KERNELS=="*[0-9]", DRIVERS=="cdc_acm", SUBSYSTEMS=="usb", ACTION=="add", 
                            ATTRS{modalias}=="usb:v1753pC902d*dc*dsc*dp*ic*isc*ip*in*", SYMLINK+="ttyS60"' 
                            >> /etc/udev/rules.d/99-usb-serial.rules''')
                
                os.system("cd /usr/socin/econect/pdv/lib/; rm -r ChavesCliSiTef/")
                
                Error['text']="PINPAD CONECTADO!\n\nAo iniciar a aplicação\nFaça o teste novamente..."
                # Error.update()

                sleep(5)

                # pdv.reiniciar(Error,modal,modal,"nao")

                # Error['text']=""
                # Error.destroy()
                modal.destroy()

                restartpdv = reiniciarModal(pinpadmodal.telaPrincipal,pinpadmodal.servicos)

                restartpdv.start('nao','pinpad')

                # sleep(30)

                # restartpdv.container.destroy()
    
                # modalPinpad(pinpadmodal.telaPrincipal,pinpadmodal.servicos).resultadoFinal()
                
            thread=threading.Thread(name="verificarPINPAD",target=verificarConectado)
            thread.start()                