from app.celery_app import celery_app
from openai import OpenAI
from app.core.pipeline.ingestion import IngestionPipeline
from app.core.pipeline.qa import QAPipeline
from app import settings

@celery_app.task(bind=True, name="rag.ingest")
def task_ingest(self, input_dir: str | None = None, strategy: str = "recursive"):
    client = OpenAI()
    pipe = IngestionPipeline(client, strategy_name=strategy)
    out = pipe.run(input_path=input_dir or settings.DOCS_DIR, out_dir=settings.VECTOR_DIR)
    return out

@celery_app.task(bind=True, name="rag.ask")
def task_ask(self, query: str, k: int = 3):
    client = OpenAI()
    pipe = QAPipeline(client, k=k)
    return pipe.run(query=query, vector_dir=settings.VECTOR_DIR)
