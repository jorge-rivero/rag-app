# app/rag_utils.py
from pathlib import Path
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from app import settings

def load_documents(input_path: Path) -> List:
    docs = []
    paths: List[Path] = []
    if input_path.is_dir():
        for ext in ("**/*.pdf", "**/*.txt", "**/*.md"):
            paths.extend(input_path.glob(ext))
    else:
        paths = [input_path]

    for p in paths:
        if p.suffix.lower() == ".pdf":
            docs.extend(PyPDFLoader(str(p)).load())
        elif p.suffix.lower() in (".txt", ".md"):
            docs.extend(TextLoader(str(p), encoding="utf-8").load())
    return docs

def chunk_documents(docs, chunk_size=settings.CHUNK_SIZE, chunk_overlap=settings.CHUNK_OVERLAP):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""],
        add_start_index=True,
    )
    return splitter.split_documents(docs)

def build_embeddings():
    return OpenAIEmbeddings(
        model=settings.EMBED_MODEL,
        api_key=settings.OPENAI_API_KEY,
    )

def build_or_overwrite_faiss(chunks):
    embed = build_embeddings()
    vs = FAISS.from_documents(chunks, embed)
    Path(settings.VECTOR_DIR).mkdir(parents=True, exist_ok=True)
    vs.save_local(settings.VECTOR_DIR)
    return True

def load_faiss():
    embed = build_embeddings()
    return FAISS.load_local(settings.VECTOR_DIR, embed, allow_dangerous_deserialization=True)
