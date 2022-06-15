import threading
import time
import sys
sys.path.insert(0, "..")

import opcua
import Client

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

def teste(numero):
    Client.Start(numero,endpoint, uri, numero_mensagens, tamanho_inicio, tamanho_fim)

#__main__#

i = 1
t = []

while (i <= numero_clientes):
    
    nome = "thread N = " + (str (i))
    t.append(threading.Thread(target=teste,args=(i,))) 
    t[i-1].start()
    i = i + 1
    #time.sleep(1)
    #t2 = threading.Thread(target=teste,args=())
    #t2.start()

#nome = "thread N = " + (str (i))
#t.append(threading.Thread(target=teste,args=(i,))) 
#t[0].start()
#i = i + 1
#time.sleep(1)