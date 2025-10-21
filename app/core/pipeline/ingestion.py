from pathlib import Path
from app.core.chunkers.factory import ChunkerFactory
from app.core.embeddings.base import OpenAIEmbeddingModel
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import FAISS
from app import settings

class IngestionPipeline:
    def __init__(self, client, strategy_name: str = "recursive"):
        self.chunker = ChunkerFactory.create(strategy_name)
        self.embedder = OpenAIEmbeddingModel(client)

    def _load_documents(self, path: Path):
        docs = []
        if path.is_dir():
            paths = []
            for ext in ("**/*.pdf", "**/*.txt", "**/*.md"):
                paths.extend(path.glob(ext))
        else:
            paths = [path]

        for p in paths:
            s = p.suffix.lower()
            if s == ".pdf":
                docs.extend(PyPDFLoader(str(p)).load())
            elif s in (".txt", ".md"):
                docs.extend(TextLoader(str(p), encoding="utf-8").load())
        return docs

    def run(self, input_path: str | Path, out_dir: str | Path | None = None) -> dict:
        src = Path(input_path)
        dst = Path(out_dir or settings.VECTOR_DIR)
        docs = self._load_documents(src)
        if not docs:
            return {"status": "no_docs", "docs": 0, "chunks": 0}

        # chunk to plain texts + metadatas
        texts: list[str] = []
        metadatas: list[dict] = []
        for d in docs:
            for chunk in self.chunker.split(d.page_content):
                texts.append(chunk)
                metadatas.append(d.metadata)  # keep original metadata

        # Build vector store from texts (no Document class needed)
        vs = FAISS.from_texts(
            texts=texts,
            embedding=self.embedder.to_langchain(),
            metadatas=metadatas,
        )
        dst.mkdir(parents=True, exist_ok=True)
        vs.save_local(str(dst))
        return {"status": "ok", "docs": len(docs), "chunks": len(texts), "store": str(dst)}
