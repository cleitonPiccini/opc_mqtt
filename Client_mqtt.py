import paho.mqtt.client as mqtt
import time
import sys
sys.path.insert(0, "..")
import threading, time, random
import os
import psutil
import xlsxwriter
import datetime


semaforo = threading.Semaphore(2)
workbook = None
worksheet = None
contador_arquivo = 2
start_mensagens = 0

def carga_cpu ():    
    #Obtem a carga da CPU
    load1, load5, load15 = psutil.getloadavg()                 
    carga_processador = (load15/os.cpu_count()) * 100
    return carga_processador

def carga_ram ():
    #Obtem a carga da memória
    total_memory, used_memory, free_memory = map( int, os.popen('free -t -m').readlines()[-1].split()[1:]) 
    carga_memoria = (round((used_memory/total_memory) * 100, 2))
    return carga_memoria

def Write_Excell (indice, dado_A, dado_B, dado_C, dado_D):
    global worksheet
                
    #Salva os dados no arquivo.
    coluna = 'A'+str(indice)
    worksheet.write(coluna, dado_A)
    coluna = 'B'+str(indice)
    worksheet.write(coluna, dado_B)
    coluna = 'C'+str(indice)
    worksheet.write(coluna, dado_C)
    coluna = 'D'+str(indice)
    worksheet.write(coluna, dado_D)
    
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("teste/cleiton")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    global start_mensagens, semaforo
        
    # Confirmacao de Publicação.
    if start_mensagens == 1 :
        semaforo.release()
        semaforo.release()

client = mqtt.Client()
#client.on_connect = on_connect
#client.on_message = on_message

client.connect( "localhost", 1883, 60)

client.publish("teste/cleiton", "teste do publsh", 0)
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
client.disconnect()


def Start(numero_cliente, endpoint, uri, numero_mensagens, tamanho_inicio, tamanho_fim, tipo_teste):
    global Echo, Node_Alterado, mutex, Ack, myData1, worksheet, workbook, diferenca, Data_Cliente, Teste_Ativo
    global Inicio_Timer, contador_tamanho, contador_arquivo, Flag_Sub_Echo, Flag_Sub_Ack, Flag_Sub_Data_Cliente
    global start_mensagens, semaforo

    Teste_Ativo = tipo_teste

    client = Client(endpoint)
    try:
        print("Inicio do teste - Cliente Número = ", numero_cliente)
        
        client.connect()
        # Inicia as variaveis OPC UA.
        root = client.get_root_node()
        nome_data = "2:Data_" + str(numero_cliente)
        nome_echo = "2:Echo_" + str(numero_cliente)
        nome_ack = "2:Ack_" + str(numero_cliente)
        myData1 = root.get_child(["0:Objects", "2:Objeto", "2:Variavel"])
        Data_Cliente = root.get_child(["0:Objects", "2:Objeto", nome_data])
        Echo = root.get_child(["0:Objects", "2:Objeto", nome_echo])
        Ack = root.get_child(["0:Objects", "2:Objeto", nome_ack])
        obj = root.get_child(["0:Objects", "2:Objeto"])
        idx = client.get_namespace_index(uri)

        objects = client.get_objects_node()
        Data_Cliente.set_value(" ")
        Echo.set_value(" ")
        Ack.set_value(0)

        time.sleep(2)
        
        #Cria a assinatura das variaveis.
        handler = SubHandler()
        sub = client.create_subscription(0, handler)        
        method_ack = objects.get_children()[2]
        method_echo = objects.get_children()[3]

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
        
        # Atribui o valor inicial do dado para o servidor.
        dado = "a"
        contador_tamanho = 1
        while (contador_tamanho < int(tamanho_inicio)):
            dado = dado + dado
            contador_tamanho = contador_tamanho + 1

        # Variaveis de resultado do teste.
        contador_mensagens = 0
        old_time = None
        cpu_old = 0
        ram_old = 0



def main(args):
    return args[1]

if __name__ == "__main__":

    arquivo_config = []

    # Le arquivo de configuracao.
    with open("config_client.txt", "r") as arquivo:
        for linha in arquivo:
            arquivo_config.append(linha.replace("\n",""))

    numero_clientes = int(arquivo_config[1])
    end = arquivo_config[3]
    porta = arquivo_config[5]
    numero_mensagens = int(arquivo_config[7])
    tamanho_inicio = int(arquivo_config[9])
    tamanho_fim = int(arquivo_config[11])
    tipo_teste = int(arquivo_config[13])            

    # Obtem o numero do processo que iniciou o Client.
    numero = main(sys.argv)
    Start(numero, end, porta, numero_mensagens, tamanho_inicio, tamanho_fim, tipo_teste)