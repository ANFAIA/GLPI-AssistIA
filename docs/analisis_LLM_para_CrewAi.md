# Modelos Ollama para Agentes CrewAI

A continuación se presenta un análisis y recomendación de los modelos de Ollama más adecuados para cada uno de los agentes definidos en el fichero agents.yaml, considerando sus roles, objetivos y las características de los distintos modelos de lenguaje disponibles.

## 1. Agente: `analista_sentimiento`

Este agente está diseñado para analizar el estado emocional y la urgencia del cliente a partir del texto de una incidencia. Su principal fortaleza debe ser la comprensión profunda del lenguaje natural y sus matices.

* **Rol**: Analista de Sentimiento y Urgencia del Cliente.
* **Objetivo**: Identificar el estado de ánimo (frustrado, apurado, etc.) y la urgencia percibida.
* **Backstory**: Especialista en comunicación con alta inteligencia emocional que "lee entre líneas".

### **Modelo Recomendado: `Qwen3`**

El modelo es una excelente opción por su capacidad para cambiar entre un modo de "pensamiento profundo" para análisis complejos y un modo rápido para respuestas más directas. Puede realizar una evaluación rápida inicial y, si detecta ambigüedad o una alta carga emocional, usar su modo de razonamiento profundo para un análisis más detallado.

## 2. Agente: `clasificador_incidencias`

Este agente debe analizar el contenido de una incidencia y asignarle una categoría técnica precisa (Redes, Hardware, Software, etc.). La precisión y el conocimiento técnico son claves.

* **Rol**: Especialista en Clasificación de Incidencias Técnicas.
* **Objetivo**: Etiquetar correctamente una incidencia según su categoría técnica.
* **Backstory**: Ingeniero de soporte técnico metódico con una vasta base de conocimientos para diagnosticar problemas rápidamente.

### **Modelo Recomendado: `deepseek-coder`**

Este modelo está entrenado en gran parte por código, permitiendo entendimiento superior del vocabulario técnico y la lógica de los sistemas de IT. Su rendimiento en la implementación de algoritmos demuestra una capacidad para comprender problemas técnicos complejos y clasificarlos con una alta precisión.

## 3. Agente: `buscador_soluciones`

Este agente es responsable de buscar en múltiples fuentes de conocimiento (Wikis, Zabbix, historial) para encontrar y resumir soluciones a una incidencia ya clasificada.

* **Rol**: Experto en Base de Conocimiento y Soluciones.
* **Objetivo**: Generar un resumen claro y conciso de posibles soluciones y pasos a seguir.
* **Backstory**: Talento para consultar simultáneamente bases de conocimiento y sintetizar la información en una respuesta práctica.

### **Modelo Recomendado: `deepseek-r1`**

Dispone de grandes capacidades de razonamiento, a menudo comparadas con las de modelos de vanguardia. Mediante la cadena de pensamiento procesa una consulta, la descompone en pasos lógicos, busca información en diversas fuentes y, finalmente, sintetiza los hallazgos en un informe estructurado y coherente, exactamente lo que buscamos. Su capacidad razonamiento lo hace perfecto para conectar un problema las múltiples tools disponibles.