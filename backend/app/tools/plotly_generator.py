"""Plotly Generator — creates interactive Plotly charts as JSON."""

import pandas as pd
import plotly.express as px
import plotly.io as pio
from typing import Any

from app.core.logging_config import get_logger

logger = get_logger(__name__)

def generate_interactive_chart(
    df: pd.DataFrame,
    chart_type: str,
    title: str,
    x: str | None = None,
    y: str | None = None,
    column: str | None = None,
) -> dict[str, Any]:
    """Generate a Plotly chart and return its JSON representation.

    Args:
        df: The dataset DataFrame.
        chart_type: One of 'line', 'bar', 'histogram', 'scatter', 'pie', 'box'.
        title: Chart title.
        x: X-axis column.
        y: Y-axis column.
        column: Column for histogram/pie.

    Returns:
        Plotly JSON dictionary.
    """
    logger.info(f"Generating interactive {chart_type} chart: {title}")

    try:
        if chart_type == "line":
            fig = px.line(df, x=x, y=y, title=title, template="plotly_dark")
        elif chart_type == "bar":
            fig = px.bar(df, x=x, y=y, title=title, template="plotly_dark")
        elif chart_type == "histogram":
            fig = px.histogram(df, x=column or x, title=title, template="plotly_dark")
        elif chart_type == "scatter":
            fig = px.scatter(df, x=x, y=y, title=title, template="plotly_dark")
        elif chart_type == "pie":
            fig = px.pie(df, names=column or x, title=title, template="plotly_dark")
        elif chart_type == "box":
            fig = px.box(df, y=column or y, x=x, title=title, template="plotly_dark")
        else:
            raise ValueError(f"Unsupported interactive chart type: {chart_type}")

        # Customize layout for premium look
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            margin=dict(l=40, r=40, t=60, b=40),
            title_font_size=20,
        )

        # Convert to JSON dict
        return json.loads(pio.to_json(fig))

    except Exception as e:
        logger.error(f"Failed to generate interactive chart: {e}")
        return {"error": str(e)}

import json
