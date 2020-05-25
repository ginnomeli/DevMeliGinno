import os #Importa la libreria Os de python => para ejecutar comandos en linux / windows
import sys # Importa la libreria Sys de Python
import json # Importa la libreria Json de Python, convierto la estructura {} en JSON para poder enviarla al API
import http.client # Importa la libreria htttp.client de Python

#Configura la conexión con el API
conexion = http.client.HTTPConnection ('localhost:1234')
endpoint = 'informacion'


#Obtiene la informacion de la pataforma
sistema_operativo = sys.platform #comando que me trae la info del tipo de sistema wind/lin
comando_cpuinfo = '' #incializo la variable
comando_procesos = ''
comando_usuarios = ''
so = ''
comando_version = ''

print(sistema_operativo)

#Si el sistema operativo es Windows
if sistema_operativo == 'win32':
    comando_cpuinfo = 'wmic cpu get name /value' # cargo el comando en la variable #/value cambio el formato de salida de la información para que sea 
    comando_procesos = 'tasklist'                # presentada de forma más clara y prolija
    comando_usuarios = 'whoami'
    so = 'Windows'
    comando_version = 'wmic os get Caption /value'
    
    
#Si el sistema operativo es Linux
elif sistema_operativo == 'linux2':
    comando_cpuinfo = 'cat /proc/cpuinfo'
    comando_procesos = 'ps -a'
    comando_usuarios = 'w -h'
    so = 'Linux'
    comando_version = 'lsb_release -d'
    

#Si el sistema operativo no cumple las condiciones anteriores (es diferente a Windows o Linux)
else:
    print ('SISTEMA OPERATIVO NO COMPATIBLE')
    sys.exit()#OS no compatible, no corre el agente

# os.popen() Ejecuta el comando en el terminal del SO:
# read() lee la respuesta del terminal
# strip()elimina los espacios en la respuesta
# splitlines() separa la información en lineas

cpuinfo = os.popen(comando_cpuinfo).read().strip() # os.popen en un metodo que va a ejecutar el comando en el servidor del SO
procesos = os.popen(comando_procesos).read().strip().splitlines() #genero una lista (no es texto) es un vector
usuarios = os.popen(comando_usuarios).read().strip()
version = os.popen(comando_version).read().strip()

# Enviar la informacion al API
informacion = {
    "cpu": str(cpuinfo),#transforma el texto en formato utf-8 que es el formato que acepta JSON
    "procesos": procesos, # me trae informacion a partir de la segunda linea [2:] #no uso str porque es lista, no texto
    "usuarios": str(usuarios),
    "so": str(so),
    "version": str(version)
} #Estructura/diccionario, transformo la codificación del texto 

conexion.request('POST', endpoint, json.dumps(informacion))
respuesta = conexion.getresponse()
print(respuesta.read())
conexion.close()
