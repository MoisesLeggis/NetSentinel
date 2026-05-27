from scapy.all import IP, sniff, TCP, UDP
import logging
import requests

import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("KEY")

#Memoria para almacenar las ips que pasaron el test, para no saturar la api
memoria_ips_conocida = set()



#CREAR REGISTROS  DE WARNINGS
logging.basicConfig(
    level = logging.WARNING,
    format = '%(asctime)s - %(levelname)s - %(message)s' ,
    datefmt='%Y-%m-%d %H:%M:%S',               
    filename='alerta_seguridad.log',                         
    filemode='a'  
)



#FUNCION PARA CATALOGAR SI ES DIRECCION MALICIOSA  O LIMPIA
def direcciones_malas(ip):
    # Obtenemos la url de abuseipdb
    url = 'https://api.abuseipdb.com/api/v2/check'
    #Dando la ip
    querystring = {
        'ipAddress': ip,
        'maxAgeInDays': '90'
    }
    #Credenciales
    headers = {
        'Accept': 'application/json',
        'Key':  api_key
    }
    # Llamamos a la api
    response = requests.request(method='GET', url=url, headers=headers, params=querystring)
    #Obtenemos los datos que nos devolvio la api
    datos_ip = response.json()
    try:
        #Accedemos al diccionerario y buscamos el score del riesgo
        puntaje_atacante = datos_ip['data']['abuseConfidenceScore']
        #Impresion para el test
        print(f"Analizando IP: {ip} - Puntaje: {puntaje_atacante}")
        if puntaje_atacante > 30:
            return 'DIRECCION MALICIOSA'
        else:
            return 'DIRECCION LIMPIA'
    except KeyError:
        print("Límite gratuito alcanzado")
        return 'DIRECCION LIMPIA'


#FUNCION PARA DETECTAR Y LEER UN PAQUETE IP

def centinela(paquete):

    #se verifica si cuenta con el paquete ip
    paquete_ip = paquete.haslayer(IP)
    #Se verifica si cuenta con el control de transmision
    paquete_tcp = paquete.haslayer(TCP)
    #Se verifica si cuenta con datagrama de usuario (velocidad y latencia)
    paquete_udp = paquete.haslayer(UDP)

    puerto_origen = 'N/A'
    puerto_destino = 'N/A'

    

    if paquete_ip :
        #Se obtienen las ips de origen y destino
        ip_origen = paquete[IP].src
        ip_destino = paquete[IP].dst
        
        if paquete_tcp:
            puerto_origen = paquete[TCP].sport
            puerto_destino = paquete[TCP].dport
            
        elif paquete_udp:
            puerto_origen = paquete[UDP].sport
            puerto_destino = paquete[UDP].dport
        #Si la ip de destino empieza con mi red local entonces se descarta
        if ip_destino.startswith("RANGO-DE-TU-IP"):
            pass
        #De lo contrario, se pasa la ip de destino a la funcion de direcciones malas para la catologacion
        else:
            if ip_destino in memoria_ips_conocida:
                pass
            else:
                resultado = direcciones_malas(ip_destino)
                memoria_ips_conocida.add(ip_destino)
                if resultado == 'DIRECCION MALICIOSA':
                    #Se activia el registro estructurando su contenido
                    logging.warning(f"Tráfico malicioso detectado destino: [{ip_destino}] puerto destino: < {puerto_destino} >  origen: [{ip_origen}] puerto origen: < {puerto_origen} > ")
                else:
                    pass


#Se caputaran los paquetes ips
paquetes_capturados = sniff(
    filter = "ip",
    prn = centinela,
    store = False
)