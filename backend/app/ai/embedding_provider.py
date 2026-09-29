import math
import hashlib
from typing import List
from abc import ABC, abstractmethod
from backend.app.core.config import settings


class BaseEmbeddingProvider(ABC):
    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        pass

    @abstractmethod
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        pass


class MockEmbeddingProvider(BaseEmbeddingProvider):
    """Deterministic hash-based pseudo-embedding provider for offline/demo operation."""

    def __init__(self, dimension: int = 128):
        self.dimension = dimension

    def embed_text(self, text: str) -> List[float]:
        text_norm = text.lower().strip()
        vec = []
        for i in range(self.dimension):
            h = hashlib.sha256(f"{text_norm}_{i}".encode("utf-8")).hexdigest()
            val = (int(h[:8], 16) / 0xFFFFFFFF) * 2.0 - 1.0
            vec.append(val)
        # Normalize vector
        norm = math.sqrt(sum(x * x for x in vec))
        return [x / norm for x in vec]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self.embed_text(t) for t in texts]


class OpenAIEmbeddingProvider(BaseEmbeddingProvider):
    def __init__(self, api_key: str, model: str = "text-embedding-3-small"):
        from langchain_openai import OpenAIEmbeddings
        self.client = OpenAIEmbeddings(openai_api_key=api_key, model=model)

    def embed_text(self, text: str) -> List[float]:
        return self.client.embed_query(text)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.client.embed_documents(texts)


def get_embedding_provider() -> BaseEmbeddingProvider:
    provider_type = settings.EMBEDDING_PROVIDER.lower()
    if provider_type == "openai" and settings.OPENAI_API_KEY:
        return OpenAIEmbeddingProvider(settings.OPENAI_API_KEY, settings.EMBEDDING_MODEL)
    return MockEmbeddingProvider()
