import httpx
from fastapi import HTTPException

from .infrastructure.discovery import ServiceResolver
from .infrastructure.http_client import get_client


async def fetch_info(service_key: str, resolver: ServiceResolver, timeout: float) -> dict:
    try:
        base_url = resolver.resolve(service_key)
    except KeyError as exc:
        raise HTTPException(status_code=500, detail=f"unknown service: {service_key}") from exc
    try:
        response = await get_client().get(f"{base_url.rstrip('/')}/info", timeout=timeout)
        response.raise_for_status()
    except httpx.ConnectError as exc:
        raise HTTPException(status_code=503, detail=f"{service_key} unavailable") from exc
    except httpx.TimeoutException as exc:
        raise HTTPException(status_code=504, detail=f"{service_key} timed out") from exc
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502, detail=f"{service_key} error: {exc.response.status_code}"
        ) from exc
    return response.json()
