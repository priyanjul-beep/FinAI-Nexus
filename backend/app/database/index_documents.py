import os
import glob
import uuid
from sqlalchemy.orm import Session
from backend.app.database.session import SessionLocal
from backend.app.models.domain import User, Document
from backend.app.rag.parser import parser
from backend.app.rag.chunker import chunker
from backend.app.rag.vector_store import vector_store


def index_sample_documents():
    db: Session = SessionLocal()
    try:
        admin_user = db.query(User).filter(User.role == "ADMIN").first()
        user_id = admin_user.id if admin_user else "admin-default-id"

        doc_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "documents")
        files = glob.glob(os.path.join(doc_dir, "*.md")) + glob.glob(os.path.join(doc_dir, "*.pdf"))

        print(f"[Indexer] Found {len(files)} sample documents to index in {doc_dir}")

        for file_path in files:
            filename = os.path.basename(file_path)
            # Check if document already exists
            existing = db.query(Document).filter(Document.filename == filename).first()
            if existing:
                print(f"[Indexer] Document '{filename}' already indexed. Skipping.")
                continue

            # Parse pages
            pages = parser.parse_file(file_path)
            doc_id = str(uuid.uuid4())

            # Create document record
            doc_obj = Document(
                id=doc_id,
                user_id=user_id,
                filename=filename,
                file_path=file_path,
                file_type="markdown" if filename.endswith(".md") else "pdf",
                file_size=os.path.getsize(file_path),
                status="INDEXED",
                total_pages=len(pages),
                metadata_json={"source": "sample_seed_documents"}
            )
            db.add(doc_obj)
            db.commit()

            # Create & index chunks
            chunks = chunker.chunk_document(document_id=doc_id, pages=pages)
            vector_store.add_chunks(db=db, chunks=chunks)
            print(f"[Indexer] Successfully parsed & indexed '{filename}' ({len(chunks)} chunks)")

    except Exception as e:
        db.rollback()
        print(f"[Indexer Error] {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    index_sample_documents()
