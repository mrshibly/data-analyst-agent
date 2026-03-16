"""File upload and preview endpoints."""

from fastapi import APIRouter, UploadFile, File

from app.schemas.upload import UploadResponse, FilePreviewResponse
from app.services.file_service import save_uploaded_file, get_file_preview

router = APIRouter(tags=["analysis"])


@router.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)) -> UploadResponse:
    """Upload a dataset file (CSV or Excel).

    Validates the file, stores it, and returns metadata including
    column information and a data preview.
    """
    content = await file.read()
    result = await save_uploaded_file(
        filename=file.filename or "upload.csv",
        content=content,
    )
    return UploadResponse(**result)


@router.get("/files/{file_id}/preview", response_model=FilePreviewResponse)
async def preview_file(file_id: str) -> FilePreviewResponse:
    """Get a preview of an uploaded dataset.

    Returns the first rows, column info, and column type classification.
    """
    result = get_file_preview(file_id)
    return FilePreviewResponse(**result)
