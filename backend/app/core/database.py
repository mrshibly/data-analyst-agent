"""SQLite Database Module for safe, concurrent file registry storage."""

import json
import sqlite3
from pathlib import Path
from typing import Any, Optional

from app.core.config import settings
from app.core.logging_config import get_logger

logger = get_logger(__name__)

DB_PATH = Path(settings.upload_dir) / "registry.db"


def get_db_connection() -> sqlite3.Connection:
    """Get a thread-safe connection to the SQLite database."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH), timeout=10.0)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initialize the SQLite database schema."""
    with get_db_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS file_registry (
                file_id TEXT PRIMARY KEY,
                filename TEXT NOT NULL,
                file_path TEXT NOT NULL,
                file_size INTEGER NOT NULL,
                row_count INTEGER NOT NULL,
                column_count INTEGER NOT NULL,
                metadata_json TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    logger.info(f"Initialized SQLite file registry at {DB_PATH}")


def db_register_file(file_id: str, filename: str, file_path: str, file_size: int, metadata: dict[str, Any]) -> None:
    """Register a new file in the SQLite registry."""
    row_count = metadata.get("row_count", 0)
    column_count = metadata.get("column_count", 0)
    metadata_json = json.dumps(metadata)

    with get_db_connection() as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO file_registry
            (file_id, filename, file_path, file_size, row_count, column_count, metadata_json)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (file_id, filename, file_path, file_size, row_count, column_count, metadata_json),
        )
        conn.commit()


def db_get_file(file_id: str) -> Optional[dict[str, Any]]:
    """Retrieve metadata for a file by file_id."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM file_registry WHERE file_id = ?", (file_id,))
        row = cursor.fetchone()
        if not row:
            return None

        result = dict(row)
        metadata = json.loads(result["metadata_json"])
        result.update(metadata)
        return result


def db_list_files() -> list[dict[str, Any]]:
    """List all registered files."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM file_registry ORDER BY created_at DESC")
        rows = cursor.fetchall()
        files = []
        for r in rows:
            item = dict(r)
            meta = json.loads(item["metadata_json"])
            item.update(meta)
            files.append(item)
        return files
