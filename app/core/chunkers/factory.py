from app.core.chunkers.strategies import ChunkStrategy, RecursiveChunkStrategy, MarkdownChunkStrategy

# Factory Pattern: for easy extension of new chunking algorithms.
# Strategy Pattern: for polymorphic text splitting.
class ChunkerFactory:
    @staticmethod
    def create(strategy_name: str) -> ChunkStrategy:
        if strategy_name == "recursive":
            return RecursiveChunkStrategy()
        if strategy_name == "markdown":
            return MarkdownChunkStrategy()
        raise ValueError(f"Unknown strategy: {strategy_name}")