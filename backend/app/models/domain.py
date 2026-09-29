import datetime
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, Text, ForeignKey, JSON
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="ANALYST")  # ADMIN, ANALYST, VIEWER
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    documents = relationship("Document", back_populates="owner")
    agent_runs = relationship("AgentRun", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")


class Document(Base):
    __tablename__ = "documents"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    file_type = Column(String(50), nullable=False)
    file_size = Column(Integer, nullable=False)
    status = Column(String(50), default="PROCESSING")  # UPLOADED, PROCESSING, INDEXED, FAILED
    total_pages = Column(Integer, default=0)
    metadata_json = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    owner = relationship("User", back_populates="documents")
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(String(36), primary_key=True)
    document_id = Column(String(36), ForeignKey("documents.id"), nullable=False)
    page_number = Column(Integer, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    embedding_json = Column(JSON, nullable=True)  # JSON array representation for cross-db compatibility
    metadata_json = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    document = relationship("Document", back_populates="chunks")


class Product(Base):
    __tablename__ = "products"

    id = Column(String(36), primary_key=True)
    product_code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Region(Base):
    __tablename__ = "regions"

    id = Column(String(36), primary_key=True)
    region_code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    currency = Column(String(10), nullable=False)
    compliance_framework = Column(String(255))


class Customer(Base):
    __tablename__ = "customers"

    id = Column(String(36), primary_key=True)
    customer_name = Column(String(255), nullable=False)
    segment = Column(String(100), nullable=False)  # Enterprise, SMB, Mid-Market
    region = Column(String(50), nullable=False)
    tier = Column(String(50), default="Gold")
    joined_date = Column(DateTime, default=datetime.datetime.utcnow)


class PricingRule(Base):
    __tablename__ = "pricing_rules"

    id = Column(String(36), primary_key=True)
    rule_code = Column(String(50), unique=True, nullable=False)
    category = Column(String(100), nullable=False)
    region = Column(String(50), nullable=False)
    product_code = Column(String(50), nullable=False)
    min_rate = Column(Float, nullable=False)
    max_rate = Column(Float, nullable=False)
    recommended_rate = Column(Float, nullable=False)
    guidelines = Column(Text)
    status = Column(String(50), default="ACTIVE")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class InterchangeRate(Base):
    __tablename__ = "interchange_rates"

    id = Column(String(36), primary_key=True)
    region = Column(String(50), nullable=False)
    card_category = Column(String(100), nullable=False)  # Consumer Credit, Commercial, Debit
    transaction_type = Column(String(100), nullable=False)  # E-commerce, In-store, Cross-border
    tier = Column(String(50), default="Standard")
    interchange_rate_pct = Column(Float, nullable=False)
    min_fee = Column(Float, default=0.0)
    max_fee = Column(Float, default=0.0)
    effective_date = Column(DateTime, default=datetime.datetime.utcnow)


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String(36), primary_key=True)
    transaction_date = Column(DateTime, nullable=False, index=True)
    customer_id = Column(String(36), ForeignKey("customers.id"), nullable=False)
    region = Column(String(50), nullable=False, index=True)
    country = Column(String(100), nullable=False)
    product_code = Column(String(50), nullable=False, index=True)
    customer_segment = Column(String(100), nullable=False)
    volume = Column(Integer, nullable=False)
    value = Column(Float, nullable=False)
    interchange_rate = Column(Float, nullable=False)
    pricing_rate = Column(Float, nullable=False)
    revenue = Column(Float, nullable=False)
    cost = Column(Float, nullable=False)
    profit = Column(Float, nullable=False)


class AgentRun(Base):
    __tablename__ = "agent_runs"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    query = Column(Text, nullable=False)
    intent = Column(String(100), nullable=False)
    status = Column(String(50), default="RUNNING")  # RUNNING, COMPLETED, FAILED
    execution_time_ms = Column(Float, default=0.0)
    total_tokens = Column(Integer, default=0)
    estimated_cost = Column(Float, default=0.0)
    final_answer_json = Column(JSON, default=dict)
    confidence = Column(String(50), default="HIGH")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="agent_runs")
    messages = relationship("AgentMessage", back_populates="agent_run", cascade="all, delete-orphan")
    tool_calls = relationship("ToolCall", back_populates="agent_run", cascade="all, delete-orphan")
    llm_requests = relationship("LLMRequest", back_populates="agent_run", cascade="all, delete-orphan")


class AgentMessage(Base):
    __tablename__ = "agent_messages"

    id = Column(String(36), primary_key=True)
    agent_run_id = Column(String(36), ForeignKey("agent_runs.id"), nullable=False)
    agent_name = Column(String(100), nullable=False)
    node_name = Column(String(100), nullable=False)
    input_state = Column(JSON, default=dict)
    output_state = Column(JSON, default=dict)
    step_order = Column(Integer, nullable=False)
    duration_ms = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    agent_run = relationship("AgentRun", back_populates="messages")


class ToolCall(Base):
    __tablename__ = "tool_calls"

    id = Column(String(36), primary_key=True)
    agent_run_id = Column(String(36), ForeignKey("agent_runs.id"), nullable=False)
    agent_name = Column(String(100), nullable=False)
    tool_name = Column(String(100), nullable=False)
    tool_args = Column(JSON, default=dict)
    tool_result = Column(JSON, default=dict)
    duration_ms = Column(Float, default=0.0)
    status = Column(String(50), default="SUCCESS")  # SUCCESS, FAILED

    agent_run = relationship("AgentRun", back_populates="tool_calls")


class LLMRequest(Base):
    __tablename__ = "llm_requests"

    id = Column(String(36), primary_key=True)
    agent_run_id = Column(String(36), ForeignKey("agent_runs.id"), nullable=False)
    provider = Column(String(50), nullable=False)
    model = Column(String(100), nullable=False)
    prompt_version = Column(String(50), nullable=False)
    prompt_tokens = Column(Integer, default=0)
    completion_tokens = Column(Integer, default=0)
    latency_ms = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    agent_run = relationship("AgentRun", back_populates="llm_requests")


class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(String(36), primary_key=True)
    agent_run_id = Column(String(36), ForeignKey("agent_runs.id"), nullable=True)
    question = Column(Text, nullable=False)
    expected_answer = Column(Text, nullable=True)
    generated_answer = Column(Text, nullable=False)
    faithfulness = Column(Float, default=1.0)
    relevance = Column(Float, default=1.0)
    citation_accuracy = Column(Float, default=1.0)
    context_precision = Column(Float, default=1.0)
    hallucination_risk = Column(Float, default=0.0)
    passed = Column(Boolean, default=True)
    metrics_json = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    action = Column(String(100), nullable=False)
    resource = Column(String(255), nullable=False)
    status = Column(String(50), default="SUCCESS")
    ip_address = Column(String(50), default="127.0.0.1")
    metadata_json = Column(JSON, default=dict)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="audit_logs")


class PromptVersion(Base):
    __tablename__ = "prompt_versions"

    id = Column(String(36), primary_key=True)
    prompt_name = Column(String(100), nullable=False)
    version = Column(String(20), nullable=False)
    description = Column(Text)
    template = Column(Text, nullable=False)
    variables_json = Column(JSON, default=list)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
