from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database.session import get_db
from backend.app.auth.rbac import require_viewer
from backend.app.models.domain import User, AgentRun, AgentMessage

router = APIRouter()


@router.get("/{run_id}")
def get_agent_trace(
    run_id: str,
    current_user: User = Depends(require_viewer),
    db: Session = Depends(get_db)
):
    """Retrieves full execution trace and node latencies for an agent run."""
    run = db.query(AgentRun).filter(AgentRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Agent run not found")

    messages = db.query(AgentMessage).filter(AgentMessage.agent_run_id == run_id).order_by(AgentMessage.step_order).all()

    return {
        "run_id": run.id,
        "query": run.query,
        "intent": run.intent,
        "status": run.status,
        "execution_time_ms": run.execution_time_ms,
        "total_tokens": run.total_tokens,
        "confidence": run.confidence,
        "steps": [
            {
                "step_order": m.step_order,
                "agent_name": m.agent_name,
                "node_name": m.node_name,
                "duration_ms": m.duration_ms,
                "summary": m.output_state.get("summary", "")
            }
            for m in messages
        ]
    }
