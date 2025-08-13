from uuid import uuid4

from starlette.applications import Starlette
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse
from starlette.routing import Route


# --- Simple in-memory job store ---
jobs = {}


def run_crew(data, job_id):
    # Execute the crew process...
    # Simulate processing the data.
    jobs[job_id] = {"result": 42}
    print(f"Processed data for job {job_id}: {data}")


async def run_agent(request):
    data = await request.json()
    if not data:
        return JSONResponse({"error": "Missing data"}, status_code=400)

    job_id = str(uuid4())
    jobs[job_id] = None  # mark as pending

    # Add background task
    background = BackgroundTask(run_crew, data, job_id)

    return JSONResponse({"job_id": job_id}, background=background)


async def get_result(request):
    job_id = request.path_params["job_id"]
    if job_id not in jobs:
        return JSONResponse({"error": "Job not found"}, status_code=404)

    result = jobs[job_id]
    if result is None:
        return JSONResponse({"status": "pending"})
    return JSONResponse({"status": "done", "response": result})


routes = [
    Route("/run-agent", run_agent, methods=["POST"]),
    Route("/get-result/{job_id}", get_result, methods=["GET"]),
]

app = Starlette(debug=True, routes=routes)
