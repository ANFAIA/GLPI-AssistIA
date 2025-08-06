import requests
import json
from config import OLLAMA_HOST, OLLAMA_MODEL

def summarize_ticket(ticket_content: str) -> str:
    """
    Genera un resumen del ticket usando el modelo de IA de Ollama a través de su API REST.
    
    Args:
        ticket_content (str): Contenido completo del ticket
        
    Returns:
        str: Resumen generado por la IA
    """
    try:
        # URL de la API de Ollama
        api_url = f"{OLLAMA_HOST}/api/chat"
        
        # Prompt del sistema para instruir a la IA
        system_prompt = """Eres un experto en soporte técnico con amplia experiencia en resolución de problemas de IT. 
Tu tarea es crear un resumen conciso y profesional de un ticket de soporte técnico para que otro técnico pueda entender rápidamente:

1. El problema principal reportado
2. Las acciones técnicas realizadas hasta el momento
3. El estado actual del ticket
4. Información técnica relevante

El resumen debe ser claro, estructurado y útil para la toma de decisiones técnicas. 
Usa un lenguaje técnico apropiado pero comprensible.""" #Prompt generado mediante una IA generativa y revisado por un humano
        # Preparación para la API de Ollama
        payload = {
            "model": OLLAMA_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user", 
                    "content": f"Por favor, genera un resumen del siguiente ticket de soporte técnico:\n\n{ticket_content}"
                }
            ],
            "stream": False
        }

        # Realizar la llamada a la API de Ollama
        print(f"Generando resumen con modelo {OLLAMA_MODEL}...")
        
        response = requests.post(api_url, json=payload, timeout=120)
        response.raise_for_status()  # Lanzar excepción si hay error HTTP
        
        # Extraer y devolver el contenido de la respuesta
        result = response.json()

        
        if 'message' in result and 'content' in result['message']:
            summary = result['message']['content']
            print(f"Resumen extraído correctamente ({len(summary)} caracteres)")
            return summary
        else:
            print(f"Estructura de respuesta inesperada: {result}")
            # Intentar extraer el contenido de diferentes formas posibles
            if 'content' in result:
                return result['content']
            elif 'response' in result:
                return result['response']
            else:
                return f"No se pudo extraer el contenido de la respuesta. Estructura: {result}"
        
    except requests.exceptions.ConnectionError:
        error_message = "No se pudo conectar con Ollama"
        print(error_message)
        return error_message
    except requests.exceptions.Timeout:
        error_message = "Timeout - El modelo puede estar tardando en responder."
        print(error_message)
        return error_message
    except json.JSONDecodeError as e:
        error_message = f"JSON inválido: {str(e)}"
        print(error_message)
        return error_message
    except Exception as e:
        error_message = f"Error al generar resumen: {str(e)}"
        print(error_message)
        return error_message 