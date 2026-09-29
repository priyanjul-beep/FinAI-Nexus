from typing import List, Dict, Any, Optional, TypedDict
from backend.app.schemas.api_models import Citation, ChartData, AgentTraceStep


class AgentState(TypedDict, total=False):
    user_query: str
    user_id: str
    intent: str
    plan: List[str]
    retrieved_documents: List[Dict[str, Any]]
    sql_query: Optional[str]
    sql_results: Optional[List[Dict[str, Any]]]
    chart_data: Optional[ChartData]
    agent_outputs: Dict[str, Any]
    key_findings: List[str]
    evidence: List[str]
    recommendations: List[str]
    citations: List[Citation]
    confidence: str
    safety_flags: List[str]
    final_answer: str
    execution_trace: List[AgentTraceStep]
    total_tokens: int
    latency_ms: float
    errors: List[str]
    db_session: Any
