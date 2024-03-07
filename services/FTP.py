import ftplib
import os

class FTP():
 
 def __init__(self,hostname,usuario,senha):

    self.hostname=hostname
    self.usuario=usuario
    self.senha=senha

 def conexao(self):
        
        # Connect FTP Server
        ftp_server = ftplib.FTP(self.hostname, self.usuario, self.senha)
        
        # force UTF-8 encoding
        ftp_server.encoding = "utf-8"

        return ftp_server