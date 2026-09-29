from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from backend.app.auth.rbac import require_viewer
from backend.app.models.domain import User

router = APIRouter()


@router.get("", response_model=List[Dict[str, Any]])
def list_active_agents(current_user: User = Depends(require_viewer)):
    """Lists registered autonomous agents and their capabilities."""
    return [
        {
            "id": "agent-supervisor",
            "name": "Supervisor Orchestrator Agent",
            "role": "Intent Classification & Dynamic Graph Routing",
            "status": "ACTIVE",
            "tools": ["intent_classifier", "graph_router"]
        },
        {
            "id": "agent-rag",
            "name": "RAG Research Agent",
            "role": "Semantic Vector Search & Document Citation",
            "status": "ACTIVE",
            "tools": ["vector_search", "semantic_retriever", "document_parser"]
        },
        {
            "id": "agent-analyst",
            "name": "Data Analyst Agent",
            "role": "Read-Only NL-to-SQL & Pandas Data Analytics",
            "status": "ACTIVE",
            "tools": ["sql_generator", "read_only_sql_executor", "chart_generator"]
        },
        {
            "id": "agent-pricing",
            "name": "Pricing Intelligence Agent",
            "role": "Margin Optimization & Policy Anomaly Detection",
            "status": "ACTIVE",
            "tools": ["pricing_rule_validator", "anomaly_detector"]
        },
        {
            "id": "agent-recommendation",
            "name": "Recommendation Agent",
            "role": "Actionable Business Insights & Confidence Estimation",
            "status": "ACTIVE",
            "tools": ["impact_estimator", "recommendation_engine"]
        },
        {
            "id": "agent-report",
            "name": "Report Generation Agent",
            "role": "Executive Report Synthesis",
            "status": "ACTIVE",
            "tools": ["report_formatter"]
        },
        {
            "id": "agent-responsible-ai",
            "name": "Responsible AI Guardrail Agent",
            "role": "Hallucination Detection, Citation Audit & PII Filter",
            "status": "ACTIVE",
            "tools": ["hallucination_detector", "citation_verifier", "pii_scanner"]
        }
    ]
