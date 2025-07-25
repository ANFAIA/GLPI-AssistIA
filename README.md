# GLPI AI Automation

## 🎯 Descripción del Proyecto

Este proyecto busca modernizar y automatizar la plataforma open-source GLPI. La meta es integrar un sistema de agentes de IA para automatizar las respuestas del soporte técnico, optimizar los flujos de trabajo y enriquecer la experiencia de usuario, especialmente para personas sin perfil técnico.

## 🏛️ Arquitectura y Visión General
El núcleo del sistema está diseñado en torno a un flujo de trabajo que se activa con la creación de un ticket en GLPI. La información del ticket es procesada por un sistema de agentes inteligentes (`CrewAI`) que colaboran para analizar, enriquecer y proponer soluciones.

Este `CrewAI` se conecta a herramientas externas (bases de conocimiento, sistemas de monitorización) a través de un **Servidor MCP (Model Context Protocol)**, que actúa como un bus de datos.

### Flujo de Trabajo del Ticket
![Diagrama de Arquitectura V3](https://raw.githubusercontent.com/ANFAIA/GLPI-AssistIA/c81ce359886bd2f5c9111d7a7446144947432ea3/docs/BigPicture%20V3.svg)

1.  **Entrada en GLPI**: Un usuario o técnico crea un ticket de incidencia.
2.  **Activación del Agente**: La incidencia se transfiere al sistema `CrewAI` para su procesamiento.
3.  **Análisis por Agentes IA**:
      * **Analista de Emociones**: Evalúa la urgencia y el estado de ánimo del usuario para priorizar el ticket.
      * **Agente Categorizador**: Clasifica la incidencia según las etiquetas predefinidas en GLPI.
      * **Agente GLPI**: Busca en el historial de GLPI incidencias similares o relacionadas para obtener contexto.
      * **Agente Experto en \[X]**: Para cada categoría, un agente especializado consulta bases de datos externas como **Wiki.js**, **Zabbix**, etc., a través del Servidor MCP.
      * **Agente Resolutor**: Consolida toda la información, genera un resumen enriquecido y una posible solución.
4.  **Respuesta en GLPI**: La solución y el análisis generados se publican en el ticket de GLPI, asistiendo al técnico o respondiendo directamente al usuario.

## 🚀 Estado Actual del Proyecto

El proyecto se encuentra en una fase inicial de desarrollo. La arquitectura general ha sido diseñada y el enfoque actual está en la construcción de los componentes principales.

### ✅ Fase 1: Cimientos y Análisis (Completada)

  * **Entorno GLPI (Local)**: Se ha instalado y configurado una instancia de GLPI funcional utilizando Docker, con una base de datos MariaDB. Se han realizado pruebas locales de la configuración y los módulos.
  * **Entorno de Desarrollo**: Se ha establecido un entorno de desarrollo para la creación de agentes.
  * **Framework de Agentes Python**: Se ha definido el marco de trabajo básico para los agentes de IA basados en Python.
  * **Análisis de Modelos IA**: Se ha realizado una evaluación inicial de servicios de IA y LLMs de código abierto (como `deepseek-r1`, `llama3`, etc.) utilizando **Ollama** para la ejecución local.

### ⏳ Fase 2: Desarrollo de la Arquitectura (En Curso)

  * **Desarrollo del Servidor MCP**: Implementación del servidor basado en `FastAPI` que gestionará las comunicaciones entre GLPI, los agentes y las herramientas externas.
  * **Implementación de Agentes (`CrewAI`)**: Desarrollo de los agentes especializados (Analista de Emociones, Categorizador, etc.).
  * **Integración con GLPI**: Creación del plugin o *hook* en GLPI que activará el flujo de IA cuando se cree o actualice un ticket.

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

🧠 Contenido realizado por un humano y perfeccionado mediante IA
