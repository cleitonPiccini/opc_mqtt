import subprocess
import threading
import time
import sys
import os
sys.path.insert(0, "..")

import opcua
import Client

#from teste_1 import Client
#from teste_2 import Client

teste_1 = Client
teste_2 = Client

arquivo_config = []

with open("config_client.txt", "r") as arquivo:
    for linha in arquivo:
        arquivo_config.append(linha.replace("\n",""))

endpoint = "opc.tcp://" + arquivo_config[3] + ":" + arquivo_config[5]
uri = arquivo_config[7]
numero_clientes = int(arquivo_config[1])
numero_mensagens = int(arquivo_config[9])
tamanho_inicio = int(arquivo_config[11])
tamanho_fim = int(arquivo_config[13])
tipo_teste = int(arquivo_config[15])

def teste_(numero):
    teste_1.Start(numero,endpoint, uri, numero_mensagens, tamanho_inicio, tamanho_fim, tipo_teste)

def teste(numero):
    teste_2.Start(numero,endpoint, uri, numero_mensagens, tamanho_inicio, tamanho_fim, tipo_teste)

def start_client (numero):
    os.system("python3 Client.py " + str(numero))    

#__main__#

i = 1
t = []


while (i <= numero_clientes):
    
    nome = "thread N = " + (str (i))
    t.append(threading.Thread(target=start_client,args=(i,))) 
    t[i-1].start()
    i = i + 1
    #time.sleep(1)
    #t2 = threading.Thread(target=teste,args=())
    #t2.start()

#t.append(threading.Thread(target=teste_,args=(1,))) 
#t[0].start()
#t.append(threading.Thread(target=teste,args=(2,))) 
#t[1].start()

#nome = "thread N = " + (str (i))
#t.append(threading.Thread(target=teste,args=(i,))) 
#t[0].start()
#i = i + 1
#time.sleep(1)

"""
while (i <= numero_clientes):
    os.system("python3 Client.py " + str(i))
    #subprocess.run(["python3 Client.py " + str(i)])
    i = i + 1
"""    