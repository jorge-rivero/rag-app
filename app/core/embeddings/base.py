from abc import ABC, abstractmethod
from langchain_openai import OpenAIEmbeddings
from app import settings

# Encapsulation: hides the OpenAI SDK complexity.
# Abstraction: exposes only a high-level embed() interface.

class EmbeddingModel(ABC):
    """Abstract base class for embedding models."""
    @abstractmethod
    def embed(self, text: str) -> list[float]:
        pass


class OpenAIEmbeddingModel(EmbeddingModel):
    """Encapsulates OpenAI embedding logic."""
    def __init__(self, client, model="text-embedding-3-small"):
        self._client = client
        self._model = model

    def embed(self, text: str):
        response = self._client.embeddings.create(model=self._model, input=text)
        return response.data[0].embedding

    # LangChain wrapper for VectorStore APIs
    def to_langchain(self) -> OpenAIEmbeddings:
        return OpenAIEmbeddings(model=self._model, api_key=settings.OPENAI_API_KEY)
