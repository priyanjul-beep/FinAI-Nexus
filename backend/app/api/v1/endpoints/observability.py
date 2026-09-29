from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.database.session import get_db
from backend.app.auth.rbac import require_viewer
from backend.app.models.domain import User
from backend.app.schemas.api_models import ObservabilityMetrics
from backend.app.observability.metrics import metrics_service

router = APIRouter()


@router.get("/metrics", response_model=ObservabilityMetrics)
def get_observability_metrics(
    current_user: User = Depends(require_viewer),
    db: Session = Depends(get_db)
):
    """Retrieves platform-wide AI observability, latency, cost, and token usage metrics."""
    return metrics_service.get_dashboard_metrics(db=db)
