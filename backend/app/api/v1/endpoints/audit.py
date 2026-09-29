from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.database.session import get_db
from backend.app.auth.rbac import require_admin
from backend.app.models.domain import User, AuditLog

router = APIRouter()


@router.get("", response_model=List[Dict[str, Any]])
def list_audit_logs(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Retrieves enterprise security audit logs."""
    logs = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(100).all()
    return [
        {
            "id": l.id,
            "user_id": l.user_id,
            "action": l.action,
            "resource": l.resource,
            "status": l.status,
            "ip_address": l.ip_address,
            "timestamp": l.timestamp
        }
        for l in logs
    ]
