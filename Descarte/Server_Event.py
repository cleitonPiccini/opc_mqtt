import sys
sys.path.insert(0, "..")
import logging


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

from opcua import ua, Server


if __name__ == "__main__":
    #logging.basicConfig(level=logging.WARN)
    #logger = logging.getLogger("opcua.server.internal_subscription")
    #logger.setLevel(logging.DEBUG)

    # setup our server
    server = Server()
    server.set_endpoint("opc.tcp://" + texto[3] + ":" + texto[5])

    # setup our own namespace, not really necessary but should as spec
    uri = texto[7]
    idx = server.register_namespace(uri)

    # get Objects node, this is where we should put our custom stuff
    objects = server.get_objects_node()

    # populating our address space
    myobj = objects.add_object(idx, "MyObject")
    myData1 = myobj.add_variable(idx, "Variavel", 0)
    myDataDatetime = myobj.add_variable(idx, "MyDataDatetime", 0)
    myData1.set_writable()    # Set MyVariable to be writable by clients
    myDataDatetime.set_writable()

    # Creating a custom event: Approach 1
    # The custom event object automatically will have members from its parent (BaseEventType)
    etype = server.create_custom_event_type(idx, 'MyFirstEvent', ua.ObjectIds.BaseEventType, [('MyNumericProperty', ua.VariantType.Float), ('MyStringProperty', ua.VariantType.String)])

    myevgen = server.get_event_generator(etype, myobj)

    # Creating a custom event: Approach 2
    custom_etype = server.nodes.base_event_type.add_object_type(2, 'MySecondEvent')
    custom_etype.add_property(2, 'MyIntProperty', ua.Variant(0, ua.VariantType.Int32))
    custom_etype.add_property(2, 'MyBoolProperty', ua.Variant(True, ua.VariantType.Boolean))

    mysecondevgen = server.get_event_generator(custom_etype, myobj)

    # starting!
    server.start()

    try:
        # time.sleep is here just because we want to see events in UaExpert
        import time
        count = 0
        while True:
            time.sleep(5)
            myevgen.event.Message = ua.LocalizedText("MyFirstEvent %d" % count)
            myevgen.event.Severity = count
            myevgen.event.MyNumericProperty = count
            myevgen.event.MyStringProperty = "Property " + str(count)
            myevgen.trigger()
            mysecondevgen.trigger(message="MySecondEvent %d" % count)
            count += 1

        embed()
    finally:
        # close connection, remove subcsriptions, etc
        server.stop()