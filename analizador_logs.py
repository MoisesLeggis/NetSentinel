import re
from collections import Counter

with open('alerta_seguridad.log', 'r', encoding = 'utf-8') as archivo:
    lista_ips = []
    for linea in archivo:
        encontrar_ips = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", linea)
        if encontrar_ips:
            extraer_ips = encontrar_ips.group()
            lista_ips.append(extraer_ips)

contador = Counter(lista_ips)
print("=========================================")
print("REPORTE DE INCIDENTES DE SEGURIDAD") 
print("=========================================")
print(f"Total de alertas registradas: {len(lista_ips)}")
print("IPs Maliciosas Detectadas:")
for ip, num_veces in contador.items():
    print(f"- IP: {ip}  | Avistamientos: {num_veces} veces")
print("=========================================")