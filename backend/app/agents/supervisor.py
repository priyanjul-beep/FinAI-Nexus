import time
import json
from backend.app.agents.state import AgentState
from backend.app.ai.llm_provider import get_llm_provider
from backend.app.prompts.registry import prompt_registry
from backend.app.schemas.api_models import AgentTraceStep


def supervisor_node(state: AgentState) -> AgentState:
    start_time = time.time()
    user_query = state.get("user_query", "")
    llm = get_llm_provider()

    prompt = prompt_registry.get_prompt("supervisor", user_query=user_query)
    sys_prompt = "You are the Supervisor Orchestrator Agent. Classify user intent into DOCUMENT_QA, DATA_ANALYSIS, PRICING_ANALYSIS, REVENUE_ANALYSIS, HYBRID_ANALYSIS, REPORT_GENERATION."

    llm_res = llm.generate(prompt=prompt, system_prompt=sys_prompt, json_mode=True)
    duration = (time.time() - start_time) * 1000

    intent = "HYBRID_ANALYSIS"
    plan = ["Classify intent", "RAG research", "Data analysis", "Pricing analysis", "Recommendation", "Responsible AI check"]

    try:
        data = json.loads(llm_res["text"])
        intent = data.get("intent", intent)
        plan = data.get("plan", plan)
    except Exception:
        # Fallback routing based on keywords
        q_lower = user_query.lower()
        if "sql" in q_lower or "revenue" in q_lower or "highest" in q_lower or "growth" in q_lower:
            intent = "HYBRID_ANALYSIS" if "policy" in q_lower or "rule" in q_lower else "DATA_ANALYSIS"
        elif "policy" in q_lower or "document" in q_lower or "guide" in q_lower:
            intent = "DOCUMENT_QA"

    trace_step = AgentTraceStep(
        agent_name="Supervisor Agent",
        node_name="supervisor_node",
        status="SUCCESS",
        duration_ms=round(duration, 2),
        summary=f"Classified query intent as '{intent}' with {len(plan)}-step plan.",
        tools_used=["intent_classifier"],
        tokens_used=llm_res.get("prompt_tokens", 0) + llm_res.get("completion_tokens", 0)
    )

    trace = state.get("execution_trace", [])
    trace.append(trace_step)

    state["intent"] = intent
    state["plan"] = plan
    state["execution_trace"] = trace
    state["total_tokens"] = state.get("total_tokens", 0) + trace_step.tokens_used
    state["latency_ms"] = state.get("latency_ms", 0.0) + duration

    return state
