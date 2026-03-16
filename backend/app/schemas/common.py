"""Common schemas shared across the application."""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "healthy"
    service: str = "data-analyst-agent"
    version: str = "1.0.0"


class ErrorResponse(BaseModel):
    """Standard error response."""
    error: str
    detail: str | None = None
