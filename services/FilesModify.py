class FilesModify:

    def __init__(self):
        pass

    def modificarArquivo(string,novastring):
        
        try:

            search_text = "#innodb_force_recovery"
            replace_text = "innodb_force_recovery = 6"

            with open(r'/etc/mysql/mysql.conf.d/mysqld.cnf', 'r') as file:

                data = file.read()
                data = data.replace(string, novastring)

            with open(r'/etc/mysql/mysql.conf.d/mysqld.cnf', 'w') as file:

                file.write(data)

            print("Arquivo modificado")

            return True

        except Exception as e: 

            print(e) 
            
            return e