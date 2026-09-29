import uuid
from typing import List, Dict, Any


class DocumentChunker:
    """Splits document page content into semantic overlapping chunks."""

    def __init__(self, chunk_size: int = 600, overlap: int = 100):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_document(self, document_id: str, pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        chunks = []
        chunk_index = 0

        for page in pages:
            page_num = page["page_number"]
            content = page["content"]
            if not content:
                continue

            # Split by paragraphs or fixed length with overlap
            words = content.split()
            if len(words) <= self.chunk_size // 5:
                # Small page fits into single chunk
                chunks.append({
                    "id": str(uuid.uuid4()),
                    "document_id": document_id,
                    "page_number": page_num,
                    "chunk_index": chunk_index,
                    "content": content,
                    "metadata": {"has_tables": page.get("has_tables", False)}
                })
                chunk_index += 1
            else:
                start = 0
                step = (self.chunk_size - self.overlap) // 5
                while start < len(words):
                    sub_words = words[start: start + (self.chunk_size // 5)]
                    chunk_text = " ".join(sub_words)
                    chunks.append({
                        "id": str(uuid.uuid4()),
                        "document_id": document_id,
                        "page_number": page_num,
                        "chunk_index": chunk_index,
                        "content": chunk_text,
                        "metadata": {"has_tables": page.get("has_tables", False)}
                    })
                    chunk_index += 1
                    start += step
        return chunks


chunker = DocumentChunker()
