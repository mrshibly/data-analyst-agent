"""File utility helpers for validation and path management."""

import uuid
from pathlib import Path

from app.core.config import settings


ALLOWED_EXTENSIONS = {ext.lower() for ext in settings.allowed_extensions}


def generate_file_id() -> str:
    """Generate a unique file identifier."""
    return uuid.uuid4().hex[:16]


def validate_extension(filename: str) -> bool:
    """Check if the file extension is allowed."""
    suffix = Path(filename).suffix.lower()
    return suffix in ALLOWED_EXTENSIONS


def get_safe_filename(file_id: str, original_filename: str) -> str:
    """Generate a safe filename using the file_id and original extension."""
    suffix = Path(original_filename).suffix.lower()
    return f"{file_id}{suffix}"


def get_upload_path(file_id: str, original_filename: str) -> Path:
    """Get the full path for storing an uploaded file."""
    safe_name = get_safe_filename(file_id, original_filename)
    return Path(settings.upload_dir) / safe_name


def get_chart_path(file_id: str, chart_name: str) -> Path:
    """Get the full path for storing a chart image."""
    chart_dir = Path(settings.chart_dir) / file_id
    chart_dir.mkdir(parents=True, exist_ok=True)
    return chart_dir / f"{chart_name}.png"


def get_file_size_mb(size_bytes: int) -> float:
    """Convert bytes to megabytes."""
    return size_bytes / (1024 * 1024)
