# Uso de agentes de IA en Python

Este documento explica cómo integrar **Ollama** con agentes IA y como llamarlos desde Pyhton, para su integración con programas. Ollama permite ejecutar modelos LLM localmente. Soporta modelos como `deepseek-r1`, `llama3`, `mistral`, etc., y puede ser controlado mediante CLI o API REST.

### Instalación

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull deepseek-r1
```
## Integrar con Pyhton
Para probar su funcionamiento y que exista una comunicación correcta, se ha hecho un breve programa que recoge una incidencia y muestra valores en un diccionario:
```pyhton
import subprocess

def consultar_ollama(prompt):
    """Ejecuta ollama run deepseek-r1 con un prompt dado y devuelve la respuesta."""
    result = subprocess.run(
        ['ollama', 'run', 'deepseek-r1', '--prompt', prompt],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

def analizar_incidencia(incidencia):
    """Pregunta a Ollama por resumen, contexto, info y ánimo del cliente y devuelve un diccionario."""
    prompts = {
        'resumen': f"Resume esta incidencia:\n{incidencia}",
        'contexto': f"Proporciona el contexto importante de esta incidencia:\n{incidencia}",
        'informacion': f"¿Qué información relevante se puede extraer de esta incidencia?:\n{incidencia}",
        'animo_cliente': f"¿Cuál es el ánimo o sentimiento del cliente en esta incidencia?:\n{incidencia}"
    }

    respuestas = {}
    for clave, prompt in prompts.items():
        respuesta = consultar_ollama(prompt)
        respuestas[clave] = respuesta
        print(f"\n{clave.capitalize()}:\n{respuesta}")

    return respuestas

if __name__ == "__main__":
    incidencia = input("Por favor, introduce la descripción de la incidencia:\n")
    resultados = analizar_incidencia(incidencia)

    print("\nDiccionario final con análisis:")
    print(resultados)

```
## Modelos de interés
El siguiente listado reune los modelos mas relevantes debido a su popularidad, solicitud de recursos o tipo de licencia (Se aclualizará a medida que se preuben otros, nuevos lanzamientos...):
- Deepseek r1 (ollama run deepseek-r1)
- Gemma3 (ollama run gemma3)
- Qwen3 (ollama run qwen3)
- Llama 3.3 (ollama run llama3.3)