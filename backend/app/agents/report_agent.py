import time
from backend.app.agents.state import AgentState
from backend.app.schemas.api_models import AgentTraceStep


def report_agent_node(state: AgentState) -> AgentState:
    start_time = time.time()
    user_query = state.get("user_query", "")
    findings = state.get("key_findings", [])
    recs = state.get("recommendations", [])
    citations = state.get("citations", [])
    confidence = state.get("confidence", "HIGH")

    answer_parts = [
        f"### Executive Summary\nBased on FinAI Nexus multi-agent intelligence analysis for query: *\"{user_query}\"*.",
        "\n### Key Findings"
    ]
    for f in findings:
        answer_parts.append(f"- {f}")

    answer_parts.append("\n### Strategic Recommendations")
    for r in recs:
        answer_parts.append(f"- {r}")

    answer_parts.append(f"\n**AI Confidence**: `{confidence}`")

    if citations:
        answer_parts.append("\n### Verified Document Sources")
        for c in citations:
            answer_parts.append(f"- **{c.filename}** (Page {c.page_number}): \"{c.snippet[:120]}...\"")

    final_ans = "\n".join(answer_parts)
    duration = (time.time() - start_time) * 1000

    trace_step = AgentTraceStep(
        agent_name="Report Generation Agent",
        node_name="report_agent_node",
        status="SUCCESS",
        duration_ms=round(duration, 2),
        summary="Compiled structured executive intelligence report.",
        tools_used=["report_formatter"],
        tokens_used=100
    )

    trace = state.get("execution_trace", [])
    trace.append(trace_step)

    state["final_answer"] = final_ans
    state["execution_trace"] = trace
    state["total_tokens"] = state.get("total_tokens", 0) + 100
    state["latency_ms"] = state.get("latency_ms", 0.0) + duration

    return state
