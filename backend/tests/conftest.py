"""Test fixtures and shared test configuration."""

import os
import csv
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Set test environment variables before importing app
os.environ["LLM_PROVIDER"] = "groq"
os.environ["GROQ_API_KEY"] = "test-key"
os.environ["UPLOAD_DIR"] = tempfile.mkdtemp()
os.environ["CHART_DIR"] = tempfile.mkdtemp()

from app.main import app


@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def sample_csv_path(tmp_path) -> Path:
    """Create a sample CSV file for testing."""
    csv_path = tmp_path / "test_data.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "age", "salary", "department"])
        writer.writerow(["Alice", 30, 70000, "Engineering"])
        writer.writerow(["Bob", 25, 55000, "Marketing"])
        writer.writerow(["Charlie", 35, 85000, "Engineering"])
        writer.writerow(["Diana", 28, 62000, "Sales"])
        writer.writerow(["Eve", 32, 78000, "Marketing"])
    return csv_path


@pytest.fixture
def sample_csv_bytes(sample_csv_path) -> bytes:
    """Read sample CSV as bytes."""
    return sample_csv_path.read_bytes()
