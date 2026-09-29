from typing import List, Dict, Any, Optional
from backend.app.schemas.api_models import ChartData


class ChartGenerator:
    """Generates structured chart specs for Recharts based on query dataset."""

    @staticmethod
    def generate_chart_spec(data: List[Dict[str, Any]], title: str = "Data Insights") -> Optional[ChartData]:
        if not data:
            return None

        sample = data[0]
        keys = list(sample.keys())

        x_key = None
        y_keys = []

        # Find string/categorical column for X axis
        for k in keys:
            if isinstance(sample[k], (str, type(None))):
                x_key = k
                break
        if not x_key and len(keys) > 0:
            x_key = keys[0]

        # Find numeric columns for Y axis
        for k in keys:
            if k != x_key and isinstance(sample[k], (int, float)):
                y_keys.append(k)

        if not y_keys:
            return None

        # Determine chart type
        chart_type = "bar"
        if "date" in x_key.lower() or "time" in x_key.lower() or "month" in x_key.lower():
            chart_type = "line"
        elif len(data) <= 5 and len(y_keys) == 1:
            chart_type = "pie"

        return ChartData(
            chart_type=chart_type,
            title=title,
            x_key=x_key,
            y_keys=y_keys[:2],
            data=data
        )


chart_generator = ChartGenerator()
