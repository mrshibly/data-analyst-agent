"""Analysis service — runs pandas-based data analysis operations."""

import pandas as pd
import numpy as np

from app.core.logging_config import get_logger

logger = get_logger(__name__)


def compute_descriptive_stats(df: pd.DataFrame) -> dict:
    """Compute descriptive statistics for all numeric columns.

    Returns:
        Dictionary with describe() output and additional metrics.
    """
    logger.info("Computing descriptive statistics")
    numeric_df = df.select_dtypes(include=["number"])

    if numeric_df.empty:
        return {"message": "No numeric columns found for statistics."}

    stats = numeric_df.describe().round(2).to_dict()

    # Add additional metrics
    additional = {}
    for col in numeric_df.columns:
        additional[col] = {
            "median": round(float(numeric_df[col].median()), 2),
            "skewness": round(float(numeric_df[col].skew()), 2),
            "null_count": int(numeric_df[col].isna().sum()),
            "null_percentage": round(float(numeric_df[col].isna().mean() * 100), 2),
        }

    return {"descriptive": stats, "additional_metrics": additional}


def compute_correlations(df: pd.DataFrame) -> dict:
    """Compute correlation matrix for numeric columns.

    Returns:
        Correlation matrix as a nested dictionary.
    """
    logger.info("Computing correlations")
    numeric_df = df.select_dtypes(include=["number"])

    if len(numeric_df.columns) < 2:
        return {"message": "Need at least 2 numeric columns for correlation analysis."}

    corr_matrix = numeric_df.corr().round(3)
    return {
        "correlation_matrix": corr_matrix.to_dict(),
        "strongest_correlations": _find_strong_correlations(corr_matrix),
    }


def _find_strong_correlations(corr_matrix: pd.DataFrame, threshold: float = 0.5) -> list[dict]:
    """Find pairs of columns with strong correlations."""
    strong = []
    cols = corr_matrix.columns
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            val = corr_matrix.iloc[i, j]
            if abs(val) >= threshold:
                strong.append({
                    "column_1": cols[i],
                    "column_2": cols[j],
                    "correlation": round(float(val), 3),
                    "strength": "strong" if abs(val) >= 0.7 else "moderate",
                })
    return sorted(strong, key=lambda x: abs(x["correlation"]), reverse=True)


def compute_groupby_aggregation(
    df: pd.DataFrame,
    group_column: str,
    agg_column: str,
    agg_func: str = "sum",
) -> dict:
    """Perform group-by aggregation.

    Returns:
        Aggregated data as a list of records.
    """
    logger.info(f"Grouping by '{group_column}', aggregating '{agg_column}' with '{agg_func}'")

    if group_column not in df.columns:
        raise ValueError(f"Column '{group_column}' not found in dataset.")
    if agg_column not in df.columns:
        raise ValueError(f"Column '{agg_column}' not found in dataset.")

    valid_funcs = {"sum", "mean", "count", "min", "max", "median", "std"}
    if agg_func not in valid_funcs:
        raise ValueError(f"Invalid aggregation function. Use one of: {valid_funcs}")

    result = df.groupby(group_column)[agg_column].agg(agg_func).reset_index()
    result.columns = [group_column, f"{agg_column}_{agg_func}"]
    return {"data": result.to_dict(orient="records"), "group_column": group_column}


def compute_value_counts(df: pd.DataFrame, column: str, top_n: int = 10) -> dict:
    """Get value counts for a column."""
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in dataset.")

    counts = df[column].value_counts().head(top_n)
    return {
        "column": column,
        "value_counts": counts.to_dict(),
        "unique_count": int(df[column].nunique()),
        "total_count": int(len(df)),
    }


def detect_null_summary(df: pd.DataFrame) -> dict:
    """Produce a null value analysis summary."""
    null_info = []
    for col in df.columns:
        null_count = int(df[col].isna().sum())
        null_info.append({
            "column": col,
            "null_count": null_count,
            "null_percentage": round(null_count / len(df) * 100, 2) if len(df) > 0 else 0,
            "dtype": str(df[col].dtype),
        })
    return {
        "total_rows": len(df),
        "columns_with_nulls": [c for c in null_info if c["null_count"] > 0],
        "columns_without_nulls": [c["column"] for c in null_info if c["null_count"] == 0],
    }
