import os
import uuid
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from fastapi import UploadFile
from backend.app.models.domain import Document
from backend.app.rag.parser import parser
from backend.app.rag.chunker import chunker
from backend.app.rag.vector_store import vector_store
from backend.app.core.exceptions import DocumentProcessingException


class DocumentService:
    def upload_document(self, db: Session, user_id: str, file: UploadFile) -> Document:
        upload_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "documents")
        os.makedirs(upload_dir, exist_ok=True)

        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as f:
            f.write(file.file.read())

        doc_id = str(uuid.uuid4())
        doc_obj = Document(
            id=doc_id,
            user_id=user_id,
            filename=file.filename,
            file_path=file_path,
            file_type=file.filename.split(".")[-1].lower(),
            file_size=os.path.getsize(file_path),
            status="PROCESSING",
            total_pages=0
        )
        db.add(doc_obj)
        db.commit()

        # Parse & Chunk synchronously or via worker
        try:
            pages = parser.parse_file(file_path)
            doc_obj.total_pages = len(pages)
            chunks = chunker.chunk_document(document_id=doc_id, pages=pages)
            vector_store.add_chunks(db=db, chunks=chunks)
            doc_obj.status = "INDEXED"
            db.commit()
        except Exception as e:
            doc_obj.status = "FAILED"
            db.commit()
            raise DocumentProcessingException(f"Document indexing failed: {str(e)}")

        return doc_obj

    def list_documents(self, db: Session) -> List[Document]:
        return db.query(Document).order_by(Document.created_at.desc()).all()

    def delete_document(self, db: Session, doc_id: str) -> bool:
        doc = db.query(Document).filter(Document.id == doc_id).first()
        if not doc:
            return False
        if os.path.exists(doc.file_path):
            try:
                os.remove(doc.file_path)
            except Exception:
                pass
        db.delete(doc)
        db.commit()
        return True


document_service = DocumentService()
