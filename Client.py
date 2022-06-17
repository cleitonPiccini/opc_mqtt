
from opcua import Client
import time
import sys
sys.path.insert(0, "..")
import opcua
import threading, time, random
import os
import psutil
import xlsxwriter
import datetime

Flag_Sub_Echo = 0
Flag_Sub_Ack = 0
Flag_Sub_Data_Cliente = 0
Data_Cliente = None
Echo = None
Ack = None
myData1 = None
mutex = threading.Lock()
workbook = None
worksheet = None
#contador_arquivo = 2
contador_arquivo = 2
diferenca = 0
Inicio_Timer = None
Inicio_Timer = None
contador_tamanho = None
Teste_Ativo = 0

def Subscribe ():

    pass

def Write_Excell (indice, dado_A, dado_D):
    global worksheet

    #if worksheet != None:
        
    #Obtem a carga da CPU
    load1, load5, load15 = psutil.getloadavg()                 
    carga_processador = (load15/os.cpu_count()) * 100
                
    #Obtem a carga da memória
    total_memory, used_memory, free_memory = map(
        int, os.popen('free -t -m').readlines()[-1].split()[1:]) 
    carga_memoria = (round((used_memory/total_memory) * 100, 2))
                
    #Salva os dados no arquivo.
    coluna = 'A'+str(indice)
    worksheet.write(coluna, dado_A)
    coluna = 'B'+str(indice)
    worksheet.write(coluna, carga_processador)
    coluna = 'C'+str(indice)
    worksheet.write(coluna, carga_memoria)
    coluna = 'D'+str(indice)
    worksheet.write(coluna, dado_D)
        #contador_arquivo = contador_arquivo + 1 

class SubHandler(object):

    def datachange_notification(self, node, val, data):
        global mutex, Echo, Ack, Data_Cliente, contador_arquivo, worksheet, Teste_Ativo
        global Inicio_Timer, Flag_Sub_Echo, Flag_Sub_Ack, Flag_Sub_Data_Cliente, contador_tamanho

        #mutex.acquire()
        
        if (Echo == node and Teste_Ativo == 2):
            #if (worksheet != None and Inicio_Timer != None and Echo != None ):
                
            Flag_Sub_Echo = 1
        
        elif (Ack == node and Teste_Ativo == 3):
                        
            Flag_Sub_Ack = 1
            """
            if (worksheet != None and Inicio_Timer != None and contador_tamanho != None):
                
                #Obtem o tempo da troca de dados.
                data_hora = datetime.datetime.now() - Inicio_Timer
                Write_Excell(contador_arquivo, data_hora, contador_tamanho)
                contador_arquivo = contador_arquivo + 1
            """
            
        elif (Data_Cliente == node and Teste_Ativo == 1):
            
            #Flag_Sub_Data_Cliente = 1
            
            if (worksheet != None and Inicio_Timer != None and contador_tamanho != None):
                #print("olhai entrou")
                #Obtem o tempo da troca de dados.
                data_hora = datetime.datetime.now() - Inicio_Timer
                Write_Excell(contador_arquivo, data_hora, contador_tamanho)
                contador_arquivo = contador_arquivo + 1
            

        #mutex.release()

    def event_notification(self, event):
        print("Python: New event", event)

    def data_change(self, handle, node, val, attr):
        """
        Deprecated, use datachange_notification
        """
        print("Teste data change")
        #pass


