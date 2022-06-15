# This code from https://github.com/FreeOpcUa
from opcua import ua, Server, uamethod
import sys
import time
import datetime
import threading, time, random
import psutil
import xlsxwriter

sys.path.insert(0, "..")

myData1 = None
Echo = []
Ack = []
arquivo_config = []
mutex = threading.Lock()

with open("config_client.txt", "r") as arquivo:
    for linha in arquivo:
        arquivo_config.append(linha.replace("\n",""))

endpoint = "opc.tcp://" + arquivo_config[3] + ":" + arquivo_config[5]
uri_ = arquivo_config[7]
numero_clientes = int(arquivo_config[1])
numero_mensagens = int(arquivo_config[9])
tamanho_inicio = int(arquivo_config[11])
tamanho_fim = int(arquivo_config[13])


@uamethod
def set_var(parent, value, numero_cliente):
    global mutex
    mutex.acquire()
    #
    value = str(myData1.get_value()) + " " + value
    myData1.set_value(value)
    Echo[numero_cliente-1].set_value(value)
    Ack[numero_cliente-1].set_value(1)
    #opc.set_node("ns=2;i=2").set_value(10)
    #client.set_node("ns=2;i=2").set_value(10)
    #print("olha o parante ai",parent)
    mutex.release()
    return 1



if __name__ == "__main__":

    server = Server()
    server.set_endpoint(endpoint)
    uri = uri_
    idx = server.register_namespace(uri)
    objects = server.get_objects_node()

    myobj = objects.add_object(idx, "Objeto")
    # Gerando as variaveis.
    myData1 = myobj.add_variable(idx, "Variavel", "")
    #Echo = []
    #Ack = []
    indice = 1
    while indice <= numero_clientes:
        Echo.append (myobj.add_variable(idx, "Echo_" + str(indice), ""))
        Ack.append (myobj.add_variable(idx, "Ack_" + str(indice), 0))
        Echo[indice - 1].set_writable()
        Ack[indice - 1].set_writable()
        indice = indice + 1
        pass
    
    myDataDatetime = myobj.add_variable(idx, "MyDataDatetime", 0)
    myData1.set_writable()    # Set MyVariable to be writable by clients
    myDataDatetime.set_writable()


    metodo = ua.Argument()
    metodo.Name = "Variavel_Valor"
    #metodo.DataType = ua.NodeId(ua.ObjectIds.Int64)
    metodo.ValueRank = -1
    metodo.ArrayDemisions = []
    metodo.Description = ua.LocalizedText("Valor da Variavel")

    base = server.get_objects_node()
    base.add_method(1, "Teste de metodo", set_var, [metodo])
    
    # populating our address space
        # Set MyVariable to be writable by clients
    # starting!
    server.start()
    try:
        count = ""
        old_count = ""

        count = myData1.get_value()
        myData1.set_value(count)

        old_count = myData1.get_value()
        
        while True:
            pass
            #time.sleep(2)
            #
            #count = myData1.get_value()
            #if (count != old_count):
            #    old_count = count
            #    print("Temperatura = " + count)

            #count += 0.1
            #myDataDatetime.set_value(datetime.datetime.now())
            #myData1.set_value(count)
    finally:
        #close connection, remove subcsriptions, etc
        server.stop()
        