# This code from https://github.com/FreeOpcUa
from opcua import ua, Server
import sys
import time
import datetime
sys.path.insert(0, "..")


texto = []

with open("config_client.txt", "r") as arquivo:
    for linha in arquivo:
        #print(linha[len(linha)-1])
        texto.append(linha)

if __name__ == "__main__":
    # setup our server
    server = Server()
    server.set_endpoint("opc.tcp://" + texto[3] + ":" + texto[5])
    # setup our own namespace, not really necessary but should as spec
    uri = texto[7]
    idx = server.register_namespace(uri)
    objects = server.get_objects_node()

    myobj = objects.add_object(idx, "Objeto")
    myData1 = myobj.add_variable(idx, "Variavel", 0)
    myDataDatetime = myobj.add_variable(idx, "MyDataDatetime", 0)
    myData1.set_writable()    # Set MyVariable to be writable by clients
    myDataDatetime.set_writable()

    
    # populating our address space
        # Set MyVariable to be writable by clients
    # starting!
    server.start()
    try:
        count = 0
        old_count = 0

        count = myData1.get_value()
        myData1.set_value(count)

        old_count = myData1.get_value()
        
        while True:
            time.sleep(2)
            #
            count = myData1.get_value()
            if (count != old_count):
                old_count = count
                print("Temperatura = %4.1f" %count)

            #count += 0.1
            myDataDatetime.set_value(datetime.datetime.now())
            #myData1.set_value(count)
    finally:
        #close connection, remove subcsriptions, etc
        server.stop()
        