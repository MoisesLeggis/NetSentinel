# 🛡️ NetSentinel: Real-Time Traffic Analyzer & Threat Intelligence Agent

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Library-Scapy-red?style=for-the-badge&logo=python&logoColor=white" alt="Scapy">
  <img src="https://img.shields.io/badge/API-AbuseIPDB-orange?style=for-the-badge" alt="AbuseIPDB">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT License">
</p>

---

## 📌 Descripción General

> **NetSentinel** es una solución de seguridad defensiva y análisis forense de red capaz de auditar el tráfico pasivo (*sniffing*) en tiempo real.

El agente intercepta paquetes de red, desglosa su arquitectura interna (**IPs, protocolos TCP/UDP y puertos**), descarta automáticamente tráfico local y enriquece la telemetría consultando dinámicamente la reputación de amenazas globales mediante la API v2 de **AbuseIPDB**.

El sistema fue desarrollado bajo estándares modernos de ingeniería de software, priorizando:

- ⚡ **Resiliencia frente a fallos externos**
- 🧠 **Optimización extrema de recursos**
- 🔒 **Seguridad de credenciales**
- 📊 **Monitoreo forense continuo**

---

# 🎯 Características Destacadas

## 🔬 Análisis Forense de Bajo Nivel

Captura y desempaquetado de tráfico de red crudo utilizando sockets mediante la librería `Scapy`.

---

## 🧠 Caché Inteligente en RAM (Deduplicación)

Implementación de una libreta de control basada en `set()` de Python para evitar consultas repetidas a la API externa.

✅ Reduce consumo de créditos en más de **90%**  
✅ Mitiga bloqueos por *Rate Limiting*  
✅ Mejora el rendimiento general del sistema

---

## ⚡ Escudo de Resiliencia Industrial

Arquitectura tolerante a fallos mediante manejo selectivo de excepciones:

```python
try:
    ...
except KeyError:
    ...
```

Si la API externa falla, se queda sin créditos o responde de forma inválida:

- ❌ El sistema NO colapsa
- ✅ El monitoreo continúa activo
- ✅ Se asume un estado seguro temporal

---

## 🔒 Gestión Segura de Secretos

Integración completa con:

- `.env`
- `python-dotenv`

Las credenciales nunca se almacenan directamente en el código fuente.

---

## 📜 Bitácora Forense Estandarizada

Generación automática de alertas mediante el módulo nativo `logging`.

Archivo generado:

```bash
alerta_seguridad.log
```

Incluye:

- Timestamp
- IP origen
- IP destino
- Puertos involucrados
- Nivel de severidad

---

# 📊 Arquitectura del Sistema y Flujo Lógico

El agente procesa cada evento de red a través de un pipeline jerárquico diseñado para el máximo rendimiento de cómputo:

```text
[ Tráfico de Red ]
          │
          ▼
[ Sniffer (Scapy) ]
          │
          ▼
[ Función Centinela ]
          │
 ┌────────┴────────┐
 │                 │
 ▼                 ▼
¿IP Local?     ¿IP Externa?
 │                 │
 ▼                 ▼
IGNORAR      Revisar Caché RAM
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
   ¿Ya conocida?           ¿Es nueva?
        │                       │
        ▼                       ▼
    IGNORAR          Consultar AbuseIPDB
                                │
                ┌───────────────┴───────────────┐
                │                               │
                ▼                               ▼
        Score > 30                     Error / Sin créditos
                │                               │
                ▼                               ▼
     LOG: ALERTA FORENSE          Escudo de resiliencia
                │                               │
                ▼                               ▼
       Añadir a Caché RAM        Asumir limpia y continuar
```

---

# 📦 Requisitos e Instalación

## 1️⃣ Clonar el Repositorio

```bash
git clone https://github.com/TU_USUARIO/NetSentinel.git
cd NetSentinel
```

---

## 2️⃣ Configurar Entorno Virtual

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

---

## 3️⃣ Instalar Dependencias

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Variables de Entorno (Credenciales)

Crear un archivo `.env` en la raíz del proyecto:

```env
KEY=tu_api_key_secreta_aqui
```

---

# 🕹️ Modo de Uso y Pruebas

Debido a que el *sniffing* interactúa con interfaces de red a bajo nivel, el programa requiere privilegios de administrador.

## ▶️ Ejecutar el Monitor

```bash
sudo python analizar_ips.py
```

---

# 🖥️ Monitoreo Activo en Terminal (Modo Debug)

```text
Analizando IP: 8.8.8.8 - Puntaje: 0
Analizando IP: 185.220.101.5 - Puntaje: 100
Error conectando con la API o límite alcanzado (Escudo de resiliencia activado)
```

---

# 🚨 Telemetría de Alertas

Archivo:

```bash
alerta_seguridad.log
```

Contenido:

```text
2026-05-27 10:15:32 - WARNING - Tráfico malicioso detectado destino: [185.220.101.5] puerto destino: <443> origen: [192.168.100.15] puerto origen: <53210>
```

---

# 🛡️ Buenas Prácticas de Ingeniería Implementadas

## ⚡ Complejidad O(1) con `set()`

El uso de estructuras hash evita degradación del rendimiento conforme aumenta el número de IPs detectadas.

---

## 🧯 Arquitectura Fail-Safe

El software evita colapsos causados por:

- APIs caídas
- Timeouts
- Créditos agotados
- Respuestas inválidas

Manteniendo el monitoreo siempre activo.

---

## 🔐 Principio de Menor Privilegio

El archivo `.env` debe estar registrado en `.gitignore` para evitar exposición accidental de credenciales.

Ejemplo:

```gitignore
.env
```

---

# 📚 Tecnologías Utilizadas

| Tecnología | Propósito |
|---|---|
| Python 3 | Lenguaje principal |
| Scapy | Captura y análisis de paquetes |
| AbuseIPDB API | Inteligencia de amenazas |
| Logging | Telemetría forense |
| dotenv | Gestión segura de credenciales |

---

# 📄 Licencia

Este proyecto está bajo la licencia **MIT**.

Consulta el archivo:

```bash
LICENSE
```

para más información.

---

# 👨‍💻 Autor

### NetSentinel Security Research Project

Desarrollado con enfoque en:

- Ciberseguridad defensiva
- Threat Intelligence
- Ingeniería de software resiliente
- Análisis forense de red

---
