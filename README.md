# GLPI AI Agent - Prototipo Inicial

Este proyecto implementa un agente de inteligencia artificial que se integra con la plataforma de helpdesk GLPI para generar resúmenes automáticos de tickets y optimizar los flujos de trabajo técnicos.

Para más información puedes visitar el Readme de la rama principal del proyecto

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
