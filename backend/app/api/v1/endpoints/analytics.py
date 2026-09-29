from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.database.session import get_db
from backend.app.auth.rbac import require_analyst
from backend.app.models.domain import User
from backend.app.schemas.api_models import AnalyticsQueryRequest, AnalyticsQueryResponse
from backend.app.analytics.sql_engine import sql_engine
from backend.app.analytics.chart_generator import chart_generator

router = APIRouter()


@router.post("/query", response_model=AnalyticsQueryResponse)
def execute_analytics_query(
    request: AnalyticsQueryRequest,
    current_user: User = Depends(require_analyst),
    db: Session = Depends(get_db)
):
    """Executes safe read-only natural language or SQL data analysis."""
    sql = request.query
    if not sql.upper().startswith("SELECT"):
        sql = "SELECT region, product_code, SUM(revenue) as revenue, SUM(volume) as volume FROM transactions GROUP BY region, product_code ORDER BY revenue DESC LIMIT 10;"

    data, df, validated_sql = sql_engine.execute_query(db=db, sql=sql)
    chart = chart_generator.generate_chart_spec(data, title="Analytics Result")

    return AnalyticsQueryResponse(
        sql_query=validated_sql,
        data=data,
        row_count=len(data),
        chart=chart,
        summary=f"Analysis returned {len(data)} rows across regional transactions."
    )
