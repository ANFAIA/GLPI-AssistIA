# GLPI AI Automation

## 🎯 Descripción del Proyecto

Este proyecto busca modernizar y automatizar la plataforma open-source GLPI. La meta es integrar un sistema de agentes de IA para automatizar las respuestas del soporte técnico, optimizar los flujos de trabajo y enriquecer la experiencia de usuario, especialmente para personas sin perfil técnico.

## 🏛️ Arquitectura y Visión General

El núcleo del sistema está diseñado en torno a un flujo de trabajo que se activa con la creación de un ticket en GLPI. La información del ticket es procesada por un sistema de agentes inteligentes (`CrewAI`) que colaboran para analizar, enriquecer y proponer soluciones.

Este `CrewAI` se conecta a herramientas externas (bases de conocimiento, sistemas de monitorización) a través de un **Servidor MCP (Model Context Protocol)**, que actúa como un bus de datos.

### Flujo de Trabajo del Ticket

1.  **Entrada en GLPI**: Un usuario o técnico crea un ticket de incidencia.
2.  **Activación del Agente**: La incidencia se transfiere al sistema `CrewAI` para su procesamiento.
3.  **Análisis por Agentes IA**:
      * **Analista de Emociones**: Evalúa la urgencia y el estado de ánimo del usuario para priorizar el ticket.
      * **Agente Categorizador**: Clasifica la incidencia según las etiquetas predefinidas en GLPI.
      * **Agente GLPI**: Busca en el historial de GLPI incidencias similares o relacionadas para obtener contexto.
      * **Agente Experto en [X]**: Para cada categoría, un agente especializado consulta bases de datos externas como **Wiki.js**, **Zabbix**, etc., a través del Servidor MCP.
      * **Agente Resolutor**: Consolida toda la información, genera un resumen enriquecido y una posible solución.
4.  **Respuesta en GLPI**: La solución y el análisis generados se publican en el ticket de GLPI, asistiendo al técnico o respondiendo directamente al usuario.

## ✨ Características Principales

  * **Resumen y Enriquecimiento de Tickets**: La IA analiza y resume el problema del usuario, añadiendo contexto técnico.
  * **Generación de Plantillas**: Creación automática de plantillas de respuesta técnica.
  * **Integración con Herramientas de Diagnóstico**: Conexión con **Zabbix**, **Wazuh** y **Wiki.js** para obtener datos en tiempo real.
  * **Arquitectura MCP**: Un bus de datos desacoplado para facilitar la comunicación y la escalabilidad.
  * **Información Contextual Inteligente**: Proporciona información relevante tanto a técnicos como a usuarios.

## 📊 Métricas de Éxito

El éxito del proyecto se medirá por la consecución de los siguientes objetivos:

  * Reducción de más del **70%** en el tiempo de primera respuesta.
  * Precisión superior al **85%** en las respuestas automáticas generadas.
  * Reducción de más del **50%** en los tickets que necesitan ser escalados manualmente.
  * Reducción de más del **40%** en el tiempo promedio de resolución de incidencias.
  * Nivel de satisfacción del usuario superior a **4.0/5.0**.

## 🤖 Módulo de agentes (Glpi AssistIA Server)

Sirve como backend que:

1.  Recibe eventos de GLPI (por ejemplo, creación o actualización de tickets).
2.  Orquesta los agentes de IA a través del servidor MCP (`mcp_server.py` en la raíz).
3.  Devuelve al ticket un resumen enriquecido o solución.
-----

### Requisitos

  - **GLPI** versión 10.x o superior (acceso vía API).
  - **Credenciales GLPI:** `GLPI_URL`, `GLPI_APP_TOKEN` y `GLPI_USER_TOKEN`.
  - **Servidor AssistIA** (`glpiassistiaserver/`):
      - Si es **PHP**, requiere **PHP ≥ 8.1** y **Composer**.
      - Si es **Python**, requiere **Python ≥ 3.11**.
  - **MCP (opcional pero recomendado):** `python ≥ 3.11` para ejecutar `mcp_server.py`.
  - **(Opcional)** LLM local si la orquestación usa modelos locales (por ejemplo, Ollama).

-----

### Variables de entorno

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

# LLM/Ollama (si aplica)
OLLAMA_HOST=http://127.0.0.1:11434

# Wiki.js
WIKIJS_URL=http://localhost:8080/
WIKIJS_API_TOKEN=tu_token
```

-----

### Puesta en marcha

1.  **Arranca el MCP** desde la raíz del repo:

<!-- end list -->

```bash
uv pip install -r requirements.txt
python mcp_server.py
```

2.  **Arranca el servidor AssistIA** desde `glpiassistiaserver/`:

<!-- end list -->

  * **PHP (Composer):**

    ```bash
    cd glpiassistiaserver
    composer install
    # Si hay carpeta public/:
    php -S 127.0.0.1:8080 -t public
    ```

  * **Python (FastAPI / Starlette):**

    ```bash
    cd glpiassistiaserver
    uv pip install -r requirements.txt
    uvicorn glpiassistiaserver.webapp:app --host 0.0.0.0 --port 8080 --reload
    ```

-----

### Integración con GLPI - GLPI Tool

Esta herramienta permite a CrewAI buscar resultados en incidencias anteriores y publicar los resultados del informe como nota interna. Para activarlo:

1.  En GLPI → Configuración → API:

      * Habilita la API y genera los tokens.

2.  Configura un **webhook** (o tarea equivalente) que apunte al endpoint del servidor AssistIA, por ejemplo:

    ```
    POST http://TU_ASSISTIA:8080/webhook/glpi
    ```

El servidor validará el evento, invocará MCP y publicará el resultado en el ticket.


-----

### Implementación CrewAI como paquete instalable

El proyecto usa [uv](https://docs.astral.sh/uv/getting-started/installation/) para el desarrollo.

Una vez instalada la utilidad, puedes ejecutar el siguiente comando para ejecutar la interfaz de línea de comandos:

```bash
uv run glpiassistiaserver-cli
```

Para lanzar el servidor HTTP ejecuta:

```bash
uvicorn glpiassistiaserver.webapp:app --reload
```

-----

🧠 Documento realizado por un humano y potenciado por IA
