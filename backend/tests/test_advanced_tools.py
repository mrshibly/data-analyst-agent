import pandas as pd
import pytest
from app.tools.cleaner import fill_missing_values, create_calculated_column
from app.tools.predictive import run_regression_model, detect_anomalies

def test_fill_missing_values():
    df = pd.DataFrame({"goals": [10, None, 20, 30], "name": ["A", "B", "C", "D"]})
    df_clean, info = fill_missing_values(df, strategy="mean", columns=["goals"])
    assert df_clean["goals"].isnull().sum() == 0
    assert df_clean["goals"].iloc[1] == 20.0
    assert "goals" in info

def test_create_calculated_column():
    df = pd.DataFrame({"goals": [10, 20], "matches": [5, 10]})
    df_new, info = create_calculated_column(df, "goals_per_match", "goals / matches")
    assert info["status"] == "success"
    assert "goals_per_match" in df_new.columns
    assert list(df_new["goals_per_match"]) == [2.0, 2.0]

def test_run_regression_model():
    df = pd.DataFrame({
        "rating": [7.0, 7.5, 8.0, 8.5, 9.0, 9.5],
        "goals": [10, 15, 20, 25, 30, 35]
    })
    res = run_regression_model(df, feature_cols=["rating"], target_col="goals")
    assert "r2_score" in res
    assert res["r2_score"] > 0.9

def test_detect_anomalies():
    df = pd.DataFrame({
        "value": [10, 11, 12, 10, 11, 1000]
    })
    res = detect_anomalies(df, top_n=2)
    assert res["anomalies_found"] >= 1
