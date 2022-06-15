# This code from https://github.com/FreeOpcUa
#from opcua import Client
import time
import sys
sys.path.insert(0, "..")
import opcua
from opcua import client

texto = []

with open("config_client.txt", "r") as arquivo:
    for linha in arquivo:
        #print(linha[len(linha)-1])
        texto.append(linha.replace("\n",""))


try:
    client = opcua.Client("opc.tcp://" + texto[3] + ":" + texto[5])
    # connecting!
    client.connect()
    # Client has a few methods to get proxy to UA nodes that should always be in address space
    root = client.get_root_node()
    
    myData1 = root.get_child(["0:Objects", "2:Objeto", "2:Variavel"])
    Echo = root.get_child(["0:Objects", "2:Objeto", "2:Echo_1"])
    Ack = root.get_child(["0:Objects", "2:Objeto", "2:Ack_1"])
    myDataDatetime = root.get_child(["0:Objects", "2:Objeto", "2:MyDataDatetime"])
    obj = root.get_child(["0:Objects", "2:Objeto"])
    #teste = client.get_name_spece()
    uri = texto[7]
    idx = client.get_namespace_index(uri)
    teste = client.get_objects_node()
    #teste.
    print("Teste Objects is: ", client.get_objects_node())
    objects = client.get_objects_node()
    print("Teste Children of objects are: ", objects.get_children())
    print("Teste do Children  ", objects.get_children()[2].get_browse_name())

    print("meu Objeto é: ", obj)
    print("valor da Variavel é: ", myData1)
    print("myDataDatetime is: ", myDataDatetime)
    print("valor do idx = ", idx)
    print("valor do teste =", teste)

    method = objects.get_children()[2]
    while True:
        #client.set_node("ns=2;i=2").set_value(10)
        #count = myData1.get_value()
        #count = client.get_node(myData1).get_value()
        #count += 0.1
        #myData1.set_value(count)
        #objects.call_method(method, "--Cliente 02--", 0)
        #contador = myData1.get_value()
        #print("Temperatura = %4.1f" %client.get_node(myData1).get_value())
        #print("Variavel = " + client.get_node(myData1).get_value())
        #print("Echo = " + client.get_node(Echo).get_value())
        #print("Ack = " + str (client.get_node(Ack).get_value()))
        #print("Data e hora = ", client.get_node("ns=2;i=3").get_value().strftime("%Y-%m-%d 	%H:%M:%S"))
        time.sleep(1)            
finally:
    client.disconnect()

    myData1.set_value(33)