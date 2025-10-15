FROM python:3.11-slim

WORKDIR /app
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# Ensure vector store & docs exist
RUN mkdir -p /app/vector_store /app/docs

CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]