def Start(numero_cliente, endpoint, uri, numero_mensagens, tamanho_inicio, tamanho_fim, tipo_teste):
    global Echo, Node_Alterado, mutex, Ack, myData1, worksheet, workbook, diferenca, Data_Cliente, Teste_Ativo
    global Inicio_Timer, contador_tamanho, contador_arquivo, Flag_Sub_Echo, Flag_Sub_Ack, Flag_Sub_Data_Cliente

    Teste_Ativo = tipo_teste

    client = Client(endpoint)
    try:
        print("Inicio do teste")
        client.connect()
        root = client.get_root_node()
        nome_data = "2:Data_" + str(numero_cliente)
        print("numero do cliente = ", numero_cliente, "nome da variavel = ", nome_data)
        nome_echo = "2:Echo_" + str(numero_cliente)
        nome_ack = "2:Ack_" + str(numero_cliente)
        myData1 = root.get_child(["0:Objects", "2:Objeto", "2:Variavel"])
        Data_Cliente = root.get_child(["0:Objects", "2:Objeto", nome_data])
        Echo = root.get_child(["0:Objects", "2:Objeto", nome_echo])
        Ack = root.get_child(["0:Objects", "2:Objeto", nome_ack])
        #myDataDatetime = root.get_child(["0:Objects", "2:Objeto", "2:MyDataDatetime"])
        obj = root.get_child(["0:Objects", "2:Objeto"])
        idx = client.get_namespace_index(uri)

        objects = client.get_objects_node()

        #myData1.set_value(" ")
        Data_Cliente.set_value(" ")
        print(Data_Cliente, " olhai ai", numero_cliente)
        Echo.set_value(" ")
        Ack.set_value(0)

        time.sleep(2)
        
        handler = SubHandler()
        sub = client.create_subscription(0, handler)

        
        
        
        
        method_ack = objects.get_children()[2]
        method_echo = objects.get_children()[3]
        dado = "a"
        
        #print("Valor do metodo 1 = ", method_ack)
        #print("Valor do metodo 2 = ", method_echo)

        # Seleciona o tipo de teste.
        if tipo_teste == 1:
            nome_xlsx = "Teste Ack Cliente - " + str(numero_cliente) + ".xlsx"
            workbook = xlsxwriter.Workbook(nome_xlsx) 
            worksheet = workbook.add_worksheet() 
            worksheet.write('A1', 'Tempo de ACK')
            worksheet.write('B1', 'Carga Processador')
            worksheet.write('C1', 'Carga Memoria RAM')
            worksheet.write('D1', 'Tamanho do dado')
            handle = sub.subscribe_data_change(Data_Cliente)
            

        elif tipo_teste == 2:
            nome_xlsx = "Teste Echo Cliente - " + str(numero_cliente) + ".xlsx"
            workbook = xlsxwriter.Workbook(nome_xlsx) 
            worksheet = workbook.add_worksheet() 
            worksheet.write('A1', 'Tempo de Echo')
            worksheet.write('B1', 'Carga Processador')
            worksheet.write('C1', 'Carga Memoria RAM')
            worksheet.write('D1', 'Tamanho do dado')
            handle = sub.subscribe_data_change(Echo)
            

        elif tipo_teste == 3:
            nome_xlsx = "Teste Ack Variavel Global Cliente - " + str(numero_cliente) + ".xlsx"
            workbook = xlsxwriter.Workbook(nome_xlsx) 
            worksheet = workbook.add_worksheet() 
            worksheet.write('A1', 'Tempo de ACK')
            worksheet.write('B1', 'Carga Processador')
            worksheet.write('C1', 'Carga Memoria RAM')
            worksheet.write('D1', 'Tamanho do dado')
            handle = sub.subscribe_data_change(Ack)
            

        else:
            print("Erro no tipo de teste")

        contador_tamanho = 1
        
        # Atribui o valor inicial do dado para o servidor.
        while (contador_tamanho < int(tamanho_inicio)):
            dado = dado + dado
            contador_tamanho = contador_tamanho + 1

        #device = objects.call_method(method, "--Cliente--", 0)
        contador_mensagens = 0

        while (contador_tamanho <= int(tamanho_fim)):
            
            
            # Teste Ack             
            if tipo_teste == 1:
                #print("oiiiiii")                
                if contador_mensagens < numero_mensagens :
                    mensagem = dado + str(contador_mensagens)
                    Inicio_Timer = datetime.datetime.now()
                    Data_Cliente.set_value(mensagem)
                    """
                    Flag_Sub_Data_Cliente = 0
                    Flag_Primeiro = 0
                    
                    while Flag_Sub_Data_Cliente == 0:
                        if Flag_Primeiro == 0:
                            Data_Cliente.set_value(mensagem)    
                            Flag_Primeiro = 1        
                    
                    #Obtem o tempo da troca de dados.
                    data_hora = datetime.datetime.now() - Inicio_Timer
                    #Salva os dados no arquivo.
                    Write_Excell(contador_arquivo, data_hora, contador_tamanho)
                    contador_arquivo = contador_arquivo + 1
                    """
                    contador_mensagens = contador_mensagens + 1 
                else:
                    dado = dado * 2
                    contador_mensagens = 0                
                    contador_tamanho = contador_tamanho * 2
                time.sleep(0.2)
            
            # Teste Echo
            elif tipo_teste == 2:

                if contador_mensagens < numero_mensagens :
                    mensagem = dado + str(contador_mensagens)
                    Inicio_Timer = datetime.datetime.now()
                    Flag_Sub_Echo = 0
                    Flag_Primeiro = 0
                    #device = objects.call_method(method_echo, mensagem, numero_cliente)
                    while Flag_Sub_Echo == 0 :
                        #print("Aguardando retorno")
                        if Flag_Primeiro == 0:
                            device = objects.call_method(method_echo, mensagem, numero_cliente)
                            Flag_Primeiro = 1

                    # Rerebe o Valor do Echo.
                    dado_server = Echo.get_value()
                    #Obtem o tempo da troca de dados.
                    data_hora = datetime.datetime.now() - Inicio_Timer
                    #Salva os dados no arquivo.
                    Write_Excell(contador_arquivo, data_hora, contador_tamanho)
                    contador_arquivo = contador_arquivo + 1
                    contador_mensagens = contador_mensagens + 1 
                else:
                    dado = dado * 2
                    contador_mensagens = 0                
                    contador_tamanho = contador_tamanho * 2
                time.sleep(0.3)

            elif tipo_teste == 3:
                
                if contador_mensagens < numero_mensagens :
                    mensagem = dado + str(contador_mensagens)
                    Inicio_Timer = datetime.datetime.now()
                    #device = objects.call_method(method_ack, mensagem, (contador_mensagens), numero_cliente)        
                    
                    Flag_Sub_Ack = 0
                    Flag_Primeiro = 0
                    while Flag_Sub_Ack == 0:
                        if Flag_Primeiro == 0:
                            device = objects.call_method(method_ack, mensagem, contador_mensagens + 1, numero_cliente)        
                            Flag_Primeiro = 1
                    #Obtem o tempo da troca de dados.
                    data_hora = datetime.datetime.now() - Inicio_Timer
                    #Salva os dados no arquivo.
                    Write_Excell(contador_arquivo, data_hora, contador_tamanho)
                    contador_arquivo = contador_arquivo + 1
                    
                    contador_mensagens = contador_mensagens + 1 
                else:
                    time.sleep(0.5)
                    dado = dado * 2
                    contador_mensagens = 0                
                    contador_tamanho = contador_tamanho * 2
                time.sleep(0.5)

            else:
                break

        time.sleep(5)
        workbook.close()
        time.sleep(5)
        sub.unsubscribe(handle)
        time.sleep(5)
        sub.delete()
        print("Fim do teste")
 
    finally:
        client.disconnect()