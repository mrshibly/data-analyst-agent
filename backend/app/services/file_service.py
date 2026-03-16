"""File service — handles file storage and metadata retrieval."""

from pathlib import Path

import pandas as pd

from app.core.config import settings
from app.core.exceptions import FileValidationError, FileNotFoundError
from app.core.logging_config import get_logger
from app.tools.file_loader import load_dataset, inspect_dataset, preview_rows
from app.utils.file_utils import (
    generate_file_id,
    validate_extension,
    get_upload_path,
    get_file_size_mb,
)

logger = get_logger(__name__)

import json
import os

# Registry file path
REGISTRY_FILE = Path(settings.upload_dir) / "registry.json"

def _load_registry() -> dict:
    """Load the file registry from disk."""
    if not REGISTRY_FILE.exists():
        return {}
    try:
        with open(REGISTRY_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load registry: {e}")
        return {}

def _save_registry(registry: dict):
    """Save the file registry to disk."""
    try:
        os.makedirs(settings.upload_dir, exist_ok=True)
        with open(REGISTRY_FILE, "w") as f:
            json.dump(registry, f, indent=2)
    except Exception as e:
        logger.error(f"Failed to save registry: {e}")

# Load registry on module import
_file_registry: dict[str, dict] = _load_registry()


async def save_uploaded_file(filename: str, content: bytes) -> dict:
    """Validate, save, and register an uploaded file.

    Args:
        filename: Original filename from the upload.
        content: Raw file bytes.

    Returns:
        Dictionary with file metadata including file_id, columns, and preview.
    """
    # Validate extension
    if not validate_extension(filename):
        raise FileValidationError(
            f"Unsupported file type. Allowed: {', '.join(settings.allowed_extensions)}"
        )

    # Validate file size
    size_mb = get_file_size_mb(len(content))
    if size_mb > settings.max_file_size_mb:
        raise FileValidationError(
            f"File too large ({size_mb:.1f} MB). Maximum: {settings.max_file_size_mb} MB"
        )

    # Validate content is not empty
    if len(content) == 0:
        raise FileValidationError("Uploaded file is empty.")

    # Generate file ID and save
    file_id = generate_file_id()
    file_path = get_upload_path(file_id, filename)

    settings.ensure_directories()
    file_path.write_bytes(content)

    logger.info(f"Saved file: {filename} -> {file_path} (ID: {file_id})")

    # Load and inspect the dataset
    try:
        df = load_dataset(file_path)
    except Exception as e:
        # Clean up the file if loading fails
        file_path.unlink(missing_ok=True)
        raise FileValidationError(f"Failed to read file: {str(e)}")

    metadata = inspect_dataset(df)
    preview = preview_rows(df, n=5)

    # Register file
    _file_registry[file_id] = {
        "file_id": file_id,
        "filename": filename,
        "file_path": str(file_path),
        "file_size": len(content),
        **metadata,
    }
    _save_registry(_file_registry)

    return {
        "file_id": file_id,
        "filename": filename,
        "file_size": len(content),
        "row_count": metadata["row_count"],
        "column_count": metadata["column_count"],
        "columns": metadata["columns"],
        "preview": preview,
    }


def list_files() -> list[dict]:
    """List all registered files."""
    return list(_file_registry.values())


def get_file_metadata(file_id: str) -> dict:
    """Retrieve metadata for a registered file, with disk fallback."""
    if file_id in _file_registry:
        return _file_registry[file_id]
    
    # Try recovery from disk
    logger.info(f"File ID {file_id} not in registry, attempting disk recovery...")
    upload_dir = Path(settings.upload_dir)
    # Search for any file matching the file_id prefix
    matches = list(upload_dir.glob(f"{file_id}*"))
    if matches:
        file_path = matches[0]
        try:
            from app.tools.file_loader import load_dataset, inspect_dataset
            df = load_dataset(file_path)
            metadata = inspect_dataset(df)
            
            # Re-register
            _file_registry[file_id] = {
                "file_id": file_id,
                "filename": file_path.name.split('_', 1)[-1] if '_' in file_path.name else file_path.name,
                "file_path": str(file_path),
                "file_size": file_path.stat().st_size,
                **metadata,
            }
            _save_registry(_file_registry)
            logger.info(f"Successfully recovered file {file_id} from disk")
            return _file_registry[file_id]
        except Exception as e:
            logger.error(f"Failed to recover file {file_id} from disk: {e}")

    raise FileNotFoundError(file_id)


def get_file_path(file_id: str) -> Path:
    """Get the filesystem path for a registered file."""
    metadata = get_file_metadata(file_id)
    path = Path(metadata["file_path"])
    if not path.exists():
        raise FileNotFoundError(file_id)
    return path


def get_file_preview(file_id: str) -> dict:
    """Get preview data for a registered file."""
    metadata = get_file_metadata(file_id)
    file_path = Path(metadata["file_path"])
    df = load_dataset(file_path)
    preview = preview_rows(df, n=10)

    return {
        "file_id": file_id,
        "filename": metadata["filename"],
        "row_count": metadata["row_count"],
        "column_count": metadata["column_count"],
        "columns": metadata["columns"],
        "numeric_columns": metadata.get("numeric_columns", []),
        "categorical_columns": metadata.get("categorical_columns", []),
        "datetime_columns": metadata.get("datetime_columns", []),
        "preview": preview,
    }


def load_file_as_dataframe(file_id: str) -> pd.DataFrame:
    """Load a registered file as a pandas DataFrame."""
    file_path = get_file_path(file_id)
    return load_dataset(file_path)
