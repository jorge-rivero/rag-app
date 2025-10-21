# RAG-App — Async RAG Pipeline with FastAPI, Celery, Redis, Prometheus, and Flower

This project implements a **Retrieval-Augmented Generation (RAG)** microservice architecture designed for modularity, observability, and scalability.

It integrates:
- **FastAPI** for serving endpoints  
- **Celery + Redis** for async background processing  
- **FAISS** for vector search  
- **Prometheus + Flower** for monitoring and metrics  

---

## How to Run It

### Using Docker

```bash
docker compose up --build -d
```

To stop and remove everything (including volumes):

```bash
docker compose down -v
```

Once up, all services are available:

| Service | URL |
|----------|-----|
| **Flower UI** | [http://localhost:5555](http://localhost:5555) |
| **Prometheus** | [http://localhost:9090](http://localhost:9090) |
| **API Metrics** | [http://localhost:8000/metrics](http://localhost:8000/metrics) |
| **FastAPI Docs (Swagger UI)** | [http://localhost:8000/docs](http://localhost:8000/docs) |

Prometheus scrapes two targets:  
- `api` (FastAPI metrics endpoint)  
- `celery_exporter` (Celery task metrics)

---

## Endpoints Overview

### Ingest Documents

Uploads and embeds documents for retrieval.

**POST** `/ingest`

Example:
```bash
curl -X POST http://localhost:8000/ingest   -H "Content-Type: application/json"   -d '{"input_dir": "docs", "strategy": "recursive"}'
```

Response:
```json
{
  "task_id": "a1b2c3...",
  "message": "Ingestion started."
}
```

---

### 2️⃣ Ask Questions (Async RAG Query)

**POST** `/ask`

Example:
```bash
curl -X POST http://localhost:8000/ask   -H "Content-Type: application/json"   -d '{"query": "How do I authenticate to the API?", "k": 3}'
```

Response:
```json
{
  "task_id": "82ac463b-6ab5-4874-9f7b-612e0fcc7bb4",
  "message": "Query queued."
}
```

Then check the status:

```bash
curl http://localhost:8000/status/82ac463b-6ab5-4874-9f7b-612e0fcc7bb4
```

---

### Metrics & Observability

| Metric | Description |
|--------|-------------|
| **rag_latency_seconds** | Latency per task |
| **rag_throughput_total** | Number of tasks completed |
| **rag_errors_total** | Number of failed tasks |
| **rag_events_total** | Custom RAG events exposed from observable pipeline |

---

## Architecture

```
rag-app/
├── app/
│   ├── core/
│   │   ├── chunkers/
│   │   │   ├── factory.py
│   │   │   └── strategies.py
│   │   ├── embeddings/
│   │   │   └── base.py   
│   │   └── pipeline/
│   │       ├── facade.py
│   │       ├── ingestion.py
│   │       ├── observable.py
│   │       └── qa.py
│   ├── celery_app.py
│   ├── tasks.py   
│   ├── app.py
│   └── settings.py
├── docs/
│   └── *.txt,*.pdf,*.md
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## References

- **Flower UI:** [http://localhost:5555](http://localhost:5555)
- **Prometheus:** [http://localhost:9090](http://localhost:9090)
  - Targets: `api`, `celery_exporter`
- **API Metrics:** [http://localhost:8000/metrics](http://localhost:8000/metrics)
- **API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Next Steps

### Observability
- Define metrics:
  - Latency, throughput, error rate
  - RAG observability (groundedness, factual accuracy)
- Create **Grafana dashboard** for visual monitoring

### ML & RAG Enhancements
- Add support for multiple LLM and embedding models
- Make architecture **model-agnostic**
- Improve `/ask` endpoint to respond immediately (non-blocking)
- Introduce document and chunk ID tracking for audits

### Security & CI/CD
- Store `.env` variables securely
- Implement **GitHub Actions** for testing & deployment
- Optionally store vector embeddings in **Postgres** (FAISS → PGVector)
- Add **Pydantic validation** for request schemas

### QA & Testing
- Add pytest test suite
- Save Postman collection for API testing

---

## License
MIT License © 2025 — Jorge Rivero

---

**Author:** Jorge Rivero  
**Project:** RAG-App  
**Stack:** FastAPI • Celery • Redis • FAISS • Prometheus • Flower  
**Version:** 1.0.0  
