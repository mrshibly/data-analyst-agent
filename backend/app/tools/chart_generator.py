"""Chart Generator Tool — creates matplotlib/seaborn visualizations."""

from pathlib import Path
from io import BytesIO

import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from app.core.config import settings
from app.core.logging_config import get_logger
from app.utils.file_utils import get_chart_path

logger = get_logger(__name__)

# Apply a clean, modern style
sns.set_theme(style="darkgrid", palette="viridis")
plt.rcParams.update({
    "figure.figsize": (10, 6),
    "figure.dpi": 100,
    "font.size": 12,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
})


def generate_line_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    file_id: str,
    chart_name: str,
) -> str:
    """Generate a line chart and save it as PNG.

    Returns:
        URL path to the chart image.
    """
    fig, ax = plt.subplots()
    ax.plot(df[x], df[y], marker="o", linewidth=2, markersize=4)
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(title)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    chart_path = get_chart_path(file_id, chart_name)
    fig.savefig(chart_path, bbox_inches="tight")
    plt.close(fig)

    logger.info(f"Generated line chart: {chart_name}")
    return f"/api/v1/files/{file_id}/charts/{chart_name}"


def generate_bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    file_id: str,
    chart_name: str,
) -> str:
    """Generate a bar chart and save it as PNG."""
    fig, ax = plt.subplots()
    colors = sns.color_palette("viridis", n_colors=len(df[x].unique()))
    ax.bar(df[x].astype(str), df[y], color=colors)
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(title)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    chart_path = get_chart_path(file_id, chart_name)
    fig.savefig(chart_path, bbox_inches="tight")
    plt.close(fig)

    logger.info(f"Generated bar chart: {chart_name}")
    return f"/api/v1/files/{file_id}/charts/{chart_name}"


def generate_histogram(
    df: pd.DataFrame,
    column: str,
    title: str,
    file_id: str,
    chart_name: str,
    bins: int = 30,
) -> str:
    """Generate a histogram and save it as PNG."""
    fig, ax = plt.subplots()
    ax.hist(df[column].dropna(), bins=bins, color="#4C78A8", edgecolor="white", alpha=0.85)
    ax.set_xlabel(column)
    ax.set_ylabel("Frequency")
    ax.set_title(title)
    plt.tight_layout()

    chart_path = get_chart_path(file_id, chart_name)
    fig.savefig(chart_path, bbox_inches="tight")
    plt.close(fig)

    logger.info(f"Generated histogram: {chart_name}")
    return f"/api/v1/files/{file_id}/charts/{chart_name}"


def generate_scatter_plot(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    file_id: str,
    chart_name: str,
) -> str:
    """Generate a scatter plot and save it as PNG."""
    fig, ax = plt.subplots()
    ax.scatter(df[x], df[y], alpha=0.6, color="#E45756", edgecolors="white", s=50)
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(title)
    plt.tight_layout()

    chart_path = get_chart_path(file_id, chart_name)
    fig.savefig(chart_path, bbox_inches="tight")
    plt.close(fig)

    logger.info(f"Generated scatter plot: {chart_name}")
    return f"/api/v1/files/{file_id}/charts/{chart_name}"


def generate_correlation_heatmap(
    df: pd.DataFrame,
    title: str,
    file_id: str,
    chart_name: str,
) -> str:
    """Generate a correlation heatmap for numeric columns."""
    numeric_df = df.select_dtypes(include=["number"])
    if numeric_df.empty or len(numeric_df.columns) < 2:
        raise ValueError("Not enough numeric columns for a correlation heatmap.")

    corr = numeric_df.corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        square=True,
        linewidths=0.5,
        ax=ax,
    )
    ax.set_title(title)
    plt.tight_layout()

    chart_path = get_chart_path(file_id, chart_name)
    fig.savefig(chart_path, bbox_inches="tight")
    plt.close(fig)

    logger.info(f"Generated correlation heatmap: {chart_name}")
    return f"/api/v1/files/{file_id}/charts/{chart_name}"
def generate_box_plot(
    df: pd.DataFrame,
    y: str,
    title: str,
    file_id: str,
    chart_name: str,
    x: str | None = None,
) -> str:
    """Generate a box plot and save it as PNG."""
    fig, ax = plt.subplots()
    sns.boxplot(data=df, x=x, y=y, ax=ax, palette="viridis")
    ax.set_title(title)
    if x: ax.set_xlabel(x)
    ax.set_ylabel(y)
    plt.tight_layout()

    chart_path = get_chart_path(file_id, chart_name)
    fig.savefig(chart_path, bbox_inches="tight")
    plt.close(fig)

    logger.info(f"Generated box plot: {chart_name}")
    return f"/api/v1/files/{file_id}/charts/{chart_name}"
