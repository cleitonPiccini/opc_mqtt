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
#contador_arquivo = 2
start_mensagens = 0
client = mqtt.Client()

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
    #client.subscribe("teste/cleiton")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    global start_mensagens, semaforo
    
       
    # Confirmacao de Publicação.
    if start_mensagens == 1 and Teste_Ativo == 2:
        dado_broker = msg.payload
        semaforo.release()
        semaforo.release()
    elif start_mensagens == 1:
        semaforo.release()
        semaforo.release()
    
    #print("Feedback")

#client = mqtt.Client()
#client.on_connect = on_connect
#client.on_message = on_message

#client.connect( "localhost", 1883, 60)
#client.on_connect = on_connect
#client.on_message = on_message
#client.publish("teste/cleiton", "teste do publsh", 0)
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
#client.loop_forever()
#client.disconnect()

def start_sub_thread ():
    global client
    client.loop_forever()

def Start(numero_cliente, end, porta, numero_mensagens, tamanho_inicio, tamanho_fim, tipo_teste):
    global worksheet, workbook, Teste_Ativo
    global start_mensagens, semaforo, client

    #client = mqtt.Client()
    client.connect( end, porta, 60)
    client.on_connect = on_connect
    client.on_message = on_message

    Teste_Ativo = tipo_teste

    
    t = threading.Thread(target=start_sub_thread,args=())
    t.start()

    #client = Client(endpoint)
    try:
        print("Inicio do teste - Cliente Número = ", numero_cliente)
        
        #client.connect()
        # Inicia os Tópicos MQTT.
        topico_data = "Teste/Data_" + str(numero_cliente)
        topico_echo = "Teste/Echo_" + str(numero_cliente)
        topico_ack = "Teste/Ack_" + str(numero_cliente)
        topico_var_global = "Teste/Variavel"
        
        time.sleep(2)
        
        # Seleciona o tipo de teste. E cria a assinatura das variaveis.
        if tipo_teste == 1:
            nome_xlsx = "MQTT Teste Ack Cliente - " + str(numero_cliente) + ".xlsx"
            workbook = xlsxwriter.Workbook(nome_xlsx) 
            worksheet = workbook.add_worksheet() 
            Write_Excell(1,'Tempo de ACK', 'Carga Processador', 'Carga Memoria RAM', 'Tamanho do dado')
            client.subscribe(topico_data)
            
        elif tipo_teste == 2:
            nome_xlsx = "MQTT Teste Echo Cliente - " + str(numero_cliente) + ".xlsx"
            workbook = xlsxwriter.Workbook(nome_xlsx) 
            worksheet = workbook.add_worksheet() 
            Write_Excell(1,'Tempo de Echo', 'Carga Processador', 'Carga Memoria RAM', 'Tamanho do dado')
            client.subscribe(topico_echo)

        elif tipo_teste == 3:
            nome_xlsx = "MQTT Teste Ack Variavel Global Cliente - " + str(numero_cliente) + ".xlsx"
            workbook = xlsxwriter.Workbook(nome_xlsx) 
            worksheet = workbook.add_worksheet() 
            Write_Excell(1,'Tempo de ACK', 'Carga Processador', 'Carga Memoria RAM', 'Tamanho do dado')
            client.subscribe(topico_ack)
            
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
        contador_arquivo = 2
        old_time = None
        cpu_old = 0
        ram_old = 0

        # Inicia a troca de mensagens com o Servidor.
        while (contador_tamanho <= int(tamanho_fim)):
            
            # Teste Ack             
            if tipo_teste == 1:               
                if contador_mensagens < numero_mensagens :
                    print("While Tamanho mensagem = ", contador_tamanho, " Ciclo = ", contador_mensagens)
                    start_mensagens = 1
                    mensagem = dado + str(contador_mensagens)
                    Inicio_Timer = datetime.datetime.now()
                    
                    semaforo.acquire()
                    client.publish(topico_data, mensagem)
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
                        old_time = None
                        cpu_old = 0
                        ram_old = 0
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
            
            # Teste Echo
            elif tipo_teste == 2:

                if contador_mensagens < numero_mensagens :
                    
                    start_mensagens = 1

                    # Envia mensagem
                    mensagem = dado + str(contador_mensagens)
                    Inicio_Timer = datetime.datetime.now()
                    semaforo.acquire()
                    client.publish(topico_echo, mensagem)
                    semaforo.acquire()

                    # Rerebe o Valor do Echo.
                    #dado_server = Echo.get_value()
                    #dado_broker = client.msg.payload
                    
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
                        old_time = None
                        cpu_old = 0
                        ram_old = 0
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
                    #device = objects.call_method(method_ack, mensagem, (int(contador_mensagens) + 1), int(numero_cliente))
                    client.publish(topico_var_global, mensagem)
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
                        old_time = None
                        cpu_old = 0
                        ram_old = 0
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
        
    finally:
        client.disconnect()
        print("Fim do teste Cliente Número = ", numero_cliente)

def main(args):
    return args[1]

if __name__ == "__main__":

    arquivo_config = []

    # Le arquivo de configuracao.
    with open("config_client_mqtt.txt", "r") as arquivo:
        for linha in arquivo:
            arquivo_config.append(linha.replace("\n",""))

    numero_clientes = int(arquivo_config[1])
    end = arquivo_config[3]
    porta = int(arquivo_config[5])
    numero_mensagens = int(arquivo_config[7])
    tamanho_inicio = int(arquivo_config[9])
    tamanho_fim = int(arquivo_config[11])
    tipo_teste = int(arquivo_config[13])            

    # Obtem o numero do processo que iniciou o Client.
    numero = main(sys.argv)
    Start(numero, end, porta, numero_mensagens, tamanho_inicio, tamanho_fim, tipo_teste)