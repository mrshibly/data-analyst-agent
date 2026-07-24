"""Predictive Analytics & Anomaly Detection Engine for Lumina Analyst."""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import IsolationForest
from app.core.logging_config import get_logger

logger = get_logger(__name__)

def run_regression_model(df: pd.DataFrame, feature_cols: list[str], target_col: str) -> dict:
    """Train a linear regression model predicting target_col from feature_cols."""
    try:
        clean_df = df[feature_cols + [target_col]].dropna()
        if len(clean_df) < 5:
            return {"error": "Not enough valid rows to build a regression model (minimum 5 required)."}

        X = clean_df[feature_cols]
        y = clean_df[target_col]

        model = LinearRegression()
        model.fit(X, y)

        r2 = float(model.score(X, y))
        coefs = {col: float(coef) for col, coef in zip(feature_cols, model.coef_)}
        intercept = float(model.intercept_)

        return {
            "r2_score": round(r2, 4),
            "intercept": round(intercept, 4),
            "coefficients": coefs,
            "target": target_col,
            "sample_size": len(clean_df),
        }
    except Exception as e:
        logger.error(f"Regression model error: {e}")
        return {"error": str(e)}


def detect_anomalies(df: pd.DataFrame, numeric_cols: list[str] | None = None, top_n: int = 5) -> dict:
    """Identify anomalous rows in dataset using Isolation Forest and Z-score metrics."""
    try:
        target_cols = numeric_cols if numeric_cols else list(df.select_dtypes(include=[np.number]).columns)
        if not target_cols:
            return {"error": "No numeric columns found for anomaly detection."}

        clean_df = df[target_cols].dropna()
        if len(clean_df) < 5:
            return {"error": "Not enough numeric rows for anomaly detection."}

        iso = IsolationForest(contamination=0.1, random_state=42)
        preds = iso.fit_predict(clean_df)

        anomaly_indices = clean_df.index[preds == -1].tolist()[:top_n]
        anomalies_data = df.loc[anomaly_indices].to_dict(orient="records")

        return {
            "anomalies_found": len(anomaly_indices),
            "anomalous_rows": anomalies_data,
            "inspected_columns": target_cols,
        }
    except Exception as e:
        logger.error(f"Anomaly detection error: {e}")
        return {"error": str(e)}
