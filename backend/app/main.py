"""Data Analyst Agent — FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse

from app.api.v1.router import v1_router
from app.core.config import settings
from app.core.logging_config import setup_logging, get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan — startup and shutdown events."""
    setup_logging(level="DEBUG" if settings.debug else "INFO")
    settings.ensure_directories()
    logger.info("Data Analyst Agent started")
    logger.info(f"LLM Provider: {settings.llm_provider}")
    logger.info(f"Upload dir: {settings.upload_dir}")
    logger.info(f"Chart dir: {settings.chart_dir}")
    yield
    logger.info("Data Analyst Agent shutting down")


app = FastAPI(
    title="Data Analyst Agent",
    description="An AI-powered data analysis agent that uses tool execution to analyze datasets.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers with version prefix
app.include_router(v1_router, prefix="/api/v1")

# Serve static files for the frontend
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os

# Resolve frontend dist directory relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Possible locations:
# 1. ../frontend/dist (Container structure)
# 2. ../../frontend/dist (Local dev structure)
frontend_dist = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend", "dist"))
if not os.path.exists(frontend_dist):
    frontend_dist = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "frontend", "dist"))

if os.path.exists(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")
    
    @app.get("/{full_path:path}")
    async def serve_spa(request: Request, full_path: str):
        # If the path starts with api/, ignore it so the router can handle it
        if full_path.startswith("api/"):
            # This shouldn't happen if prefixes match, but if it does, 
            # let's return a proper error or fallback
            return JSONResponse(status_code=404, content={"detail": "API endpoint not found"})
            

        # Check if it's a file that exists
        file_path = os.path.join(frontend_dist, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)

        # Otherwise, serve index.html for client-side routing
        return FileResponse(os.path.join(frontend_dist, "index.html"))
else:
    @app.get("/")
    async def root():
        return {"message": "Data Analyst Agent API is running. Frontend not found/built."}


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch unhandled exceptions and return a clean JSON error response."""
    from fastapi import HTTPException
    
    status_code = 500
    detail = str(exc)
    
    if isinstance(exc, HTTPException):
        status_code = exc.status_code
        detail = exc.detail
    else:
        logger.error(f"Unhandled exception: {type(exc).__name__}: {exc}")
        if not settings.debug:
            detail = "An unexpected error occurred."

    return JSONResponse(
        status_code=status_code,
        content={"detail": detail},
    )
