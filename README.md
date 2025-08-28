# GLPI AssistIA
Este README está disponible en varios idiomas: [Español](README.md) | [Galego](README.gl.md) | [English](README.en.md)

## 🎯 Caso de uso

La gestión de incidencias, especialmente en departamentos de IT, requiere de tareas que muchas veces son repetitivas como revisar Wikis, documentación o la ejecución de comandos como Ping a determinados servidores. GLPI AssistIA busca reducir toda esta carga con un informe previo de la incidencia a tratar. Una vez se registra una incidencia en el sistema, esta se envía a un servidor (GLPI AssistIA Server) que genera un informe con posíbles soluciones, este informe estará visible para el agente que trate esta incidencia como una nota provada en el momento que tome el caso reduciendo los tiempos de respuesta.

## 🏗️ Arquitectura y Visión General
El núcleo del sistema está diseñado en torno a un flujo de trabajo que se activa con la creación de un ticket en GLPI. La información del ticket es procesada por un sistema de agentes inteligentes (`CrewAI`) que colaboran para analizar, enriquecer y proponer soluciones.

Este `CrewAI` se conecta a herramientas externas (bases de conocimiento, sistemas de monitorización) a través de un **Servidor MCP (Model Context Protocol)**, que actúa como un bus de datos.

### Flujo de Trabajo del Ticket
![Diagrama de Arquitectura V3](https://raw.githubusercontent.com/ANFAIA/GLPI-AssistIA/c81ce359886bd2f5c9111d7a7446144947432ea3/docs/BigPicture%20V3.svg)

1.  **Entrada en GLPI**: Un usuario o técnico crea un ticket de incidencia.
2.  **Activación del Agente**: La incidencia se transfiere al sistema `CrewAI` alojado en GLPI AssistIA Server para su procesamiento.
3.  **Análisis por Agentes IA**:
      * **Analista de Emociones**: Evalúa la urgencia y el estado de ánimo del usuario para priorizar el ticket.
      * **Agente Categorizador**: Clasifica la incidencia según las etiquetas predefinidas en GLPI.
      * **Agente Resolutor**: Revisa los datos disponibles en Wiki.js, incidencias anteriores de GLPI y realiza Pings (En caso de problemas de conexión). Finalmente consolida toda la información, genera un resumen enriquecido y una posible solución.
4.  **Respuesta en GLPI**: La solución y el análisis generados se publican en el ticket de GLPI, asistiendo al técnico o respondiendo directamente al usuario.



## ✨ Características Principales

  * **Resumen y Enriquecimiento de Tickets**: La IA analiza y resume el problema del usuario, añadiendo contexto técnico.
  * **Arquitectura MCP**: Un bus de datos desacoplado para facilitar la comunicación y la escalabilidad.
  * **Información Contextual Inteligente**: Proporciona información relevante tanto a técnicos como a usuarios.

## Requisitos
- **GLPI** versión 10.x o superior (acceso vía API).
- **Credenciales GLPI:** `GLPI_URL`, `GLPI_APP_TOKEN` y `GLPI_USER_TOKEN`.
- **Servidor AssistIA** (`glpiassistiaserver/`):
  - Si es **PHP**, requiere **PHP ≥ 8.1** y **Composer**.
  - Si es **Python**, requiere **Python ≥ 3.11**.
- **MCP (opcional pero recomendado):** `python ≥ 3.11` para ejecutar `mcp_server.py`.
- **(Opcional)** LLM local si la orquestación usa modelos locales (por ejemplo, Ollama).



## Variables de entorno
Crea un archivo `.env` que contenga:

```env
# GLPI
GLPI_URL=https://tu-glpi.example.com
GLPI_API_URL=https://mi.glpi/apirest.php
GLPI_APP_TOKEN=xxx
GLPI_USER_TOKEN=yyy
GLPI_VERIFY_SSL=true

# MCP
MCP_HOST=127.0.0.1
MCP_PORT=8765

# Proveedor de LLM (Introduce una línea)
OLLAMA_HOST=[HOST DE OLLAMA]
CEREBRAS_API_KEY=[API KEY]
GROQ_API_KEY=[API KEY]

# Wiki.js
WIKIJS_URL=http://localhost:8080/
WIKIJS_API_TOKEN=tu_token
```

## Puesta en marcha
### Servidor
El sistema consta de dos servidores, el primero es WebApp que recibirá las incidencias. Puedes iniciarlo con el siguiente comando desde el directorio principal del repositorio:
uvicorn glpiassistiaserver.webapp:app --host 0.0.0.0 --port 8089 --reload

El segundo es MCP Server, que realizará las comunicaciones entre GLPI AssistIA Server y las herramientas. Puedes iniciarlo ejecutando directamente el script mcp_server.py (Si deseas cambiar algún dato puedes usar el comando uvicorn como hicimos en el paso anterior).

### Instalación plugin
Deberás de mover la carpeta glpiassistia a la carpeta de plugins de tu GLPI e instalarla. Una vez instalado deberás de entrar en configuración, activar la opción de GLPI AssistIA, establecer la dirección de GLPI AssistIA Server y guardar los datos. Una vez realizados estos pasos deberás de activar el plugin en el apartado de plugins. Cada vez que se cree una incidencia será enviada al servidor.

## Capturas de Pantalla
### Casos prácticos
A continuación se muestra el procesamiento de una incidencia de ejemplo

<img width="475.25" height="226.75" alt="APERTURA INCIDENCIA" src="https://github.com/user-attachments/assets/06465e4f-4ed0-4f21-8a60-67f224985b2a" />
<img width="421.25" height="196.5" alt="PROCESAMIENTO" src="https://github.com/user-attachments/assets/2547cee4-0c46-48ef-a622-03cb887ab306" />

<img width="475.5" height="228" alt="RES" src="https://github.com/user-attachments/assets/cbfadd07-f0a8-4314-9fbb-fb51cc9aae94" />
<img width="475.75" height="228" alt="RES2" src="https://github.com/user-attachments/assets/b2a81c28-b1f1-43b0-a075-8c82ee3dcdc6" />

### Plugin
A continuación se muestra la interfaz del plugin

<img width="475.5" height="226.75" alt="CONFIGURACION" src="https://github.com/user-attachments/assets/58d67305-c90a-48a0-8980-1af7b5af24fa" />

## Video de configuración rápida y ejemplo práctico
En el siguiente video se muestra la configuración del plugin y un ejemplo de uso
[![GLPIASSISTIA](https://img.youtube.com/vi/Me0OWoNrdao/0.jpg)](https://www.youtube.com/watch?v=Me0OWoNrdao)


## 📊 Métricas de Éxito

El éxito del proyecto se medirá por la consecución de los siguientes objetivos:

  * Reducción de más del **70%** en el tiempo de primera respuesta.
  * Precisión superior al **85%** en las respuestas automáticas generadas.
  * Reducción de más del **50%** en los tickets que necesitan ser escalados manualmente.
  * Reducción de más del **40%** en el tiempo promedio de resolución de incidencias.
  * Nivel de satisfacción del usuario superior a **4.0/5.0**.
---
  ## 🤝 Colaboración
  Este proyecto ha sido posíble gracias al programa de Becas de Verano de ANFAIA y la colaboración de Aitire
