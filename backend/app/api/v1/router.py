"""V1 API router — aggregates all v1 endpoint routers."""

from fastapi import APIRouter

from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.upload import router as upload_router
from app.api.v1.endpoints.analysis import router as analysis_router

v1_router = APIRouter()

v1_router.include_router(health_router)
v1_router.include_router(upload_router)
v1_router.include_router(analysis_router)
