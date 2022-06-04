# This code from https://github.com/FreeOpcUa
#from opcua import Client
import time
import sys
sys.path.insert(0, "..")
import opcua


def Start(end_ip, porta, servidor, nome):

    print (nome)
    client = opcua.Client("opc.tcp://" + end_ip + ":" + porta)
    try:
        # connecting!
        client.connect()
        # Client has a few methods to get proxy to UA nodes that should always be in address space
        root = client.get_root_node()
        myData1 = root.get_child(["0:Objects", "2:Objeto", "2:Variavel"])
        myDataDatetime = root.get_child(["0:Objects", "2:Objeto", "2:MyDataDatetime"])
        obj = root.get_child(["0:Objects", "2:Objeto"])
        #teste = client.get_name_spece()
        uri = servidor
        idx = client.get_namespace_index(uri)
        
        print("Teste Objects is: ", client.get_objects_node())
        objects = client.get_objects_node()
        print("Teste Children of objects are: ", objects.get_children())

        print("meu Objeto é: ", obj)
        print("valor da Variavel é: ", myData1)
        print("myDataDatetime is: ", myDataDatetime)
        print("valor do idx = ", idx)
        while True:
            #client.set_node("ns=2;i=2").set_value(10)
            count = myData1.get_value()
            count += 0.1
            myData1.set_value(count)
            print("Temperatura = %4.1f" %client.get_node("ns=2;i=2").get_value())
            print("Data e hora = ", client.get_node("ns=2;i=3").get_value().strftime("%Y-%m-%d 	%H:%M:%S"))
            time.sleep(2)            
    finally:
        client.disconnect()