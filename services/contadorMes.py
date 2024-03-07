from datetime import *

# print((date.today() - timedelta(1)).strftime('%d%m%Y'))

caminho="/usr/socin/econect/pdv/movimento/"
hoje = date.today()
mesatual=hoje.month
NUMEROLOJA = 31
PDV = 201
numero_cupom= 100

print('ls '+caminho+str(hoje.day)+'/movimento_'+str(hoje.strftime('%d%m%Y'))+'_'+str(NUMEROLOJA)+'_'+str(PDV)+'_'+str(numero_cupom)+'_*')