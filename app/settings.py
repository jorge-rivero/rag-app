# app/settings.py
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-3-small")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

VECTOR_DIR = os.getenv("VECTOR_DIR", "vector_store")
DOCS_DIR = os.getenv("DOCS_DIR", "docs")

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "800"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
