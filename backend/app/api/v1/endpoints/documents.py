from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from backend.app.database.session import get_db
from backend.app.auth.rbac import require_analyst, require_viewer
from backend.app.models.domain import User
from backend.app.schemas.api_models import DocumentOut, DocumentSearchRequest, DocumentSearchResponse
from backend.app.services.document_service import document_service
from backend.app.rag.vector_store import vector_store

router = APIRouter()


@router.post("/upload", response_model=DocumentOut)
def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(require_analyst),
    db: Session = Depends(get_db)
):
    """Uploads and indexes pricing & interchange policy documents."""
    return document_service.upload_document(db=db, user_id=current_user.id, file=file)


@router.get("", response_model=List[DocumentOut])
def list_documents(
    current_user: User = Depends(require_viewer),
    db: Session = Depends(get_db)
):
    """Lists all indexed platform documents."""
    return document_service.list_documents(db=db)


@router.delete("/{document_id}")
def delete_document(
    document_id: str,
    current_user: User = Depends(require_analyst),
    db: Session = Depends(get_db)
):
    """Deletes document and associated vector index."""
    success = document_service.delete_document(db=db, doc_id=document_id)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"message": "Document deleted successfully"}


@router.post("/search", response_model=DocumentSearchResponse)
def search_documents(
    request: DocumentSearchRequest,
    current_user: User = Depends(require_viewer),
    db: Session = Depends(get_db)
):
    """Performs semantic vector search across document index."""
    results = vector_store.search(db=db, query=request.query, top_k=request.top_k)
    return DocumentSearchResponse(chunks=results)
