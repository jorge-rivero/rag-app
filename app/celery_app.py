# app/celery_app.py
import celery
from app.settings import REDIS_URL

def make_celery() -> celery.Celery:
    app = celery.Celery(
        "rag",
        broker=REDIS_URL,
        backend=REDIS_URL,
        include=["app.tasks"],
    )
    # Sensible defaults
    app.conf.update(
        task_serializer="json",
        result_serializer="json",
        accept_content=["json"],
        timezone="UTC",
        task_track_started=True,
    )
    return app

celery_app = make_celery()
