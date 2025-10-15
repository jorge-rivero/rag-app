from app.celery_app import celery_app
from app import settings
from app.rag_utils import load_documents, chunk_documents, build_or_overwrite_faiss, load_faiss
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from pathlib import Path

from prometheus_client import Counter, Histogram
import time

# Task metrics
INGEST_COUNTER = Counter("rag_ingest_jobs_total", "Total ingestion jobs")
ANSWER_COUNTER = Counter("rag_answer_jobs_total", "Total answer jobs")
ANSWER_LATENCY = Histogram("rag_answer_seconds", "Answer generation latency (s)")

@celery_app.task(name="rag.embed_docs")
def task_embed_docs(input_path: str | None = None):
    docs_path = Path(input_path) if input_path else Path(settings.DOCS_DIR)
    raw_docs = load_documents(docs_path)
    if not raw_docs:
        return {"status": "no_docs", "message": f"No documents found in {docs_path}"}
    chunks = chunk_documents(raw_docs)
    build_or_overwrite_faiss(chunks)
    return {"status": "ok", "docs": len(raw_docs), "chunks": len(chunks)}

@celery_app.task(name="rag.answer")
def task_answer(query: str, k: int = 4):
    # Load FAISS store
    vs = load_faiss()
    retriever = vs.as_retriever(search_kwargs={"k": k})
    llm = ChatOpenAI(model=settings.LLM_MODEL, temperature=0, api_key=settings.OPENAI_API_KEY)

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
    )
    result = qa.invoke({"query": query})
    sources = []
    for d in result.get("source_documents", []):
        sources.append({"source": d.metadata.get("source"), "start_index": d.metadata.get("start_index")})
    return {"answer": result["result"], "sources": sources}
