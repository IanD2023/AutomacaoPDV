#importações
from views.loginModal import modalLogin
from views.TelaPrincipal import TelaPrincipal
from services import atualizaVersao as release
from scripts import econect
from envs import * 

if __name__== '__main__':

    #os.system("wmctrl -r :ACTIVE: -b toggle,above")
   #  econect.pausaAplicacao()

    # release.verificarVersao()

    if release.verificarVersao() == True:

       exit()


    econect.pausaAplicacao()    

    #TelaPrincipal.TelaPrincipal('10772')
    modalLogin.main()
