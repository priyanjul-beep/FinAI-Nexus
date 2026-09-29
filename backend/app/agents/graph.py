from langgraph.graph import StateGraph, END
from backend.app.agents.state import AgentState
from backend.app.agents.supervisor import supervisor_node
from backend.app.agents.rag_agent import rag_node
from backend.app.agents.data_analyst_agent import data_analyst_node
from backend.app.agents.pricing_agent import pricing_agent_node
from backend.app.agents.recommendation_agent import recommendation_agent_node
from backend.app.agents.report_agent import report_agent_node
from backend.app.agents.responsible_ai_agent import responsible_ai_node


def route_after_supervisor(state: AgentState) -> str:
    intent = state.get("intent", "HYBRID_ANALYSIS")
    if intent in ["DOCUMENT_QA", "DOCUMENT_SUMMARY"]:
        return "rag_node"
    elif intent in ["DATA_ANALYSIS", "REVENUE_ANALYSIS"]:
        return "data_analyst_node"
    else:
        # HYBRID_ANALYSIS, PRICING_ANALYSIS, REPORT_GENERATION
        return "rag_node"


def route_after_rag(state: AgentState) -> str:
    intent = state.get("intent", "HYBRID_ANALYSIS")
    if intent in ["DOCUMENT_QA", "DOCUMENT_SUMMARY"]:
        return "pricing_agent_node"
    else:
        return "data_analyst_node"


def build_finai_graph():
    builder = StateGraph(AgentState)

    # Add Nodes
    builder.add_node("supervisor_node", supervisor_node)
    builder.add_node("rag_node", rag_node)
    builder.add_node("data_analyst_node", data_analyst_node)
    builder.add_node("pricing_agent_node", pricing_agent_node)
    builder.add_node("recommendation_agent_node", recommendation_agent_node)
    builder.add_node("report_agent_node", report_agent_node)
    builder.add_node("responsible_ai_node", responsible_ai_node)

    # Set Entry Point
    builder.set_entry_point("supervisor_node")

    # Add Conditional Edges
    builder.add_conditional_edges(
        "supervisor_node",
        route_after_supervisor,
        {
            "rag_node": "rag_node",
            "data_analyst_node": "data_analyst_node"
        }
    )

    builder.add_conditional_edges(
        "rag_node",
        route_after_rag,
        {
            "pricing_agent_node": "pricing_agent_node",
            "data_analyst_node": "data_analyst_node"
        }
    )

    builder.add_edge("data_analyst_node", "pricing_agent_node")
    builder.add_edge("pricing_agent_node", "recommendation_agent_node")
    builder.add_edge("recommendation_agent_node", "report_agent_node")
    builder.add_edge("report_agent_node", "responsible_ai_node")
    builder.add_edge("responsible_ai_node", END)

    return builder.compile()


finai_agent_graph = build_finai_graph()
