# Orchestrates: load vector store -> retrieve -> LLM generate
from app.core.embeddings.base import OpenAIEmbeddingModel
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from app import settings

class QAPipeline:
    def __init__(self, client, k: int = 3, model: str | None = None):
        self.embedder = OpenAIEmbeddingModel(client)
        self.k = k
        self.model = model or settings.LLM_MODEL

    def run(self, query: str, vector_dir: str | None = None) -> dict:
        vs = FAISS.load_local(vector_dir or settings.VECTOR_DIR,
                              self.embedder.to_langchain(),
                              allow_dangerous_deserialization=True)
        retriever = vs.as_retriever(search_kwargs={"k": self.k})
        llm = ChatOpenAI(model=self.model, temperature=0, api_key=settings.OPENAI_API_KEY)
        chain = RetrievalQA.from_chain_type(llm, retriever=retriever, return_source_documents=True)
        result = chain.invoke({"query": query})
        srcs = [{"source": d.metadata.get("source"), "start_index": d.metadata.get("start_index")}
                for d in result.get("source_documents", [])]
        return {"answer": result["result"], "sources": srcs}
