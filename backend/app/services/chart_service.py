"""Chart service — orchestrates chart generation from analysis requests."""

import re

import pandas as pd

from app.core.logging_config import get_logger
from app.tools.chart_generator import (
    generate_line_chart,
    generate_bar_chart,
    generate_histogram,
    generate_scatter_plot,
    generate_correlation_heatmap,
    generate_box_plot,
)
from app.tools.plotly_generator import generate_interactive_chart

logger = get_logger(__name__)


def _sanitize_chart_name(name: str) -> str:
    """Convert a title into a safe filename."""
    name = name.lower().strip()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    safe_name = str(name.strip("_"))
    return safe_name[0:60]


def create_chart(
    df: pd.DataFrame,
    chart_type: str,
    file_id: str,
    title: str,
    x: str | None = None,
    y: str | None = None,
    column: str | None = None,
) -> dict:
    """Create a chart based on the specified type and parameters.

    Args:
        df: The dataset DataFrame.
        chart_type: One of 'line', 'bar', 'histogram', 'scatter', 'heatmap'.
        file_id: ID of the uploaded file (for chart storage path).
        title: Chart title.
        x: X-axis column name (for line, bar, scatter).
        y: Y-axis column name (for line, bar, scatter).
        column: Column name (for histogram).

    Returns:
        Dictionary with chart title, URL, and type.
    """
    chart_name = _sanitize_chart_name(title)
    logger.info(f"Creating {chart_type} chart: {title}")

    try:
        if chart_type == "line":
            url = generate_line_chart(df, x, y, title, file_id, chart_name)
        elif chart_type == "bar":
            url = generate_bar_chart(df, x, y, title, file_id, chart_name)
        elif chart_type == "histogram":
            url = generate_histogram(df, column or x, title, file_id, chart_name)
        elif chart_type == "scatter":
            url = generate_scatter_plot(df, x, y, title, file_id, chart_name)
        elif chart_type == "heatmap":
            url = generate_correlation_heatmap(df, title, file_id, chart_name)
        elif chart_type == "box":
            url = generate_box_plot(df, y or column, title, file_id, chart_name, x=x)
        else:
            raise ValueError(f"Unsupported chart type: {chart_type}")

        return {"title": title, "url": url, "chart_type": chart_type}

    except Exception as e:
        logger.error(f"Chart generation failed: {e}")
        raise


def create_interactive_chart(
    df: pd.DataFrame,
    chart_type: str,
    title: str,
    x: str | None = None,
    y: str | None = None,
    column: str | None = None,
) -> dict:
    """Create an interactive Plotly chart.

    Args:
        df: The dataset DataFrame.
        chart_type: One of 'line', 'bar', 'histogram', 'scatter', 'pie', 'box'.
        title: Chart title.
        x: X-axis column name.
        y: Y-axis column name.
        column: Column name.

    Returns:
        Dictionary with chart title, Plotly JSON data, and type.
    """
    logger.info(f"Creating interactive {chart_type} chart: {title}")

    try:
        data = generate_interactive_chart(df, chart_type, title, x, y, column)
        return {
            "title": title,
            "plotly_data": data,
            "chart_type": chart_type,
            "is_interactive": True
        }
    except Exception as e:
        logger.error(f"Interactive chart generation failed: {e}")
        return {"error": f"Failed to generate interactive chart: {str(e)}"}
