from services.conexaoMYSQL import Mysql
from envs import *
import hashlib

class Login:

    def __init__(self,usuario,senha):

        self.usuario=usuario
        self.senha=senha

    def main(self,Error):

        conn=Mysql(IPCONC,USUARIOBD,SENHABD,'concentrador')

        if conn.testaBanco('concentrador') == 0:

            data_user = {'tipo_usuario':"fiscal",'nome':""}

            fiscal=conn.sql("""select * from usuario_perfil
                        where id_usuario in (select id from usuario_security
                        where login = """+self.usuario+""")
                        and id_perfil = 2;""")
            
            ti=conn.sql("""select * from usuario_perfil
                        where id_usuario in (select id from usuario_security
                        where login = """+self.usuario+""")
                        and id_perfil = 15;""")

            if fiscal != "":

                if ti != "":

                    data_user['tipo_usuario'] = 'ti'

                senhaMD5 = hashlib.md5(self.senha.encode()).hexdigest()

                autenticacao=conn.sql('''select nome from usuario_security where login = '''+self.usuario+''' and senha = "'''+senhaMD5+'''"''')

                print(autenticacao)

                if autenticacao != "":

                    # print(autenticacao)

                    data_user['nome'] = autenticacao

                    return data_user

                else: Error['text']="Usuário ou senha incorretos"  
                return False
                     

            else: Error['text']="Acesso Negado"
            return False

        else: Error['text']="Erro ao validar dados\nFavor entrar em contato com o suporte TI"
        return False