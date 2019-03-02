import ftputil

servidor = 'ftp.ita.es'
usuario = 'hackathon020'
contrasenha = '257yyuFRU'
import os

def download_data():
    with ftputil.FTPHost(servidor, usuario, contrasenha) as host:

        # descarga de la ENTRADA
        host.chdir('ENTRADA')
        entrada = host.listdir(host.curdir)
        print(entrada)
        host.download(entrada[0], os.getcwd() + '/datos/' + entrada[0])

        host.chdir('..')

        # subir a SALIDA
        '''host.chdir('SALIDA')
        salida = host.listdir(host.curdir)
        print(salida)
        host.upload(salida[0], os.getcwd() + '/datos/' + salida[0])'''


download_data()





