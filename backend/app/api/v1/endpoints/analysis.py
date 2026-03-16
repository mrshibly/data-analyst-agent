"""Analysis endpoint — triggers the AI agent workflow."""

from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.core.config import settings
from app.schemas.analysis import AnalysisRequest, AnalysisResponse
from app.services.agent_service import run_analysis, run_analysis_stream
from sse_starlette.sse import EventSourceResponse
import json

router = APIRouter(tags=["analysis"])


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_dataset(request: AnalysisRequest) -> AnalysisResponse:
    """Analyze a dataset using the AI agent.

    Accepts a file ID and natural language query, runs the agent
    workflow (LLM reasoning → tool execution → LLM explanation),
    and returns structured analysis results.
    """
    return await run_analysis(
        file_id=request.file_id,
        query=request.query,
    )


@router.post("/analyze/stream")
@router.get("/analyze/stream")
async def analyze_dataset_stream(
    request: AnalysisRequest | None = None,
    file_id: str | None = None,
    query: str | None = None,
    history: str | None = None
):
    """Analyze a dataset with real-time streaming updates via SSE.
    Supports both POST (JSON body) and GET (query params) for compatibility.
    """
    # Resolve parameters from either POST request or GET query params
    f_id = request.file_id if request else file_id
    q = request.query if request else query
    raw_history = request.history if request else None
    
    if history and not raw_history:
        try:
            raw_history = json.loads(history)
        except:
            raw_history = None

    async def event_generator():
        try:
            if not f_id or not q:
                yield {"event": "error", "data": json.dumps({"detail": "Missing file_id or query"})}
                return

            async for update in run_analysis_stream(
                f_id, 
                q, 
                chat_history=raw_history
            ):
                yield {
                    "event": update["event"],
                    "data": json.dumps(update["data"])
                }
        except Exception as e:
            from app.core.logging_config import get_logger
            logger = get_logger(__name__)
            logger.error(f"Streaming error: {e}")
            yield {
                "event": "error",
                "data": json.dumps({"detail": str(e)})
            }

    return EventSourceResponse(event_generator())


@router.get("/files/{file_id}/charts/{chart_name}")
async def get_chart(file_id: str, chart_name: str) -> FileResponse:
    """Serve a generated chart image.

    Returns the PNG file for a specific chart associated with an uploaded file.
    """
    chart_path = Path(settings.chart_dir) / file_id / f"{chart_name}.png"

    if not chart_path.exists():
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chart '{chart_name}' not found.",
        )

    return FileResponse(
        path=str(chart_path),
        media_type="image/png",
        filename=f"{chart_name}.png",
    )
