import sys
sys.path.insert(0, "..")
import time
import logging

from opcua import Client
from opcua import ua

arquivo_config = []

with open("config_client.txt", "r") as arquivo:
    for linha in arquivo:
        arquivo_config.append(linha.replace("\n",""))

endpoint = "opc.tcp://" + arquivo_config[3] + ":" + arquivo_config[5]
uri_ = arquivo_config[7]
numero_clientes = int(arquivo_config[1])
numero_mensagens = int(arquivo_config[9])
tamanho_inicio = int(arquivo_config[11])
tamanho_fim = int(arquivo_config[13])

class SubHandler(object):

    def datachange_notification(self, node, val, data):
        print("Python: New data change event", node)

    def event_notification(self, event):
        print("Python: New event", event)


if __name__ == "__main__":
    client = Client(endpoint)
    try:
        client.connect()
        root = client.get_root_node()

        myData1 = root.get_child(["0:Objects", "2:Objeto", "2:Variavel"])
        Echo = root.get_child(["0:Objects", "2:Objeto", "2:Echo_1"])
        Ack = root.get_child(["0:Objects", "2:Objeto", "2:Ack_1"])
        myDataDatetime = root.get_child(["0:Objects", "2:Objeto", "2:MyDataDatetime"])
        obj = root.get_child(["0:Objects", "2:Objeto"])
        uri = texto[7]
        idx = client.get_namespace_index(uri)

        objects = client.get_objects_node()

        handler = SubHandler()
        sub = client.create_subscription(500, handler)
        handle = sub.subscribe_data_change(Echo)
        #handle = sub.subscribe_data_change()
        #handle = sub.subscribe_data_change(myData1)

        method = objects.get_children()[2]
        #device = objects.get_child(["2:MyObjects", "2:MyDevice"])
        #method = device.get_child("2:MyMethod")
        #result = d.call_method(method, ua.Variant("sin"), ua.Variant(180, ua.VariantType.Double))
        device = objects.call_method(method, "--Cliente--", 0)
        #print("Mehtod result is: ", device)

        while True:
            device = objects.call_method(method, "--Cliente--", 0)
            pass

        #device = objects.call_method(method, "--Cliente--")
        #print("Mehtod result is: ", result)

        #embed()
        time.sleep(3)
        sub.unsubscribe(handle)
        sub.delete()
        #client.close_session()
    finally:
        client.disconnect()