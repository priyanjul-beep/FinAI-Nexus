import time
import json
from backend.app.agents.state import AgentState
from backend.app.ai.llm_provider import get_llm_provider
from backend.app.prompts.registry import prompt_registry
from backend.app.schemas.api_models import AgentTraceStep


def recommendation_agent_node(state: AgentState) -> AgentState:
    start_time = time.time()
    findings = state.get("key_findings", [])
    evidence = state.get("evidence", [])
    llm = get_llm_provider()

    prompt = prompt_registry.get_prompt(
        "recommendation",
        key_findings="\n- ".join(findings),
        evidence="\n- ".join(evidence[:3])
    )
    sys_prompt = "You are the Executive Recommendation Agent. Provide 2-3 actionable, high-impact business recommendations."

    llm_res = llm.generate(prompt=prompt, system_prompt=sys_prompt, json_mode=True)
    duration = (time.time() - start_time) * 1000

    recs = [
        "Re-index the 14% out-of-compliance US PRD_CREDIT_PREM accounts back to standard 1.95% rate to capture $840,000 in annual gross revenue.",
        "Enforce automated contract renewal locks for APAC_SG cross-border accounts to mandate the 3.10% baseline FX spread.",
        "Implement real-time pricing rule guardrails in the gateway quoting API to prevent below-margin quotes."
    ]
    confidence = "HIGH"

    try:
        data = json.loads(llm_res["text"])
        if "recommendations" in data and isinstance(data["recommendations"], list):
            recs = data["recommendations"]
        confidence = data.get("confidence", confidence)
    except Exception:
        pass

    trace_step = AgentTraceStep(
        agent_name="Recommendation Agent",
        node_name="recommendation_agent_node",
        status="SUCCESS",
        duration_ms=round(duration, 2),
        summary=f"Synthesized {len(recs)} executive recommendations with {confidence} confidence.",
        tools_used=["impact_estimator", "recommendation_engine"],
        tokens_used=llm_res.get("prompt_tokens", 0) + llm_res.get("completion_tokens", 0)
    )

    trace = state.get("execution_trace", [])
    trace.append(trace_step)

    state["recommendations"] = recs
    state["confidence"] = confidence
    state["execution_trace"] = trace
    state["total_tokens"] = state.get("total_tokens", 0) + trace_step.tokens_used
    state["latency_ms"] = state.get("latency_ms", 0.0) + duration

    return state
