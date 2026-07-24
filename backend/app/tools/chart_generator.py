"""Chart Generator Tool — thread-safe matplotlib/seaborn visualizations."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
from matplotlib.figure import Figure
import seaborn as sns
import pandas as pd

from app.core.config import settings
from app.core.logging_config import get_logger
from app.utils.file_utils import get_chart_path

logger = get_logger(__name__)


def _create_base_figure(figsize: tuple[int, int] = (10, 6)) -> tuple[Figure, any]:
    """Create an isolated, thread-safe Matplotlib Figure and Axes."""
    fig = Figure(figsize=figsize, dpi=100)
    ax = fig.add_subplot(111)
    ax.set_facecolor("#1e1e2e")
    fig.patch.set_facecolor("#181825")
    ax.tick_params(colors="white", which="both", labelsize=10)
    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")
    ax.title.set_color("white")
    ax.grid(True, linestyle="--", alpha=0.3)
    return fig, ax


def generate_line_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    file_id: str,
    chart_name: str,
) -> str:
    """Generate a thread-safe line chart and save it as PNG."""
    fig, ax = _create_base_figure()
    ax.plot(df[x], df[y], marker="o", linewidth=2, markersize=4, color="#89b4fa")
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    ax.tick_params(axis="x", rotation=45)
    fig.set_tight_layout(True)

    chart_path = get_chart_path(file_id, chart_name)
    fig.savefig(chart_path, bbox_inches="tight")

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
    """Generate a thread-safe bar chart and save it as PNG."""
    fig, ax = _create_base_figure()
    colors = sns.color_palette("viridis", n_colors=len(df[x].unique()))
    ax.bar(df[x].astype(str), df[y], color=colors)
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    ax.tick_params(axis="x", rotation=45)
    fig.set_tight_layout(True)

    chart_path = get_chart_path(file_id, chart_name)
    fig.savefig(chart_path, bbox_inches="tight")

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
    """Generate a thread-safe histogram and save it as PNG."""
    fig, ax = _create_base_figure()
    ax.hist(df[column].dropna(), bins=bins, color="#89b4fa", edgecolor="#11111b", alpha=0.85)
    ax.set_xlabel(column)
    ax.set_ylabel("Frequency")
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    fig.set_tight_layout(True)

    chart_path = get_chart_path(file_id, chart_name)
    fig.savefig(chart_path, bbox_inches="tight")

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
    """Generate a thread-safe scatter plot and save it as PNG."""
    fig, ax = _create_base_figure()
    ax.scatter(df[x], df[y], alpha=0.7, color="#f38ba8", edgecolors="#11111b", s=50)
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    fig.set_tight_layout(True)

    chart_path = get_chart_path(file_id, chart_name)
    fig.savefig(chart_path, bbox_inches="tight")

    logger.info(f"Generated scatter plot: {chart_name}")
    return f"/api/v1/files/{file_id}/charts/{chart_name}"


def generate_correlation_heatmap(
    df: pd.DataFrame,
    title: str,
    file_id: str,
    chart_name: str,
) -> str:
    """Generate a thread-safe correlation heatmap for numeric columns."""
    numeric_df = df.select_dtypes(include=["number"])
    if numeric_df.empty or len(numeric_df.columns) < 2:
        raise ValueError("Not enough numeric columns for a correlation heatmap.")

    corr = numeric_df.corr()
    fig, ax = _create_base_figure(figsize=(10, 8))
    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        square=True,
        linewidths=0.5,
        ax=ax,
        cbar_kws={"shrink": 0.8},
    )
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    fig.set_tight_layout(True)

    chart_path = get_chart_path(file_id, chart_name)
    fig.savefig(chart_path, bbox_inches="tight")

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
    """Generate a thread-safe box plot and save it as PNG."""
    fig, ax = _create_base_figure()
    sns.boxplot(data=df, x=x, y=y, ax=ax, palette="viridis")
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    if x:
        ax.set_xlabel(x)
    ax.set_ylabel(y)
    fig.set_tight_layout(True)

    chart_path = get_chart_path(file_id, chart_name)
    fig.savefig(chart_path, bbox_inches="tight")

    logger.info(f"Generated box plot: {chart_name}")
    return f"/api/v1/files/{file_id}/charts/{chart_name}"

