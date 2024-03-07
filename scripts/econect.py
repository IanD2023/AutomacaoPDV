from envs import *

def pausaAplicacao():

    PID=os.popen('pgrep -f java').read().rstrip('\n')

    os.system('kill -STOP '+PID)

    return PID
def retornaAplicacao():

    PID=os.popen('pgrep -f java').read().rstrip('\n')

    os.system('kill -CONT '+PID)

    return PID