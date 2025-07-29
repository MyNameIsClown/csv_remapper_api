from fastapi import APIRouter

from app.api.v1.endpoints import router

v1_router = APIRouter()
v1_router.include_router(router, prefix="/v1", tags=["v1"])