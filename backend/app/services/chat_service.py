import uuid
import time
from sqlalchemy.orm import Session
from backend.app.agents.graph import finai_agent_graph
from backend.app.agents.state import AgentState
from backend.app.schemas.api_models import ChatRequest, ChatResponse
from backend.app.models.domain import AgentRun, AgentMessage, ToolCall, LLMRequest


class ChatService:
    def process_query(self, db: Session, user_id: str, request: ChatRequest) -> ChatResponse:
        run_id = str(uuid.uuid4())
        start_time = time.time()

        initial_state: AgentState = {
            "user_query": request.query,
            "user_id": user_id,
            "db_session": db,
            "execution_trace": [],
            "evidence": [],
            "citations": [],
            "safety_flags": [],
            "total_tokens": 0,
            "latency_ms": 0.0
        }

        # Execute LangGraph Multi-Agent Workflow
        final_state = finai_agent_graph.invoke(initial_state)

        total_latency = round((time.time() - start_time) * 1000, 2)

        # Record AgentRun in database
        run_record = AgentRun(
            id=run_id,
            user_id=user_id,
            query=request.query,
            intent=final_state.get("intent", "HYBRID_ANALYSIS"),
            status="COMPLETED",
            execution_time_ms=total_latency,
            total_tokens=final_state.get("total_tokens", 0),
            estimated_cost=round(final_state.get("total_tokens", 0) * 0.00001, 6),
            final_answer_json={"text": final_state.get("final_answer", "")},
            confidence=final_state.get("confidence", "HIGH")
        )
        db.add(run_record)

        # Log trace steps as AgentMessages
        for step_idx, step in enumerate(final_state.get("execution_trace", [])):
            msg = AgentMessage(
                id=str(uuid.uuid4()),
                agent_run_id=run_id,
                agent_name=step.agent_name,
                node_name=step.node_name,
                input_state={"query": request.query},
                output_state={"summary": step.summary},
                step_order=step_idx + 1,
                duration_ms=step.duration_ms
            )
            db.add(msg)

        db.commit()

        return ChatResponse(
            run_id=run_id,
            query=request.query,
            intent=final_state.get("intent", "HYBRID_ANALYSIS"),
            answer=final_state.get("final_answer", ""),
            key_findings=final_state.get("key_findings", []),
            evidence=final_state.get("evidence", []),
            recommendations=final_state.get("recommendations", []),
            confidence=final_state.get("confidence", "HIGH"),
            limitations=["Analysis based on current indexed pricing documents and transaction dataset."],
            citations=final_state.get("citations", []),
            charts=[final_state["chart_data"]] if final_state.get("chart_data") else [],
            sql_executed=final_state.get("sql_query"),
            execution_trace=final_state.get("execution_trace", []),
            safety_flags=final_state.get("safety_flags", []),
            total_tokens=final_state.get("total_tokens", 0),
            total_latency_ms=total_latency
        )


chat_service = ChatService()
