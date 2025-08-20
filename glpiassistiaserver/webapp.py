from uuid import uuid4
import json
import sys
from typing import Any, Dict

from starlette.applications import Starlette
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse
from starlette.routing import Route

from glpiassistiaserver.crew import build_crew
from glpiassistiaserver.__main__ import _normalize_ticket_fields

jobs = {}

def run_crew(data, job_id):
    """
    Ejecuta el proceso completo de los agentes para la incidencia recibida.
    Esta función se ejecuta en segundo plano.
    """
    try:
        ticket = _normalize_ticket_fields(data)

        numero_str = f"#{ticket['numero']} - " if str(ticket.get("numero", "")).strip() else ""
        incidencia_texto = (
            f"TICKET {numero_str}TÍTULO: {ticket.get('titulo', '')}\n\n"
            f"DESCRIPCIÓN:\n{ticket.get('contenido', '')}"
        )
        
        try:
            ticket_id = int(ticket.get("numero"))
        except (ValueError, TypeError):
            ticket_id = ticket.get("numero")
        
        inputs = {
            "incidencia": incidencia_texto,
            "cat": "Redes, Hardware, Software, Cuentas de usuario, Permisos",
            "url_a_verificar": "google.com",
            "id": ticket_id
        }

        print(f"Iniciando el proceso de la tripulación para el Job ID: {job_id}")
        crew = build_crew()
        crew.crew().kickoff(inputs=inputs)

        jobs[job_id] = {"status": "done", "message": "Incidencia procesada y publicada en GLPI."}
        print(f"Proceso finalizado. El informe ha sido publicado en GLPI para el Job ID: {job_id}")

    except Exception as exc:
        error_message = f"Error ejecutando el Crew: {exc.__class__.__name__}: {exc}"
        jobs[job_id] = {"status": "error", "message": error_message}
        print(f"Error en el proceso para el Job ID {job_id}: {error_message}")


async def run_agent(request):
    """
    Endpoint para iniciar el procesamiento de una nueva incidencia.
    """
    try:
        data = await request.json()
    except json.JSONDecodeError:
        return JSONResponse({"error": "Invalid JSON format"}, status_code=400)
    
    if not data:
        return JSONResponse({"error": "Missing data"}, status_code=400)
    
    if "id" not in data:
        return JSONResponse({"error": "Missing 'id' field in data"}, status_code=400)

    job_id = str(uuid4())
    jobs[job_id] = None 
    background = BackgroundTask(run_crew, data, job_id)

    return JSONResponse({"job_id": job_id}, background=background)


async def get_result(request):
    """
    Endpoint para consultar el estado de una tarea.
    """
    job_id = request.path_params["job_id"]
    if job_id not in jobs:
        return JSONResponse({"error": "Job not found"}, status_code=404)

    result = jobs[job_id]
    if result is None:
        return JSONResponse({"status": "pending"})
    
    return JSONResponse(result)


routes = [
    Route("/run-agent", run_agent, methods=["POST"]),
    Route("/get-result/{job_id}", get_result, methods=["GET"]),
]

app = Starlette(debug=True, routes=routes)