from envs import *

def createLog(nameprocesse,message):

    try:

        if DEBUG:

            os.system('echo "'+str(datetime.now())+': '+nameprocesse+' '+message+'" >> '+PASTALOCAL+'/logs/'+nameprocesse+'.log ')

    except Exception as erro:

        print(erro)