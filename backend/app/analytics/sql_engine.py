import pandas as pd
from typing import Dict, Any, List, Tuple
from sqlalchemy import text
from sqlalchemy.orm import Session
from backend.app.analytics.sql_validator import validator
from backend.app.core.exceptions import SQLValidationException


class SQLEngine:
    """Safe read-only SQL Execution Engine."""

    def execute_query(self, db: Session, sql: str) -> Tuple[List[Dict[str, Any]], pd.DataFrame, str]:
        validated_sql = validator.validate_sql(sql)

        try:
            result = db.execute(text(validated_sql))
            rows = result.mappings().all()
            data = [dict(row) for row in rows]
            df = pd.DataFrame(data) if data else pd.DataFrame()
            return data, df, validated_sql
        except Exception as e:
            raise SQLValidationException(f"SQL execution error: {str(e)}")


sql_engine = SQLEngine()
