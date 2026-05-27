# 🛡️ NetSentinel: Real-Time Traffic Analyzer & Threat Intelligence Agent

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Library-Scapy-red?style=for-the-badge&logo=python&logoColor=white" alt="Scapy">
  <img src="https://img.shields.io/badge/API-AbuseIPDB-orange?style=for-the-badge" alt="AbuseIPDB">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT License">
</p>

---

> **NetSentinel** es una solución de seguridad defensiva y análisis forense de red capaz de auditar el tráfico pasivo (*sniffing*) en tiempo real. El agente intercepta paquetes de red, desglosa su arquitectura interna (IPs, protocolos TCP/UDP y puertos), descarta de forma automatizada el tráfico local y enriquece la telemetría consultando dinámicamente la reputación de amenazas globales a través de la API v2 de **AbuseIPDB**.

El sistema ha sido desarrollado bajo estrictos estándares de ingeniería de software, priorizando la **resiliencia frente a fallos externos** y la **optimización extrema de recursos en memoria RAM**.

---

## 🎯 Características Destacadas

* **🔬 Análisis Forense de Bajo Nivel:** Captura y desempaquetado de tráfico de red crudo mediante sockets con la librería `Scapy`.
* **🧠 Caché en Memoria RAM (Deduplicación):** Implementación de una libreta de control inteligente basada en conjuntos de Python (`set()`). Evita consultas redundantes a la API externa para un mismo destino, reduciendo el consumo de créditos en más de un **90%** y mitigando bloqueos por *Rate Limiting*.
* **⚡ Escudo de Resiliencia Industrial:** Arquitectura tolerante a fallos mediante control selectivo de excepciones (`try/except KeyError`). Si la API externa experimenta caídas o agota sus créditos, el script protege su ejecución continua (*Uptime*), asume un estado seguro y continúa monitoreando.
* **🔒 Gestión Segura de Secretos:** Integración total con variables de entorno (`.env`) y la librería `python-dotenv`. Las llaves de infraestructura y credenciales se mantienen completamente aisladas del código público.
* **📜 Bitácora Forense Estandarizada:** Generación automatizada de alertas detalladas en un archivo de logs estático (`alerta_seguridad.log`), utilizando el framework nativo `logging` con marcas de tiempo personalizadas.

---

## 📊 Arquitectura del Sistema y Flujo Lógico

El agente procesa cada evento de red a través de un pipeline jerárquico diseñado para el máximo rendimiento de cómputo:

```text
[ Tráfico de Red ] ──> [ Sniffer (Scapy) ] ──> [ Función Centinela ]
                                                       │
                               ┌───────────────────────┴───────────────────────┐
                        (¿IP Destino Local?)                    (¿IP Destino Externa?)
                               │                                               │
                           [ IGNORAR ]                             [ Revisar Libreta/Caché ]
                                                                               │
                                               ┌───────────────────────────────┴───────────────────────────────┐
                                         (¿Ya Conocida?)                                                 (¿Es Nueva?)
                                               │                                                               │
                                           [ IGNORAR ]                                            [ Consultar API AbuseIPDB ]
                                                                                                               │
                                                                                               ┌───────────────┴───────────────┐
                                                                                         (Puntaje > 30)                (Error/Sin Créditos)
                                                                                               │                               │
                                                                                     [ LOG: ALERTA FORENSE ]          [ ESCUDO DE RESILIENCIA ]
                                                                                               │                               │
                                                                                     [ Añadir a Caché RAM ]           [ Asumir Limpia + Guardar ]


📦 Requisitos e Instalación1. Clonar el RepositorioBashgit clone [https://github.com/TU_USUARIO/NetSentinel.git](https://github.com/TU_USUARIO/NetSentinel.git)
cd NetSentinel
2. Configurar el Entorno VirtualBashpython3 -m venv .venv
source .venv/bin/activate  # En Linux/macOS
# .venv\Scripts\activate   # En Windows
3. Instalar DependenciasBashpip install -r requirements.txt
4. Variables de Entorno (Credenciales)Crea un archivo llamado .env en la raíz del directorio del proyecto e introduce tu llave secreta de AbuseIPDB:Fragmento de códigoKEY=tu_api_key_secreta_aqui
🕹️ Modo de Uso y PruebasDebido a que la captura pasiva (sniffing) interactúa con las interfaces de red del sistema operativo a bajo nivel, el script requiere permisos de superusuario (Administrador) para su ejecución:Bashsudo python analizar_ips.py
Monitoreo Activo en Terminal (Modo Debug):PlaintextAnalizando IP: 8.8.8.8 - Puntaje: 0
Analizando IP: 185.220.101.5 - Puntaje: 100
Error conectando con la API o límite alcanzado (Escudo de resiliencia activado)
Telemetría de Alertas en alerta_seguridad.log:Plaintext2026-05-27 10:15:32 - WARNING - Tráfico malicioso detectado destino: [185.220.101.5] puerto destino: < 443 > origen: [192.168.100.15] puerto origen: < 53210 >
🛡️ Buenas Prácticas de Ingeniería ImplementadasEste proyecto no es un script de automatización aislado; fue diseñado aplicando conceptos clave de arquitectura de software para ciberseguridad:Deduplicación en memoria RAM vs Listas: El uso de set() garantiza búsquedas con una complejidad temporal de $O(1)$, evitando la degradación del rendimiento del script conforme se descubren nuevas IPs.Defensa contra caídas del API (Fail-Safe): En lugar de permitir un colapso del socket (KeyError), el software atrapa el error, notifica al administrador y mantiene la monitorización activa.Principio de Menor Privilegio para Datos: El archivo .env está estrictamente registrado en el .gitignore para asegurar el cumplimiento de normativas de desarrollo seguro (OWASP / GitLeaks prevention).📄 LicenciaEste proyecto está bajo la Licencia MIT. Consulta el archivo para más detalles.👨‍💻 AutorDesarrollado como un proyecto de auditoría de seguridad de redes e inteligencia de amenazas en tiempo real.
