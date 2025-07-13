#!/usr/bin/env python3
"""
--Agente de IA para GLPI - Prototipo Inicial--

Este es el punto de entrada principal del agente de IA que se integra con GLPI.
El agente obtiene tickets y genera resúmenes automáticos para mejorar los flujos de trabajo técnicos.

"""

from glpi_client import GLPIClient
from ai_summarizer import summarize_ticket
from config import GLPI_URL, GLPI_APP_TOKEN, GLPI_USER_TOKEN

def main():
    """
    Función principal que ejecuta el flujo completo del agente de IA.
    """
    print("Iniciando Agente de IA para GLPI - Prototipo")
    print("=" * 50)
    
    try:
        # 1. Instanciar el cliente GLPI
        print("Conectando con GLPI...")
        glpi_client = GLPIClient(
            url=GLPI_URL,
            app_token=GLPI_APP_TOKEN,
            user_token=GLPI_USER_TOKEN
        )
        
        # 2. Obtener contenido del ticket de ejemplo
        ticket_id = 123
        print(f"\nProcesando ticket #{ticket_id}...")
        ticket_content = glpi_client.get_ticket_full_content(ticket_id)
        
        # 3. Mostrar el contenido original del ticket
        print("\n" + "=" * 50)
        print("CONTENIDO ORIGINAL DEL TICKET")
        print("=" * 50)
        print(ticket_content)
        
        # 4. Generar resumen con IA
        print("\n" + "=" * 50)
        print("PROCESANDO CON INTELIGENCIA ARTIFICIAL")
        print("=" * 50)
        summary = summarize_ticket(ticket_content)
        
        # 5. Mostrar el resumen generado
        print("\n" + "=" * 50)
        print("RESUMEN GENERADO POR IA:")
        print("=" * 50)
        print(summary)
        

    except Exception as e:
        print(f"\n Error en el proceso principal: {str(e)}")
        print("Verifica que Ollama esté ejecutándose y el modelo phi3:mini esté disponible")

if __name__ == "__main__":
    main() 