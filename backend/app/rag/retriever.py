from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from backend.app.rag.vector_store import vector_store
from backend.app.schemas.api_models import Citation


class RAGRetriever:
    """Retriever service for semantic RAG lookups and citation formatting."""

    def retrieve_context(
        self,
        db: Session,
        query: str,
        top_k: int = 5,
        similarity_threshold: float = 0.50
    ) -> Dict[str, Any]:

        chunks = vector_store.search(
            db=db,
            query=query,
            top_k=top_k,
            threshold=similarity_threshold
        )

        formatted_context_blocks = []
        citations = []

        for idx, item in enumerate(chunks):
            snippet = item["content"]
            fname = item["filename"]
            page_num = item["page_number"]
            doc_id = item["document_id"]
            score = item["score"]

            block = f"[Source {idx+1}: {fname} (Page {page_num})]\n{snippet}"
            formatted_context_blocks.append(block)

            citations.append(Citation(
                document_id=doc_id,
                filename=fname,
                page_number=page_num,
                snippet=snippet[:200] + "...",
                score=score
            ))

        full_context = "\n\n".join(formatted_context_blocks)

        return {
            "query": query,
            "context_text": full_context,
            "retrieved_chunks": chunks,
            "citations": citations,
            "chunk_count": len(chunks)
        }


retriever = RAGRetriever()
