from fastapi import APIRouter
from backend.app.api.v1.endpoints import (
    auth, chat, documents, analytics, evaluations, traces, observability, agents, audit
)

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(chat.router, prefix="/chat", tags=["Agentic Chat"])
api_router.include_router(documents.router, prefix="/documents", tags=["Documents & RAG"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Data Analytics & SQL"])
api_router.include_router(evaluations.router, prefix="/evaluations", tags=["LLM Evaluation"])
api_router.include_router(traces.router, prefix="/traces", tags=["Agent Traces"])
api_router.include_router(observability.router, prefix="/observability", tags=["AI Observability"])
api_router.include_router(agents.router, prefix="/agents", tags=["Agents Registry"])
api_router.include_router(audit.router, prefix="/audit-logs", tags=["Audit Logs"])
