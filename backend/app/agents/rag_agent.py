import time
from backend.app.agents.state import AgentState
from backend.app.rag.retriever import retriever
from backend.app.schemas.api_models import AgentTraceStep


def rag_node(state: AgentState) -> AgentState:
    start_time = time.time()
    user_query = state.get("user_query", "")
    db = state.get("db_session")

    if not db:
        from backend.app.database.session import SessionLocal
        db = SessionLocal()
        should_close = True
    else:
        should_close = False

    try:
        retrieval_res = retriever.retrieve_context(
            db=db,
            query=user_query,
            top_k=5,
            similarity_threshold=0.30
        )
    finally:
        if should_close:
            db.close()

    duration = (time.time() - start_time) * 1000

    chunks = retrieval_res["retrieved_chunks"]
    citations = retrieval_res["citations"]
    context_text = retrieval_res["context_text"]

    evidence_items = [f"Doc: {c.filename} (Page {c.page_number})" for c in citations]

    trace_step = AgentTraceStep(
        agent_name="RAG Research Agent",
        node_name="rag_node",
        status="SUCCESS",
        duration_ms=round(duration, 2),
        summary=f"Retrieved {len(chunks)} relevant document chunks and generated {len(citations)} citations.",
        tools_used=["vector_search", "semantic_retriever"],
        tokens_used=150
    )

    trace = state.get("execution_trace", [])
    trace.append(trace_step)

    agent_outputs = state.get("agent_outputs", {})
    agent_outputs["rag_context"] = context_text

    state["retrieved_documents"] = chunks
    state["citations"] = citations
    state["evidence"] = state.get("evidence", []) + evidence_items
    state["agent_outputs"] = agent_outputs
    state["execution_trace"] = trace
    state["total_tokens"] = state.get("total_tokens", 0) + 150
    state["latency_ms"] = state.get("latency_ms", 0.0) + duration

    return state
