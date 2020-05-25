# Importo libreria Flask y la dependiencias (modulo de la libreria) Flask y request de Flask
from flask import Flask, request
#Importo las dependencias Resource y Api de flask_restful
from flask_restful import Resource, Api


import json #Importo la libreria json
import datetime #Importo libreria que maneja fechas




#Inicializo la APi
app = Flask(__name__) #inicializacion de las librerias
api = Api(app)

#Creo el endpoint
class Server(Resource): #Creamos una clase llamada server, que funciona como un endpoint
    #Defino la información http como post
    def post(self): #post es el metodo que permita enviar informacion a un endpoint
        #Obtengo la información desde el agente
        server_info = request.data #request guarda informacion del cliente / agente es todo aquel que invoca el metodo post de la api, guardo la info que envia el agente
        server_ip = request.remote_addr # Agente envia respuesta y agrego informacion de IP para mostrarla en el nombre del archivo

        #Procedimiento para nombrar el archivo
        #<IP de servidor>_<AAAA-MM-DD>

        fecha = datetime.datetime.now().strftime('%Y-%m-%d') #
                #Obtengo fecha actual   #Convieto la fecha en el formato texto solicitado
        
        #Abro el archivo informacion.txt
        f = open(server_ip + '_' + fecha + '.json', 'wb') #Abro el archivo en modo binario
        #Escribo lo que mandó el agente
        f.write(server_info)
        #Cierro el archivo
        f.close()
        #Devuelvo la respuesta al agente
        return 'OK'

# Integro el endpoint 'informacion' al API
api.add_resource(Server, '/informacion') #información es el nombre del endpoint

if __name__ == '__main__': #sirve referenciar de donde se esta ejecutando el comando de python
    #Inicio el servidor en el puerto 1234
    app.run(host = '0.0.0.0', port = 1234, debug = True)
