"""Schemas for analysis endpoints."""

from pydantic import BaseModel, Field


class AnalysisRequest(BaseModel):
    """Request body for the analyze endpoint."""
    file_id: str = Field(..., description="ID of the uploaded file to analyze")
    query: str = Field(..., min_length=1, max_length=2000, description="Natural language query")
    history: list[dict] | None = Field(default=None, description="Optional conversation history")


class ChartInfo(BaseModel):
    """Information about a generated chart (static or interactive)."""
    title: str
    url: str | None = None
    chart_type: str = ""
    is_interactive: bool = False
    plotly_data: dict | None = None


class StatisticsInfo(BaseModel):
    """Summary statistics about the dataset."""
    row_count: int | None = None
    column_count: int | None = None
    numeric_columns: list[str] = Field(default_factory=list)
    categorical_columns: list[str] = Field(default_factory=list)
    descriptive_stats: dict | None = None


class AnalysisResponse(BaseModel):
    """Structured response from the analysis endpoint."""
    summary: str = Field(..., description="Natural language summary of the analysis")
    insights: list[str] = Field(default_factory=list, description="Key insights found")
    statistics: StatisticsInfo | None = None
    charts: list[ChartInfo] = Field(default_factory=list, description="Generated charts")
    data_preview: list[dict] = Field(default_factory=list, description="Relevant data rows")
    tool_calls: list[str] = Field(default_factory=list, description="Tools used during analysis")
