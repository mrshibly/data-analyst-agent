"""File Loader Tool — loads and inspects datasets."""

from pathlib import Path

import pandas as pd

from app.core.logging_config import get_logger

logger = get_logger(__name__)


def load_dataset(file_path: str | Path) -> pd.DataFrame:
    """Load a dataset from a CSV or Excel file.

    Args:
        file_path: Path to the dataset file.

    Returns:
        Loaded pandas DataFrame.

    Raises:
        ValueError: If the file format is unsupported.
    """
    file_path = Path(file_path)
    suffix = file_path.suffix.lower()

    logger.info(f"Loading dataset: {file_path.name}")

    if suffix == ".csv":
        # Try multiple encodings for CSV
        encodings = ["utf-8", "utf-8-sig", "latin1"]
        df = None
        last_error = None

        for encoding in encodings:
            try:
                df = pd.read_csv(file_path, encoding=encoding)
                logger.info(f"Successfully loaded CSV with encoding: {encoding}")
                break
            except Exception as e:
                last_error = e
                continue
        
        if df is None:
            raise ValueError(f"Failed to read CSV with common encodings. Error: {str(last_error)}")
    elif suffix in (".xlsx", ".xls"):
        df = pd.read_excel(file_path)
    else:
        raise ValueError(f"Unsupported file format: {suffix}")

    if df is None:
        raise ValueError("Unknown error: dataset is None after loading attempt.")

    logger.info(f"Loaded {len(df)} rows, {len(df.columns)} columns")
    return df


def inspect_dataset(df: pd.DataFrame) -> dict:
    """Get metadata about a DataFrame.

    Returns:
        Dictionary with column info, data types, null counts, and sample values.
    """
    columns = []
    for col in df.columns:
        col_info = {
            "name": str(col),
            "dtype": str(df[col].dtype),
            "non_null_count": int(df[col].notna().sum()),
            "null_count": int(df[col].isna().sum()),
            "sample_values": [str(v) for v in df[col].dropna().head(3).tolist()],
        }
        columns.append(col_info)

    # Classify column types
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    datetime_cols = df.select_dtypes(include=["datetime64"]).columns.tolist()

    return {
        "row_count": len(df),
        "column_count": len(df.columns),
        "columns": columns,
        "numeric_columns": numeric_cols,
        "categorical_columns": categorical_cols,
        "datetime_columns": datetime_cols,
    }


def preview_rows(df: pd.DataFrame, n: int = 10) -> list[dict]:
    """Return the first n rows of a DataFrame as a list of dicts."""
    preview_df = df.head(n).copy()
    # Convert to serializable format
    for col in preview_df.columns:
        if preview_df[col].dtype == "datetime64[ns]":
            preview_df[col] = preview_df[col].astype(str)
    return preview_df.fillna("").to_dict(orient="records")
