# This code from https://github.com/FreeOpcUa
from opcua import ua, Server, uamethod
import sys
import time
import datetime
import threading, time, random
import psutil
import xlsxwriter

sys.path.insert(0, "..")

Variavel_Global = None
Echo = []
Ack = []
Data_Client = []
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
def ack_method(parent, value, contador_Dado, numero_cliente):
    global mutex, Ack, Variavel_Global
    
    mutex.acquire()
    
    # Atribui o valor para Variavel_Global
    # Atribui valor para a Confirmação do Cliente que alterou o dado.
    if Variavel_Global != None :
        Variavel_Global.set_value(value)
        Ack[numero_cliente-1].set_value(contador_Dado)
        
    mutex.release()
    return 1

@uamethod
def echo_method(parent, value, numero_cliente):
    global Echo

    # Atribui o valor para Echo do cliente e invocou o metodo.
    if (numero_cliente - 1) < len(Echo):
        #Data_Client[numero_cliente - 1].set_value(value)
        Echo[numero_cliente-1].set_value(value)

    return 1



if __name__ == "__main__":

    server = Server()
    server.set_endpoint(endpoint)
    uri = uri_
    idx = server.register_namespace(uri)
    objects = server.get_objects_node()

    myobj = objects.add_object(idx, "Objeto")
    
    # Gerando as variaveis.
    Variavel_Global = myobj.add_variable(idx, "Variavel", "")
    indice = 1
    while indice <= numero_clientes:
        #
        Data_Client.append (myobj.add_variable(idx, "Data_" + str(indice), ""))
        Echo.append (myobj.add_variable(idx, "Echo_" + str(indice), ""))
        Ack.append (myobj.add_variable(idx, "Ack_" + str(indice), 0))
        # 
        Data_Client[indice - 1].set_writable()
        Echo[indice - 1].set_writable()
        Ack[indice - 1].set_writable()
        indice = indice + 1
        pass
    Variavel_Global.set_writable()
    #myDataDatetime = myobj.add_variable(idx, "MyDataDatetime", 0)
    # Set MyVariable to be writable by clients
    #myDataDatetime.set_writable()


    metodo_ack = ua.Argument()
    metodo_ack.Name = "Confirma_Global"
    #metodo.DataType = ua.NodeId(ua.ObjectIds.Int64)
    metodo_ack.ValueRank = -1
    metodo_ack.ArrayDemisions = []
    metodo_ack.Description = ua.LocalizedText("Confirmação dado Global")

    metodo_echo = ua.Argument()
    metodo_echo.Name = "Echo_Global"
    #metodo.DataType = ua.NodeId(ua.ObjectIds.Int64)
    metodo_echo.ValueRank = -1
    metodo_echo.ArrayDemisions = []
    metodo_ack.Description = ua.LocalizedText("Echo da troca de dados com o Client")

    base = server.get_objects_node()
    base.add_method(1, "Metodo Confirmação Global", ack_method, [metodo_ack])
    base.add_method(1, "Metodo Echo Cliente", echo_method, [metodo_echo])
    
    # populating our address space
        # Set MyVariable to be writable by clients
    # starting!
    server.start()
    try:

        while True:
            pass
            #time.sleep(2)
            #
            #count = Variavel_Global.get_value()
            #if (count != old_count):
            #    old_count = count
            #    print("Temperatura = " + count)

            #count += 0.1
            #myDataDatetime.set_value(datetime.datetime.now())
            #Variavel_Global.set_value(count)
    finally:
        #close connection, remove subcsriptions, etc
        server.stop()
        