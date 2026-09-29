import re
from backend.app.core.exceptions import SQLValidationException

FORBIDDEN_SQL_KEYWORDS = [
    r"\bDROP\b",
    r"\bDELETE\b",
    r"\bUPDATE\b",
    r"\bINSERT\b",
    r"\bALTER\b",
    r"\bTRUNCATE\b",
    r"\bCREATE\b",
    r"\bGRANT\b",
    r"\bREVOKE\b",
    r"\bEXEC\b",
    r"\bEXECUTE\b"
]

ALLOWED_TABLES = [
    "transactions", "products", "regions", "customers",
    "pricing_rules", "interchange_rates"
]


class SQLValidator:
    """Validates natural language SQL queries for read-only security enforcement."""

    @staticmethod
    def validate_sql(sql: str) -> str:
        sql_clean = sql.strip().rstrip(";")
        sql_upper = sql_clean.upper()

        # Must start with SELECT or WITH (for CTEs)
        if not (sql_upper.startswith("SELECT") or sql_upper.startswith("WITH")):
            raise SQLValidationException("Only SELECT or read-only CTE queries are allowed.")

        # Check forbidden keywords
        for kw in FORBIDDEN_SQL_KEYWORDS:
            if re.search(kw, sql_upper):
                kw_name = kw.replace(r"\b", "")
                raise SQLValidationException(f"Forbidden SQL operation detected: {kw_name}")

        # Enforce ROW LIMIT if not present
        if "LIMIT" not in sql_upper:
            sql_clean += " LIMIT 100"

        return sql_clean


validator = SQLValidator()
