import os 
import psutil 
load1, load5, load15 = psutil.getloadavg() 
  
cpu_usage = (load15/os.cpu_count()) * 100
  
print("The CPU usage is : ", cpu_usage)

total_memory, used_memory, free_memory = map( 
	int, os.popen('free -t -m').readlines()[-1].split()[1:]) 
carga_memoria = (round((used_memory/total_memory) * 100, 2))

print(carga_memoria)