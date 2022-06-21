
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
semaforo = threading.Semaphore(2)
workbook = None
worksheet = None
#contador_arquivo = 2
contador_arquivo = 2
diferenca = 0
Inicio_Timer = None
contador_tamanho = None
Teste_Ativo = 0
start_mensagens = 0

def Subscribe ():

    pass

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
        #contador_arquivo = contador_arquivo + 1 

class SubHandler(object):

    def datachange_notification(self, node, val, data):
        global mutex, Echo, Ack, Data_Cliente, contador_arquivo, worksheet, Teste_Ativo
        global Inicio_Timer, Flag_Sub_Echo, Flag_Sub_Ack, Flag_Sub_Data_Cliente, contador_tamanho
        global start_mensagens, semaforo
        
        # Confirmacao de escrita no Echo
        if (Echo == node and Teste_Ativo == 2 ):                
            #Flag_Sub_Echo = 1
            if start_mensagens == 1 :
                semaforo.release()
                semaforo.release()
        
        # Confirmacao de escrita no ACK
        elif (Ack == node and Teste_Ativo == 3 ):
            #Flag_Sub_Ack = 1
            if start_mensagens == 1 :
                semaforo.release()
                semaforo.release()

        # Confirmacao de escrita na Data_Cliente
        elif (Data_Cliente == node and Teste_Ativo == 1 ):
            #Flag_Sub_Data_Cliente = 1
            if start_mensagens == 1 :
                semaforo.release()
                semaforo.release()

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

        # Inicia a troca de mensagens com o Servidor.
        while (contador_tamanho <= int(tamanho_fim)):
            
            # Teste Ack             
            if tipo_teste == 1:               
                if contador_mensagens < numero_mensagens :
                    
                    start_mensagens = 1
                    mensagem = dado + str(contador_mensagens)
                    Inicio_Timer = datetime.datetime.now()
                    
                    semaforo.acquire()
                    Data_Cliente.set_value(mensagem)
                    semaforo.acquire()

                    #Obtem o tempo da troca de dados.
                    atraso_mensagem = datetime.datetime.now() - Inicio_Timer
                    
                    if old_time == None :
                        old_time = atraso_mensagem
                    else:    
                        old_time = atraso_mensagem + old_time
                    media_tempo = ((old_time.total_seconds() * 1000) / (contador_mensagens + 1))
                    
                    cpu_old = carga_cpu() + cpu_old
                    media_cpu = cpu_old / (contador_mensagens + 1)
                    ram_old = carga_ram() + ram_old
                    media_ram = ram_old / (contador_mensagens + 1)
                    
                    #Salva os dados no arquivo. Salva quando o teste estiver na metade das mensagens.
                    if contador_mensagens == int(numero_mensagens / 2):
                        Write_Excell(contador_arquivo, media_tempo, media_cpu, media_ram, contador_tamanho)    
                        contador_arquivo = contador_arquivo + 1
                    
                    contador_mensagens = contador_mensagens + 1
                else:
                    #print("Trocou o tamanho = ", contador_tamanho)
                    #Salva os dados no arquivo.
                    Write_Excell(contador_arquivo, media_tempo, media_cpu, media_ram, contador_tamanho)
                    dado = dado * 2
                    contador_mensagens = 0
                    old_time = None
                    cpu_old = 0
                    ram_old = 0              
                    contador_tamanho = contador_tamanho * 2
                    contador_arquivo = contador_arquivo + 1
                time.sleep(0.3)
            
            # Teste Echo
            elif tipo_teste == 2:

                if contador_mensagens < numero_mensagens :
                    
                    start_mensagens = 1

                    # Envia mensagem
                    mensagem = dado + str(contador_mensagens)
                    Inicio_Timer = datetime.datetime.now()
                    semaforo.acquire()
                    Echo.set_value(mensagem)
                    semaforo.acquire()

                    # Rerebe o Valor do Echo.
                    dado_server = Echo.get_value()
                    
                    #Obtem o tempo da troca de dados.
                    atraso_mensagem = datetime.datetime.now() - Inicio_Timer
                    if old_time == None :
                        old_time = atraso_mensagem
                    else:    
                        old_time = atraso_mensagem + old_time                        
                    media_tempo = ((old_time.total_seconds() * 1000) / (contador_mensagens + 1))
                    
                    #Obtem a carga da CPU
                    cpu_old = carga_cpu() + cpu_old
                    media_cpu = cpu_old / (contador_mensagens + 1)
                    
                    #Obtem a carga da Memoria RAM
                    ram_old = carga_ram() + ram_old
                    media_ram = ram_old / (contador_mensagens + 1)

                    #Salva os dados no arquivo. Salva quando o teste estiver na metade das mensagens.
                    if contador_mensagens == int(numero_mensagens / 2):
                        Write_Excell(contador_arquivo, media_tempo, media_cpu, media_ram, contador_tamanho)    
                        contador_arquivo = contador_arquivo + 1

                    contador_mensagens = contador_mensagens + 1 
                else:
                    #Salva os dados no arquivo.
                    Write_Excell(contador_arquivo, media_tempo, media_cpu, media_ram, contador_tamanho)
                    dado = dado * 2
                    contador_mensagens = 0
                    old_time = None
                    cpu_old = 0
                    ram_old = 0
                    contador_tamanho = contador_tamanho * 2
                    contador_arquivo = contador_arquivo + 1
                time.sleep(0.3)

            # Teste Ack - Todos os Clientes escrevem na mesma variavel do server
            elif tipo_teste == 3:
                
                if contador_mensagens < numero_mensagens :
                    
                    start_mensagens = 1

                    # Envia mensagem
                    mensagem = dado + str(contador_mensagens)
                    Inicio_Timer = datetime.datetime.now()
                    semaforo.acquire()
                    device = objects.call_method(method_ack, mensagem, (int(contador_mensagens) + 1), int(numero_cliente))
                    semaforo.acquire()

                    #Obtem o tempo da troca de dados.
                    atraso_mensagem = datetime.datetime.now() - Inicio_Timer
                    if old_time == None :
                        old_time = atraso_mensagem
                    else:    
                        old_time = atraso_mensagem + old_time
                    media_tempo = ((old_time.total_seconds() * 1000) / (contador_mensagens + 1))
                    
                    #Obtem a carga da CPU
                    cpu_old = carga_cpu() + cpu_old
                    media_cpu = cpu_old / (contador_mensagens + 1)
                    
                    #Obtem a carga da Memoria RAM
                    ram_old = carga_ram() + ram_old
                    media_ram = ram_old / (contador_mensagens + 1)

                    #Salva os dados no arquivo. Salva quando o teste estiver na metade das mensagens.
                    if contador_mensagens == int(numero_mensagens / 2):
                        Write_Excell(contador_arquivo, media_tempo, media_cpu, media_ram, contador_tamanho)    
                        contador_arquivo = contador_arquivo + 1
                    
                    contador_mensagens = contador_mensagens + 1 
                else:
                    #Salva os dados no arquivo.
                    Write_Excell(contador_arquivo, media_tempo, media_cpu, media_ram, contador_tamanho)
                    dado = dado * 2
                    contador_mensagens = 0
                    old_time = None
                    cpu_old = 0
                    ram_old = 0
                    contador_tamanho = contador_tamanho * 2
                    contador_arquivo = contador_arquivo + 1
                time.sleep(0.3)

            else:
                break

        time.sleep(2)
        workbook.close()
        time.sleep(2)
        sub.unsubscribe(handle)
        time.sleep(2)
        sub.delete()
        
    finally:
        client.disconnect()
        print("Fim do teste Cliente Número = ", numero_cliente)

def main(args):
    return args[1]

if __name__ == "__main__":

    arquivo_config = []

    # Le arquivo de configuracao.
    with open("config_client.txt", "r") as arquivo:
        for linha in arquivo:
            arquivo_config.append(linha.replace("\n",""))

    endpoint = "opc.tcp://" + arquivo_config[3] + ":" + arquivo_config[5]
    uri = arquivo_config[7]
    numero_clientes = int(arquivo_config[1])
    numero_mensagens = int(arquivo_config[9])
    tamanho_inicio = int(arquivo_config[11])
    tamanho_fim = int(arquivo_config[13])
    tipo_teste = int(arquivo_config[15])            

    # Obtem o numero do processo que iniciou o Client.
    numero = main(sys.argv)
    Start(numero, endpoint, uri, numero_mensagens, tamanho_inicio, tamanho_fim, tipo_teste)