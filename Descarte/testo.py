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


try:
    from IPython import embed
except ImportError:
    import code

    def embed():
        vars = globals()
        vars.update(locals())
        shell = code.InteractiveConsole(vars)
        shell.interact()


from opcua import Client


class SubHandler(object):

    """
    Subscription Handler. To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another
    thread if you need to do such a thing
    """
    def event_notification(self, event):
        print("New event recived: ", event)


if __name__ == "__main__":

    client = Client("opc.tcp://" + texto[3] + ":" + texto[5])
    # client = Client("opc.tcp://admin@localhost:4840/freeopcua/server/") #connect using a user
    try:
        # connecting!
        client.connect()
        # Client has a few methods to get proxy to UA nodes that should always be in address space
        root = client.get_root_node()
        myData1 = root.get_child(["0:Objects", "2:Objeto", "2:Variavel"])
        myDataDatetime = root.get_child(["0:Objects", "2:Objeto", "2:MyDataDatetime"])
        obj = root.get_child(["0:Objects", "2:Objeto"])
        #teste = client.get_name_spece()
        uri = texto[7]
        idx = client.get_namespace_index(uri)
        
        print("Teste Objects is: ", client.get_objects_node())
        objects = client.get_objects_node()
        print("Teste Children of objects are: ", objects.get_children())

        myevent = root.get_child(["0:Types", "0:EventTypes", "0:BaseEventType", "2:MyFirstEvent"])
        print("MyFirstEventType is: ", myevent)

        msclt = SubHandler()
        sub = client.create_subscription(100, msclt)
        handle = sub.subscribe_events(objects, myevent)

        embed()
        sub.unsubscribe(handle)
        sub.delete()
    finally:
        client.disconnect()