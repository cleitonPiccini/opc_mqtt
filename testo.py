# This code from https://github.com/FreeOpcUa
#from opcua import Client
import time
import sys
sys.path.insert(0, "..")
import opcua


texto = []

with open("config_client.txt", "r") as arquivo:
    for linha in arquivo:
        #print(linha[len(linha)-1])
        texto.append(linha.replace("\n",""))

#texto[3] = texto[3].replace("\n","")
print(texto[3])
print(texto[5])
print(texto[7])