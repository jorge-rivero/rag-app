from abc import ABC, abstractmethod
from langchain.text_splitter import RecursiveCharacterTextSplitter

class ChunkStrategy(ABC):
    @abstractmethod
    def split(self, text: str) -> list[str]:
        pass


class RecursiveChunkStrategy(ChunkStrategy):
    def split(self, text: str):
        splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=100)
        return splitter.split_text(text)


class MarkdownChunkStrategy(ChunkStrategy):
    def split(self, text: str):
        return text.split("##")  # simplistic markdown split
