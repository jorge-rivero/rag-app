from prometheus_fastapi_instrumentator import Instrumentator
from fastapi import FastAPI, UploadFile, File, Form, status
from fastapi.responses import JSONResponse
from pathlib import Path
from app.tasks import task_embed_docs, task_answer
from app import settings
import shutil
import uuid
from pydantic import BaseModel

app = FastAPI(title="RAG API (FastAPI + Celery + Redis)")

# Instrument all routes and expose /metrics
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.post("/ingest", status_code=status.HTTP_202_ACCEPTED)
async def ingest(input_dir: str | None = Form(default=None)):
    task = task_embed_docs.delay(input_dir)
    return {"task_id": task.id, "message": "Ingestion started."}

@app.post("/upload-and-ingest")
async def upload_and_ingest(file: UploadFile = File(...)):
    """
    Upload a single PDF/TXT/MD and trigger ingestion.
    The file is saved under docs/uploads/<uuid>.<ext>.
    """
    uploads_dir = Path(settings.DOCS_DIR) / "uploads"
    uploads_dir.mkdir(parents=True, exist_ok=True)
    ext = Path(file.filename).suffix
    saved_path = uploads_dir / f"{uuid.uuid4()}{ext}"
    with open(saved_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    task = task_embed_docs.delay(str(uploads_dir))
    return {"task_id": task.id, "saved": str(saved_path)}

class AskRequest(BaseModel):
    query: str
    k: int | None = 3

@app.post("/ask", status_code=status.HTTP_202_ACCEPTED)
def ask(request: AskRequest):
    """Queue a QA job against the current FAISS index using POST JSON body."""
    task = task_answer.delay(request.query, request.k)
    return {"task_id": task.id, "message": "Query queued."}


@app.get("/status/{task_id}")
def status(task_id: str):
    from app.celery_app import celery_app
    res = celery_app.AsyncResult(task_id)
    payload = {"task_id": task_id, "state": res.state}
    if res.state == "SUCCESS":
        payload["result"] = res.result
    elif res.state == "FAILURE":
        payload["error"] = str(res.result)
    return JSONResponse(payload)
