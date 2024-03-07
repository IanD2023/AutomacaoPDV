import os
from envs import *

class Mysql:

    def __init__(self,host,usuario,senha,database):

        self.host=host
        self.usuario=usuario
        self.senha=senha
        self.database=database

    def conexao(self):

        conexaoMysql="mysql -u "+self.usuario+" -p"+self.senha+" -h "+self.host+" "+self.database+" -C -A -s"

        return conexaoMysql
    
    def sql(self,sql):

        conexao=self.conexao()

        resultado=os.popen(conexao+" -e '"+sql+"'").read().rstrip('\n')

        return resultado
    
    def testaBanco(self,database):

        testeConexao=os.system(self.conexao()+" --connect-timeout=1 -e 'use "+database+"; select numero_pdv from pdv limit 1'")

        return testeConexao
        