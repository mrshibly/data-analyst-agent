"""Custom exception classes for the application."""

from fastapi import HTTPException, status


class FileValidationError(HTTPException):
    """Raised when an uploaded file fails validation."""

    def __init__(self, detail: str) -> None:
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class FileNotFoundError(HTTPException):
    """Raised when a requested file is not found."""

    def __init__(self, file_id: str) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File with ID '{file_id}' not found.",
        )


class AnalysisError(HTTPException):
    """Raised when analysis execution fails."""

    def __init__(self, detail: str) -> None:
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {detail}",
        )


class LLMError(HTTPException):
    """Raised when LLM API calls fail."""

    def __init__(self, detail: str) -> None:
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"LLM service error: {detail}",
        )


class ToolExecutionError(Exception):
    """Raised when a tool execution fails (internal, not HTTP)."""

    def __init__(self, tool_name: str, detail: str) -> None:
        self.tool_name = tool_name
        self.detail = detail
        super().__init__(f"Tool '{tool_name}' failed: {detail}")
