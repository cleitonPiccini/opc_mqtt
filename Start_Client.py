import threading
import time
import sys
sys.path.insert(0, "..")

import opcua
import Client

texto = []

with open("config_client.txt", "r") as arquivo:
    for linha in arquivo:
        #print(linha[len(linha)-1])
        texto.append(linha)

def teste(nome):
    Client.Start(texto[3], texto[5], nome)

#__main__#

i = 0
t = []

while (i < int(texto[1])):
    
    nome = "thread N = " + (str (i))
    t.append(threading.Thread(target=teste,args=(nome,))) 
    t[i].start()
    i = i + 1
    time.sleep(1)
    #t2 = threading.Thread(target=teste,args=())
    #t2.start()