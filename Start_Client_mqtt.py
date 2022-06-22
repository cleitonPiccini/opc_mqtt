import subprocess
import threading
import time
import sys
import os
sys.path.insert(0, "..")

def start_client (numero):
    os.system("python3 Client_mqtt.py " + str(numero))    

arquivo_config = []

# Le arquivo de configuracao.
with open("config_client_mqtt.txt", "r") as arquivo:
    for linha in arquivo:
        arquivo_config.append(linha.replace("\n",""))

numero_clientes = int(arquivo_config[1])
end = arquivo_config[3]
porta = int(arquivo_config[5])
numero_mensagens = int(arquivo_config[7])
tamanho_inicio = int(arquivo_config[9])
tamanho_fim = int(arquivo_config[11])
tipo_teste = int(arquivo_config[13]) 

i = 1
t = []

while (i <= numero_clientes):
    
    t.append(threading.Thread(target=start_client,args=(i,))) 
    t[i-1].start()
    i = i + 1