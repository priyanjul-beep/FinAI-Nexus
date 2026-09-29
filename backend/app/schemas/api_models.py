from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime


# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    email: str
    role: str
    full_name: str


class LoginRequest(BaseModel):
    email: str
    password: str


class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str
    role: str = "ANALYST"  # ADMIN, ANALYST, VIEWER


class UserOut(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Chat & Agent Schemas
class ChatRequest(BaseModel):
    query: str
    conversation_id: Optional[str] = None
    stream: bool = False


class Citation(BaseModel):
    document_id: str
    filename: str
    page_number: int
    snippet: str
    score: float = 1.0


class CodeArtifact(BaseModel):
    type: str  # sql, python, chart
    content: str
    description: Optional[str] = None


class ChartData(BaseModel):
    chart_type: str  # bar, line, pie, scatter
    title: str
    x_key: str
    y_keys: List[str]
    data: List[Dict[str, Any]]


class AgentTraceStep(BaseModel):
    agent_name: str
    node_name: str
    status: str
    duration_ms: float
    summary: str
    tools_used: List[str] = []
    tokens_used: int = 0


class ChatResponse(BaseModel):
    run_id: str
    query: str
    intent: str
    answer: str
    key_findings: List[str] = []
    evidence: List[str] = []
    recommendations: List[str] = []
    confidence: str = "HIGH"  # HIGH, MEDIUM, LOW
    limitations: List[str] = []
    citations: List[Citation] = []
    charts: List[ChartData] = []
    sql_executed: Optional[str] = None
    execution_trace: List[AgentTraceStep] = []
    safety_flags: List[str] = []
    total_tokens: int = 0
    total_latency_ms: float = 0.0


# Document Schemas
class DocumentOut(BaseModel):
    id: str
    filename: str
    file_type: str
    file_size: int
    status: str
    total_pages: int
    metadata_json: Dict[str, Any] = {}
    created_at: datetime

    class Config:
        from_attributes = True


class DocumentSearchRequest(BaseModel):
    query: str
    top_k: int = 5
    filter_type: Optional[str] = None


class DocumentSearchResponse(BaseModel):
    chunks: List[Dict[str, Any]]


# Analytics Schemas
class AnalyticsQueryRequest(BaseModel):
    query: str


class AnalyticsQueryResponse(BaseModel):
    sql_query: str
    data: List[Dict[str, Any]]
    row_count: int
    chart: Optional[ChartData] = None
    summary: str


# Evaluation Schemas
class RunEvaluationRequest(BaseModel):
    question: Optional[str] = None
    expected_answer: Optional[str] = None


class EvaluationOut(BaseModel):
    id: str
    question: str
    generated_answer: str
    faithfulness: float
    relevance: float
    citation_accuracy: float
    context_precision: float
    hallucination_risk: float
    passed: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Observability Metrics
class ObservabilityMetrics(BaseModel):
    total_requests: int
    successful_requests: int
    failed_requests: int
    avg_latency_ms: float
    p95_latency_ms: float
    total_tokens: int
    estimated_cost_usd: float
    active_agents: List[str]
    rag_retrieval_count: int
    hallucination_flags_count: int
    avg_evaluation_score: float
    agent_latency_breakdown: Dict[str, float]
