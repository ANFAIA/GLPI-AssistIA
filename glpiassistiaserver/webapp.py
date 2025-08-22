from uuid import uuid4
import json
import sys
import os
from starlette.applications import Starlette
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse
from starlette.routing import Route

jobs = {}

def _cli_payload_from(data):
    return {
        "id": data.get("id"),
        "title": data.get("title") or data.get("titulo") or "",
        "description": data.get("description") or data.get("contenido") or "",
    }

def run_crew(data, job_id):
    """Ejecuta EXACTAMENTE: python -m glpiassistiaserver "<JSON>" (mismo flujo que a mano)."""
    try:
        payload = _cli_payload_from(data)
        if payload["id"] is None:
            raise ValueError("Missing 'id' in request body")

        cli_arg = json.dumps(payload, ensure_ascii=False)

        print(f"[GLPI-WEBAPP/CLI] Job {job_id} -> python -m glpiassistiaserver '{cli_arg}'")
        import subprocess
        # Hereda el entorno del usuario (igual que a mano)
        env = os.environ.copy()
        # IMPORTANTE: sin capturar stdout/stderr para ver los logs reales del módulo
        proc = subprocess.run(
            [sys.executable, "-m", "glpiassistiaserver", cli_arg],
            env=env,
            text=True
        )

        if proc.returncode == 0:
            jobs[job_id] = {"status": "done", "message": "Incidencia procesada y publicada en GLPI."}
            print(f"[GLPI-WEBAPP/CLI] OK Job {job_id}")
        else:
            jobs[job_id] = {"status": "error", "message": f"CLI returncode {proc.returncode}"}
            print(f"[GLPI-WEBAPP/CLI] ERROR Job {job_id} -> returncode {proc.returncode}")

    except Exception as exc:
        msg = f"{exc.__class__.__name__}: {exc}"
        jobs[job_id] = {"status": "error", "message": msg}
        print(f"[GLPI-WEBAPP/CLI] EXCEPTION Job {job_id} -> {msg}")

async def run_agent(request):
    """Crea job en background y lanza el CLI."""
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

    print(f"[GLPI-WEBAPP/API] /run-agent -> job {job_id} (id={data.get('id')})")
    return JSONResponse({"job_id": job_id}, background=background)

async def get_result(request):
    job_id = request.path_params["job_id"]
    if job_id not in jobs:
        return JSONResponse({"error": "Job not found"}, status_code=404)

    result = jobs[job_id]
    if result is None:
        return JSONResponse({"status": "queued"})
    return JSONResponse(result)

routes = [
    Route("/run-agent", run_agent, methods=["POST"]),
    Route("/get-result/{job_id}", get_result, methods=["GET"]),
]
app = Starlette(debug=True, routes=routes)
