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

logger.info(f"Frontend dist path: {frontend_dist}")
if os.path.exists(frontend_dist):
    logger.info("Found frontend dist, mounting static files...")
    # Mount assets directory
    assets_dir = os.path.join(frontend_dist, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")
        logger.info(f"Mounted /assets from {assets_dir}")
    
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        logger.debug(f"Incoming request: {request.method} {request.url.path}")
        response = await call_next(request)
        if response.status_code >= 400:
            logger.error(f"Request failed: {request.method} {request.url.path} -> {response.status_code}")
        return response

    @app.get("/{full_path:path}")
    async def serve_spa(request: Request, full_path: str):
        # Ignore API calls
        if full_path.startswith("api/"):
            return JSONResponse(status_code=404, content={"detail": "API endpoint not found"})
            
        # Check if the requested path is a real file in dist/
        file_path = os.path.join(frontend_dist, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)

        # Fallback to index.html for SPA routing
        index_path = os.path.join(frontend_dist, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        
        return JSONResponse(status_code=404, content={"detail": "Frontend index not found"})
else:
    logger.warning("Frontend dist directory NOT FOUND. Dashboard will not be served.")
    @app.get("/")
    async def root():
        return {"message": "Data Analyst Agent API is running. Frontend not found/built."}

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch unhandled exceptions and return a clean JSON error response."""
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
