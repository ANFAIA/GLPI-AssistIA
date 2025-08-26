import sys
import os
import json
from typing import Any, Dict

# Cargar variables de entorno desde .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from .crew import build_crew


def _load_json() -> Dict[str, Any]:
    """Carga el JSON desde argv[1] como diccionario.

    Devuelve un dict con los datos del ticket.
    Lanza SystemExit con código 1 si no puede cargar un JSON válido.
    """
    if len(sys.argv) < 2 or not sys.argv[1]:
        print("Error: No se recibió JSON como argumento.")
        sys.exit(1)

    arg = sys.argv[1]

    try:
        data = json.loads(arg)
    except json.JSONDecodeError as exc:
        print(f"Error: El argumento no es un JSON válido: {exc}")
        sys.exit(1)

    if not isinstance(data, dict):
        print("Error: El JSON debe ser un diccionario.")
        sys.exit(1)

    return data


def _normalize_ticket_fields(ticket_data: Dict[str, Any]) -> Dict[str, Any]:
    """Normaliza los campos típicos del ticket procedentes de GLPI u orígenes sintéticos.

    Acepta alias: numero|id, titulo|title|name, contenido|content|description
    """
    get_first = lambda *keys: next(
        (
            ticket_data.get(k)
            for k in keys
            if k in ticket_data and ticket_data.get(k) is not None
        ),
        "",
    )
    numero = get_first("numero", "id", "ticket_id", "tickets_id")
    titulo = get_first("titulo", "title", "name", "subject")
    contenido = get_first("contenido", "content", "description", "body")
    return {
        "numero": numero,
        "titulo": titulo,
        "contenido": contenido,
    }


def run():
    """Función principal que ejecuta el crew con tracking de métricas."""
    try:
        ticket_raw = _load_json()
        ticket = _normalize_ticket_fields(ticket_raw)

        numero_str = (
            f"#{ticket['numero']} - " if str(ticket.get("numero", "")).strip() else ""
        )
        incidencia_texto = (
            f"TICKET {numero_str}TÍTULO: {ticket.get('titulo', '')}\n\n"
            f"DESCRIPCIÓN:\n{ticket.get('contenido', '')}"
        )

        ticket_id = ticket_raw.get("id", ticket.get("numero"))
        try:
            ticket_id = int(ticket_id)
        except Exception:
            pass

        inputs = {
            "incidencia": incidencia_texto,
            "cat": "Redes, Hardware, Software, Cuentas de usuario, Permisos",
            "url_a_verificar": "google.com",
            "id": ticket_id
        }

        # Construir el crew
        crew_instance = build_crew()
        
        # Ejecutar con tracking completo
        result = crew_instance.execute_with_tracking(inputs)
        
        print(f"\n Procesamiento completado exitosamente para el ticket #{ticket_id}")
        
        return result
        
    except KeyboardInterrupt:
        print("\nProcesamiento interrumpido por el usuario")
        sys.exit(1)
    except Exception as exc:
        print(f" Error ejecutando el Crew: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    run()