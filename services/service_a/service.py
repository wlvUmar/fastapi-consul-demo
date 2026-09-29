from datetime import datetime, timezone

from .schemas import HealthResponse, InfoResponse


def build_info(service_name: str) -> InfoResponse:
    return InfoResponse(service=service_name, timestamp=datetime.now(timezone.utc))


def build_health(service_name: str) -> HealthResponse:
    return HealthResponse(status="ok", service=service_name)
