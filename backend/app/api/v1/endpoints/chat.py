from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.database.session import get_db
from backend.app.auth.rbac import get_current_user, require_viewer
from backend.app.models.domain import User
from backend.app.schemas.api_models import ChatRequest, ChatResponse
from backend.app.services.chat_service import chat_service

router = APIRouter()


@router.post("", response_model=ChatResponse)
def chat_endpoint(
    request: ChatRequest,
    current_user: User = Depends(require_viewer),
    db: Session = Depends(get_db)
):
    """Executes multi-agent LangGraph workflow for pricing and interchange intelligence."""
    return chat_service.process_query(db=db, user_id=current_user.id, request=request)
