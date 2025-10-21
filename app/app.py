from fastapi import FastAPI, Form, UploadFile, File, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pathlib import Path
import shutil
from app.tasks import task_ingest, task_ask
from app import settings
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Async RAG Service")
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

@app.get("/healthz")
def healthz(): return {"ok": True}

class IngestBody(BaseModel):
    input_dir: str | None = None
    strategy: str | None = "recursive"

@app.post("/ingest", status_code=status.HTTP_202_ACCEPTED)
async def ingest(body: IngestBody):
    task = task_ingest.delay(body.input_dir, body.strategy or "recursive")
    return {"task_id": task.id, "message": "Ingestion started."}

class AskBody(BaseModel):
    query: str
    k: int | None = 3

@app.post("/ask", status_code=status.HTTP_202_ACCEPTED)
async def ask(body: AskBody):
    task = task_ask.delay(body.query, body.k or 3)
    return {"task_id": task.id, "message": "Query queued."}

@app.get("/status/{task_id}")
def status_route(task_id: str):
    from app.celery_app import celery_app as c
    r = c.AsyncResult(task_id)
    payload = {"task_id": task_id, "state": r.state}
    if r.state == "SUCCESS": payload["result"] = r.result
    elif r.state == "FAILURE": payload["error"] = str(r.result)
    elif r.info: payload["result"] = r.info  # for STARTED meta
    return JSONResponse(payload)

@app.post("/upload-and-ingest", status_code=status.HTTP_202_ACCEPTED)
async def upload_and_ingest(file: UploadFile = File(...), strategy: str = Form("recursive")):
    uploads = Path(settings.DOCS_DIR) / "uploads"
    uploads.mkdir(parents=True, exist_ok=True)
    dest = uploads / file.filename
    # async file copy
    contents = await file.read()
    dest.write_bytes(contents)
    task = task_ingest.delay(str(uploads), strategy)
    return {"task_id": task.id, "saved": str(dest)}

