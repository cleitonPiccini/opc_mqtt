
from opcua import Client
import time
import sys
sys.path.insert(0, "..")
import opcua
import threading, time, random

Flag_Alterado = 0
Echo = None
Ack = None
mutex = threading.Lock()

def Subscribe ():

    pass

class SubHandler(object):

    def datachange_notification(self, node, val, data):
        #mutex.acquire()
        global mutex, Echo
        mutex.acquire()
        
        if (Echo == node):
            print("Esse é o Echo", node)
        else:
            print("Esse não é Echo", node)


        mutex.release()
        #print("Python: New data change event", self.get_node(node).get_value())
        #print("Echo = ", Echo, " node = ",node)
        #if Echo == node:
            #print("Python: New data change event", node)
        
        #print("myData1 = %4.1f" %client.get_node("ns=2;i=2").get_value())
        #pass

    def event_notification(self, event):
        print("Python: New event", event)

    def data_change(self, handle, node, val, attr):
        """
        Deprecated, use datachange_notification
        """
        print("Teste data change")
        #pass


def Start(numero_cliente, endpoint, uri, numero_mensagens, tamanho_inicio, tamanho_fim):
    global Echo, Flag_Alterado, Node_Alterado, mutex, Ack
    client = Client(endpoint)
    try:
        client.connect()
        root = client.get_root_node()
        nome_echo = "2:Echo_" + str(numero_cliente)
        nome_ack = "2:Ack_" + str(numero_cliente)
        myData1 = root.get_child(["0:Objects", "2:Objeto", "2:Variavel"])
        Echo = root.get_child(["0:Objects", "2:Objeto", nome_echo])
        Ack = root.get_child(["0:Objects", "2:Objeto", nome_ack])
        myDataDatetime = root.get_child(["0:Objects", "2:Objeto", "2:MyDataDatetime"])
        obj = root.get_child(["0:Objects", "2:Objeto"])
        idx = client.get_namespace_index(uri)

        objects = client.get_objects_node()
        handler = SubHandler()
        sub = client.create_subscription(0, handler)
        handle = sub.subscribe_data_change(Echo)
        handle = sub.subscribe_data_change(Ack)

        method = objects.get_children()[2]

        dado = "a"
        print("Passei aqui um Echo =", Echo)
        contador_tamanho = 1
        while True:
            
            if contador_tamanho < int(tamanho_inicio):
                dado = dado + dado
                contador_tamanho = contador_tamanho + 1
            else :
                break
            pass
        #device = objects.call_method(method, "--Cliente--", 0)
        contador_mensagens = 0
        while True:
            if contador_tamanho <= int(tamanho_fim):       
                if contador_mensagens < numero_mensagens:
                    print("Passei aqui ", contador_mensagens, "TAMANHO = ", contador_tamanho, "Número processo = ", numero_cliente)
                    mensagem = "Contador = " + str(contador_mensagens) + "Tamanho = " + str(contador_tamanho) + "Cliente = " + str(numero_cliente)
                    device = objects.call_method(method, mensagem, numero_cliente)
                    #mutex.acquire()
                        
                    contador_mensagens = contador_mensagens + 1   
                else:
                    #print("Dado = ", dado )
                    dado = dado * 2
                    contador_mensagens = 0
                
                    contador_tamanho = contador_tamanho * 2
            else:
                break
            
            #device = objects.call_method(method, "--Cliente--", 0)
            

        time.sleep(5)
        sub.unsubscribe(handle)
        sub.delete()
 
    finally:
        client.disconnect()