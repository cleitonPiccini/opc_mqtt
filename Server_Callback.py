import sys
sys.path.insert(0, "..")
import datetime
from datetime import datetime

try:
    from IPython import embed
except ImportError:
    import code

    def embed():   
        vars = globals()
        vars.update(locals())
        #shell = code.InteractiveConsole(vars)
        #shell.interact()
        #while True:
        #    pass



texto = []

with open("config_client.txt", "r") as arquivo:
    for linha in arquivo:
        #print(linha[len(linha)-1])
        texto.append(linha)


from opcua import ua, uamethod, Server
from opcua.common.callback import CallbackType



def create_monitored_items(event, dispatcher):
    print("Monitored Item")     

    for idx in range(len(event.response_params)) :
        if (event.response_params[idx].StatusCode.is_good()) :
            nodeId = event.request_params.ItemsToCreate[idx].ItemToMonitor.NodeId
            print("Node {0} was created".format(nodeId))     
         
    
def modify_monitored_items(event, dispatcher):
    print('modify_monitored_items')


def delete_monitored_items(event, dispatcher):
    print('delete_monitored_items')


if __name__ == "__main__":


    # now setup our server
    server = Server()
    #server.disable_clock()
    #server.set_endpoint("opc.tcp://localhost:4840/freeopcua/server/")
    server.set_endpoint("opc.tcp://" + texto[3] + ":" + texto[5])
    #server.set_server_name("FreeOpcUa Example Server")

    # setup our own namespace
    uri = texto[7]
    idx = server.register_namespace(uri)

    # get Objects node, this is where we should put our custom stuff
    objects = server.get_objects_node()

    # populating our address space
    myfolder = objects.add_folder(idx, "myEmptyFolder")
    myobj = objects.add_object(idx, "Objeto")

    myData1 = myobj.add_variable(idx, "Variavel", 0)
    myDataDatetime = myobj.add_variable(idx, "MyDataDatetime", 0)
    myData1.set_writable()
    myDataDatetime.set_writable()

    # starting!
    server.start()
    
        
    # Create Callback for item event 
    server.subscribe_server_callback(CallbackType.ItemSubscriptionCreated, create_monitored_items)
    server.subscribe_server_callback(CallbackType.ItemSubscriptionModified, modify_monitored_items)
    server.subscribe_server_callback(CallbackType.ItemSubscriptionDeleted, delete_monitored_items)
    
   
    #print("Available loggers are: ", logging.Logger.manager.loggerDict.keys())
    try:
        # enable following if you want to subscribe to nodes on server side
        embed()
    finally:
        server.stop()