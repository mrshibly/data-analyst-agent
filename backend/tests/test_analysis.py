"""Tests for the analysis endpoint response structure."""

import io
from unittest.mock import patch, AsyncMock

from app.schemas.analysis import AnalysisResponse, StatisticsInfo


def test_analyze_missing_file(client):
    """Analysis with a non-existent file ID should return an error."""
    response = client.post(
        "/api/v1/analyze",
        json={"file_id": "nonexistent", "query": "summarize the data"},
    )
    # Should fail since the file doesn't exist
    assert response.status_code in (404, 500)


def test_analyze_empty_query(client):
    """Analysis with an empty query should return 422 validation error."""
    response = client.post(
        "/api/v1/analyze",
        json={"file_id": "some_id", "query": ""},
    )
    assert response.status_code == 422


def test_analysis_response_schema():
    """AnalysisResponse should serialize correctly."""
    response = AnalysisResponse(
        summary="Test summary",
        insights=["Insight 1", "Insight 2"],
        statistics=StatisticsInfo(
            row_count=100,
            column_count=5,
            numeric_columns=["revenue", "cost"],
        ),
        charts=[],
        data_preview=[],
        tool_calls=["compute_statistics"],
    )

    data = response.model_dump()
    assert data["summary"] == "Test summary"
    assert len(data["insights"]) == 2
    assert data["statistics"]["row_count"] == 100
    assert data["statistics"]["numeric_columns"] == ["revenue", "cost"]
    assert data["tool_calls"] == ["compute_statistics"]
