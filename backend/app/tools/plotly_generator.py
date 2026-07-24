"""Plotly Generator — creates interactive Plotly charts as JSON."""

import json
from typing import Any
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.io as pio

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
    """Generate a Plotly chart and return its JSON representation."""
    logger.info(f"Generating interactive {chart_type} chart: {title} (x={x}, y={y}, col={column})")

    try:
        plot_df = df.copy()

        categorical_cols = list(plot_df.select_dtypes(include=['object', 'category']).columns)
        numeric_cols = list(plot_df.select_dtypes(include=[np.number]).columns)

        # Intelligent fuzzy column resolution (e.g. 'sum_goals' -> 'goals')
        if x and x not in plot_df.columns:
            matched = [c for c in plot_df.columns if c in str(x) or str(x) in c]
            x = matched[0] if matched else None

        if y and y not in plot_df.columns:
            matched = [c for c in plot_df.columns if c in str(y) or str(y) in c]
            y = matched[0] if matched else None

        if column and column not in plot_df.columns:
            matched = [c for c in plot_df.columns if c in str(column) or str(column) in c]
            column = matched[0] if matched else None

        # Fallback column selection if still None
        if not x:
            x = categorical_cols[0] if categorical_cols else (plot_df.columns[0] if not plot_df.empty else None)
        
        if not y:
            y = numeric_cols[0] if numeric_cols else (plot_df.columns[1] if len(plot_df.columns) > 1 else None)

        if not column:
            column = y or x

        # For bar charts, slice top 10 for high visual contrast
        if chart_type == "bar" and y and y in plot_df.columns:
            plot_df = plot_df.sort_values(by=y, ascending=False).head(10)

        if chart_type == "line":
            fig = px.line(plot_df, x=x, y=y, title=title, template="plotly_dark")
        elif chart_type == "bar":
            fig = px.bar(plot_df, x=x, y=y, title=title, template="plotly_dark", color=y if y else None)
        elif chart_type == "histogram":
            fig = px.histogram(plot_df, x=column, title=title, template="plotly_dark")
        elif chart_type == "scatter":
            fig = px.scatter(plot_df, x=x, y=y, title=title, template="plotly_dark")
        elif chart_type == "pie":
            fig = px.pie(plot_df, names=x, values=y, title=title, template="plotly_dark")
        elif chart_type == "box":
            fig = px.box(plot_df, y=y or column, x=x, title=title, template="plotly_dark")
        else:
            fig = px.bar(plot_df, x=x, y=y, title=title, template="plotly_dark")

        # Customize layout for premium dark aesthetic
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white", family="Plus Jakarta Sans, sans-serif"),
            margin=dict(l=40, r=40, t=60, b=40),
            title_font_size=18,
        )

        return json.loads(pio.to_json(fig))

    except Exception as e:
        logger.error(f"Failed to generate interactive chart: {e}")
        return {"error": str(e)}
