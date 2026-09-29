from backend.app.agents.supervisor import supervisor_node
from backend.app.agents.state import AgentState


def test_supervisor_classification():
    state: AgentState = {
        "user_query": "Which region generated highest revenue in Q2 according to pricing policy?",
        "execution_trace": [],
        "total_tokens": 0,
        "latency_ms": 0.0
    }
    result_state = supervisor_node(state)
    assert result_state["intent"] in ["HYBRID_ANALYSIS", "DATA_ANALYSIS", "DOCUMENT_QA"]
    assert len(result_state["execution_trace"]) > 0
    assert result_state["execution_trace"][0].agent_name == "Supervisor Agent"
