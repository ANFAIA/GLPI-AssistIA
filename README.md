# GLPI AI Agent - Prototipo Inicial

Este proyecto implementa un agente de inteligencia artificial que se integra con la plataforma de helpdesk GLPI para generar resúmenes automáticos de tickets y optimizar los flujos de trabajo técnicos.

Para más información puedes visitar el Readme de la rama principal del proyecto

---
# VERSIÓN 1 (Carpeta Old)

**Nota**: Este prototipo está diseñado para funcionar sin credenciales reales de GLPI, usando datos simulados para demostrar la funcionalidad de generación de resúmenes con IA. 


## Requisitos de Software

### 1. Python 3.x
- **Versión recomendada**: Python 3.11 o superior
- **Incluye**: pip para instalar dependencias

### 2. Ollama (Programa externo)
- **Estado**: Debe estar instalado y ejecutándose
- **Modelo requerido**: `phi3:mini`
- **Puerto por defecto**: 11434
- **Comandos necesarios**:
  ```bash
  ollama serve          # Iniciar el servidor
  ollama pull phi3:mini # Descargar el modelo
  ```

### 3. Dependencias de Python
Archivo `requirements.txt`:
```
python-dotenv==1.0.0
requests==2.31.0
```


## Orden de Instalación

1. **Instalar Python 3.x**
   - Descargar desde [python.org](https://python.org)
   - Verificar instalación: `python --version`

2. **Instalar Ollama**
   - Descargar desde [ollama.ai](https://ollama.ai)
   - Verificar instalación: `ollama --version`

3. **Descargar modelo de IA**
   ```bash
   ollama pull phi3:mini
   ```

4. **Instalar dependencias de Python**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configurar variables de entorno** (opcional)
   - Crear archivo `.env` con la configuración de GLPI

6. **Ejecutar el agente**
   ```bash
   python src/agent.py
   ```

   ---
# Versión 2 (Implementación CrewAI)

Este documento detalla los pasos necesarios para configurar y ejecutar el sistema de agentes inteligentes basado en **CrewAI**. El sistema está diseñado para analizar, clasificar y proponer soluciones a incidencias de soporte técnico.

## 1\. Requisitos Previos

Antes de empezar, asegúrate de tener instalado y configurado lo siguiente:

### Python

Es necesario tener instalado Python en tu sistema con las siguientes dependencias:
    ```bash
    pip install crewai langchain-community python-dotenv requests
    ```
### Ollama

El motor de los agentes funciona con modelos de lenguaje ejecutados localmente a través de Ollama.

1.  **Instala Ollama**: Sigue las instrucciones de instalación desde [ollama.ai](https://ollama.ai).
2.  **Descarga los modelos necesarios**: Este proyecto utiliza modelos específicos para cada agente con el fin de optimizar el rendimiento. Ejecuta los siguientes comandos para descargarlos:
    ```bash
    ollama pull qwen3
    ollama pull deepseek-coder
    ollama pull deepseek-r1
    ```
3.  **Inicia el servidor de Ollama**: Asegúrate de que Ollama se esté ejecutando en segundo plano. Por defecto, estará disponible en `http://localhost:11434`.

## 2\. Configuración

Sigue estos pasos para configurar el entorno de ejecución:

### Archivo de Incidencia

El script principal (`main_demo.py`) lee la incidencia a analizar desde un fichero de texto. En próximas veriones esta tarea será realizada por main.py, que leera la incidencia y proporcionará el informe directamente en GLPI.

1.  Asegúrate de que exista un archivo llamado **`incidencia.txt`** en la carpeta `CrewAi`.
2.  El contenido de este archivo debe ser la descripción de la incidencia que quieres que los agentes analicen. Puedes usar el siguiente ejemplo:
    ```
    TÍTULO: Usuario no puede acceder a la red corporativa desde su portátil

    DESCRIPCIÓN INICIAL:
    El usuario Juan Pérez (juan.perez@empresa.com) reporta que desde esta mañana no puede conectarse a la red corporativa desde su portátil Dell Latitude 5520. El equipo muestra el mensaje "No se puede conectar a esta red" cuando intenta conectarse al WiFi de la oficina. El usuario confirma que la contraseña es correcta y que otros dispositivos en la misma ubicación funcionan normalmente.
    ```

### Herramientas (Tools)

El `buscador_soluciones` utiliza herramientas para diagnosticar problemas.

  * **Wiki.js Tool**: Si deseas conectar el agente a una base de conocimiento de Wiki.js, debes editar el archivo `CrewAi/tools/wikijs_tool.py` y configurar las variables `WIKIJS_URL` y `WIKIJS_API_TOKEN` con tus credenciales.
  * **Ping Tool**: Si deseas que el agente realice un ping a una página, deberás de indicarlo en el campo habilitado. Por defecto está establecida una dirección genérica.

## 3\. Ejecución

Una vez completados los requisitos y la configuración, puedes ejecutar el sistema de agentes.

1.  Navega hasta la carpeta `CrewAi` en tu terminal.
2.  Ejecuta el script de demostración:
    ```bash
    python main_demo.py
    ```

El script iniciará el "Crew", que procesará la incidencia de manera secuencial a través de sus agentes. Verás en la terminal el razonamiento de cada agente y el resultado final, que será un informe guardado en `informe_soluciones.md`.

## 4\. Arquitectura de los Agentes

El sistema se compone de tres agentes especializados, cada uno con un modelo de lenguaje recomendado para su tarea específica (En la documentación se dispone de un análisis detallado):

  * **`analista_sentimiento`**:
      * **Objetivo**: Analizar el estado emocional y la urgencia del cliente.
      * **Modelo recomendado**: **`Qwen3`**, por su capacidad para el análisis profundo de matices en el lenguaje.
  * **`clasificador_incidencias`**:
      * **Objetivo**: Etiquetar la incidencia en una categoría técnica (Redes, Hardware, etc.).
      * **Modelo recomendado**: **`deepseek-coder`**, por su gran conocimiento de vocabulario técnico.
  * **`buscador_soluciones`**:
      * **Objetivo**: Buscar soluciones y generar un informe detallado.
      * **Modelo recomendado**: **`deepseek-r1`**, por su avanzada capacidad de razonamiento para conectar el problema con las herramientas disponibles.


🧠 Documento realizado por un humano y potenciado por IA
