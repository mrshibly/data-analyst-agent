"""Schemas for file upload endpoints."""

from pydantic import BaseModel, Field


class ColumnInfo(BaseModel):
    """Information about a single dataset column."""
    name: str
    dtype: str
    non_null_count: int
    null_count: int
    sample_values: list[str] = Field(default_factory=list)


class UploadResponse(BaseModel):
    """Response returned after successful file upload."""
    file_id: str
    filename: str
    file_size: int
    row_count: int
    column_count: int
    columns: list[ColumnInfo]
    preview: list[dict] = Field(default_factory=list, description="First few rows as dicts")


class FilePreviewResponse(BaseModel):
    """Response for file preview endpoint."""
    file_id: str
    filename: str
    row_count: int
    column_count: int
    columns: list[ColumnInfo]
    preview: list[dict] = Field(default_factory=list)
    numeric_columns: list[str] = Field(default_factory=list)
    categorical_columns: list[str] = Field(default_factory=list)
    datetime_columns: list[str] = Field(default_factory=list)
