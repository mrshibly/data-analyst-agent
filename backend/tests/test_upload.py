"""Tests for file upload and preview endpoints."""

import io


def test_upload_csv(client, sample_csv_bytes):
    """Uploading a valid CSV should return 200 with metadata."""
    response = client.post(
        "/api/v1/upload",
        files={"file": ("test_data.csv", io.BytesIO(sample_csv_bytes), "text/csv")},
    )
    assert response.status_code == 200

    data = response.json()
    assert "file_id" in data
    assert data["filename"] == "test_data.csv"
    assert data["row_count"] == 5
    assert data["column_count"] == 4
    assert len(data["columns"]) == 4
    assert len(data["preview"]) > 0


def test_upload_invalid_extension(client):
    """Uploading a non-CSV/Excel file should return 400."""
    fake_content = b"some random content"
    response = client.post(
        "/api/v1/upload",
        files={"file": ("test.txt", io.BytesIO(fake_content), "text/plain")},
    )
    assert response.status_code == 400


def test_upload_empty_file(client):
    """Uploading an empty file should return 400."""
    response = client.post(
        "/api/v1/upload",
        files={"file": ("empty.csv", io.BytesIO(b""), "text/csv")},
    )
    assert response.status_code == 400


def test_file_preview(client, sample_csv_bytes):
    """Previewing an uploaded file should return data."""
    # First upload
    upload_response = client.post(
        "/api/v1/upload",
        files={"file": ("test_data.csv", io.BytesIO(sample_csv_bytes), "text/csv")},
    )
    file_id = upload_response.json()["file_id"]

    # Then preview
    preview_response = client.get(f"/api/v1/files/{file_id}/preview")
    assert preview_response.status_code == 200

    data = preview_response.json()
    assert data["file_id"] == file_id
    assert data["row_count"] == 5
    assert len(data["preview"]) > 0
    assert "numeric_columns" in data
    assert "categorical_columns" in data


def test_preview_nonexistent_file(client):
    """Previewing a non-existent file should return 404."""
    response = client.get("/api/v1/files/nonexistent/preview")
    assert response.status_code == 404
