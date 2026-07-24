"""Data Cleaning and Transformation Engine for Lumina Analyst."""

import pandas as pd
import numpy as np
from app.core.logging_config import get_logger

logger = get_logger(__name__)

def fill_missing_values(df: pd.DataFrame, strategy: str = "mean", columns: list[str] | None = None) -> tuple[pd.DataFrame, dict]:
    """Fill missing values in specified columns using strategy: 'mean', 'median', 'mode', 'zero', 'ffill'."""
    df_clean = df.copy()
    target_cols = columns if columns else list(df_clean.columns)
    filled_info = {}

    for col in target_cols:
        if col not in df_clean.columns:
            continue
        null_count = int(df_clean[col].isnull().sum())
        if null_count > 0:
            if strategy == "mean" and pd.api.types.is_numeric_dtype(df_clean[col]):
                val = df_clean[col].mean()
                df_clean[col] = df_clean[col].fillna(val)
            elif strategy == "median" and pd.api.types.is_numeric_dtype(df_clean[col]):
                val = df_clean[col].median()
                df_clean[col] = df_clean[col].fillna(val)
            elif strategy == "mode":
                mode_val = df_clean[col].mode()
                val = mode_val[0] if not mode_val.empty else "Unknown"
                df_clean[col] = df_clean[col].fillna(val)
            elif strategy == "zero":
                val = 0
                df_clean[col] = df_clean[col].fillna(val)
            elif strategy == "ffill":
                df_clean[col] = df_clean[col].ffill()
                val = "forward-filled"
            else:
                val = 0
                df_clean[col] = df_clean[col].fillna(val)
            
            filled_info[col] = {"nulls_filled": null_count, "fill_value": str(val)}

    return df_clean, filled_info


def create_calculated_column(df: pd.DataFrame, new_column_name: str, formula_expr: str) -> tuple[pd.DataFrame, dict]:
    """Create a new calculated column in the dataframe using pandas eval."""
    df_new = df.copy()
    try:
        df_new[new_column_name] = df_new.eval(formula_expr)
        logger.info(f"Created calculated column '{new_column_name}' with formula '{formula_expr}'")
        return df_new, {"status": "success", "new_column": new_column_name, "formula": formula_expr}
    except Exception as e:
        logger.error(f"Failed to create calculated column: {e}")
        return df, {"status": "error", "message": str(e)}
