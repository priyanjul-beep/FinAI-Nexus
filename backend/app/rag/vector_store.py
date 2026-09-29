import math
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from backend.app.models.domain import DocumentChunk, Document
from backend.app.ai.embedding_provider import get_embedding_provider, BaseEmbeddingProvider


def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    if not v1 or not v2 or len(v1) != len(v2):
        return 0.0
    dot = sum(a * b for a, b in zip(v1, v2))
    mag1 = math.sqrt(sum(a * a for a in v1))
    mag2 = math.sqrt(sum(b * b for b in v2))
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot / (mag1 * mag2)


class VectorStore:
    def __init__(self, embedding_provider: Optional[BaseEmbeddingProvider] = None):
        self.embedder = embedding_provider or get_embedding_provider()

    def add_chunks(self, db: Session, chunks: List[Dict[str, Any]]) -> None:
        """Stores document chunks with their embeddings."""
        texts = [c["content"] for c in chunks]
        embeddings = self.embedder.embed_documents(texts)

        for chunk_data, emb in zip(chunks, embeddings):
            chunk_obj = DocumentChunk(
                id=chunk_data["id"],
                document_id=chunk_data["document_id"],
                page_number=chunk_data["page_number"],
                chunk_index=chunk_data["chunk_index"],
                content=chunk_data["content"],
                embedding_json=emb,
                metadata_json=chunk_data.get("metadata", {})
            )
            db.add(chunk_obj)
        db.commit()

    def search(
        self,
        db: Session,
        query: str,
        top_k: int = 5,
        threshold: float = 0.50,
        filter_doc_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Performs vector similarity search across indexed document chunks."""
        query_emb = self.embedder.embed_text(query)

        query_builder = db.query(DocumentChunk, Document.filename)\
            .join(Document, DocumentChunk.document_id == Document.id)

        if filter_doc_id:
            query_builder = query_builder.filter(DocumentChunk.document_id == filter_doc_id)

        results = query_builder.all()

        scored_results = []
        for chunk, filename in results:
            emb = chunk.embedding_json
            if not emb:
                # If embedding missing, compute on the fly using embedder
                emb = self.embedder.embed_text(chunk.content)

            score = cosine_similarity(query_emb, emb)
            if score >= threshold:
                scored_results.append({
                    "chunk_id": chunk.id,
                    "document_id": chunk.document_id,
                    "filename": filename,
                    "page_number": chunk.page_number,
                    "content": chunk.content,
                    "score": round(score, 4),
                    "metadata": chunk.metadata_json or {}
                })

        # Sort descending by similarity score
        scored_results.sort(key=lambda x: x["score"], reverse=True)
        return scored_results[:top_k]


vector_store = VectorStore()
