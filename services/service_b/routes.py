from fastapi import APIRouter

from .config import settings
from .schemas import HealthResponse, InfoResponse
from .service import build_health, build_info

router = APIRouter()


@router.get("/info", response_model=InfoResponse)
def get_info() -> InfoResponse:
    return build_info(settings.service_name)


@router.get("/health", response_model=HealthResponse)
def get_health() -> HealthResponse:
    return build_health(settings.service_name)
