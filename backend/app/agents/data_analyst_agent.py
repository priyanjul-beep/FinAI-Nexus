import time
import json
from backend.app.agents.state import AgentState
from backend.app.ai.llm_provider import get_llm_provider
from backend.app.prompts.registry import prompt_registry
from backend.app.analytics.sql_engine import sql_engine
from backend.app.analytics.chart_generator import chart_generator
from backend.app.schemas.api_models import AgentTraceStep


def data_analyst_node(state: AgentState) -> AgentState:
    start_time = time.time()
    user_query = state.get("user_query", "")
    llm = get_llm_provider()
    db = state.get("db_session")

    if not db:
        from backend.app.database.session import SessionLocal
        db = SessionLocal()
        should_close = True
    else:
        should_close = False

    prompt = prompt_registry.get_prompt("data_analyst", user_query=user_query)
    sys_prompt = "You are the Data Analyst Agent. Generate valid, read-only SQL queries to answer the user query."

    llm_res = llm.generate(prompt=prompt, system_prompt=sys_prompt, json_mode=True)

    sql_query = "SELECT region, product_code, SUM(revenue) as total_revenue, AVG(pricing_rate) as avg_rate FROM transactions GROUP BY region, product_code ORDER BY total_revenue DESC LIMIT 10;"

    try:
        data_res = json.loads(llm_res["text"])
        if "sql" in data_res:
            sql_query = data_res["sql"]
    except Exception:
        pass

    sql_results = []
    chart_spec = None
    exec_error = None

    try:
        sql_results, df, validated_sql = sql_engine.execute_query(db=db, sql=sql_query)
        sql_query = validated_sql
        chart_spec = chart_generator.generate_chart_spec(sql_results, title=f"Analysis: {user_query[:30]}")
    except Exception as e:
        exec_error = str(e)
        # Fallback safe query
        try:
            sql_results, df, validated_sql = sql_engine.execute_query(
                db=db,
                sql="SELECT region, SUM(revenue) as total_revenue FROM transactions GROUP BY region LIMIT 5;"
            )
            sql_query = validated_sql
            chart_spec = chart_generator.generate_chart_spec(sql_results, title="Regional Revenue")
        except Exception:
            pass
    finally:
        if should_close:
            db.close()

    duration = (time.time() - start_time) * 1000

    evidence_item = f"Database Query Executed: [{sql_query}] ({len(sql_results)} records returned)"

    trace_step = AgentTraceStep(
        agent_name="Data Analyst Agent",
        node_name="data_analyst_node",
        status="SUCCESS" if not exec_error else "WARNING",
        duration_ms=round(duration, 2),
        summary=f"Executed read-only SQL query returning {len(sql_results)} records.",
        tools_used=["sql_generator", "read_only_sql_executor", "chart_generator"],
        tokens_used=llm_res.get("prompt_tokens", 0) + llm_res.get("completion_tokens", 0)
    )

    trace = state.get("execution_trace", [])
    trace.append(trace_step)

    agent_outputs = state.get("agent_outputs", {})
    agent_outputs["sql_query"] = sql_query
    agent_outputs["sql_results_count"] = len(sql_results)

    state["sql_query"] = sql_query
    state["sql_results"] = sql_results
    if chart_spec:
        state["chart_data"] = chart_spec
    state["evidence"] = state.get("evidence", []) + [evidence_item]
    state["agent_outputs"] = agent_outputs
    state["execution_trace"] = trace
    state["total_tokens"] = state.get("total_tokens", 0) + trace_step.tokens_used
    state["latency_ms"] = state.get("latency_ms", 0.0) + duration

    return state
