import sys
import os
import json
from pathlib import Path
from typing import Any, Dict



# Asegurar que se pueda importar "crew" aunque el CWD no sea CrewAi/
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from crew import SoporteIncidenciasCrew


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
    get_first = lambda *keys: next((ticket_data.get(k) for k in keys if k in ticket_data and ticket_data.get(k) is not None), "")  # noqa: E731
    numero = get_first('numero', 'id', 'ticket_id', 'tickets_id')
    titulo = get_first('titulo', 'title', 'name', 'subject')
    contenido = get_first('contenido', 'content', 'description', 'body')
    return {
        'numero': numero,
        'titulo': titulo,
        'contenido': contenido,
    }


def run():
    # Crear carpeta de logs/salidas en el mismo directorio que este script
    os.chdir(SCRIPT_DIR)

    ticket_raw = _load_json()
    ticket = _normalize_ticket_fields(ticket_raw)

    try:
        with open('incidencia_guardada.json', 'w', encoding='utf-8') as f:
            json.dump(ticket_raw, f, ensure_ascii=False, indent=4)
    except Exception as exc:  # noqa: BLE001
        print(f"Aviso: No se pudo guardar 'incidencia_guardada.json': {exc}")

    numero_str = f"#{ticket['numero']} - " if str(ticket.get('numero', '')).strip() else ""
    incidencia_texto = (
        f"TICKET {numero_str}TÍTULO: {ticket.get('titulo', '')}\n\n"
        f"DESCRIPCIÓN:\n{ticket.get('contenido', '')}"
    )

    inputs = {
        'incidencia': incidencia_texto,
        'cat': "Redes, Hardware, Software, Cuentas de usuario, Permisos",
        'url_a_verificar': 'google.com',  # Poner URL del cliente
    }

    try:
        SoporteIncidenciasCrew().crew().kickoff(inputs=inputs)
    except Exception as exc:  # noqa: BLE001
        print(f"Error ejecutando el Crew: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    run()
