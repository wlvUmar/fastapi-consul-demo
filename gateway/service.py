import logging

import httpx
from fastapi import HTTPException

from .infrastructure.discovery import DiscoveryError, ServiceResolver
from .infrastructure.http_client import get_client

logger = logging.getLogger("gateway")


async def fetch_info(service_key: str, resolver: ServiceResolver, timeout: float) -> dict:
    try:
        base_url = await resolver.resolve(service_key)
    except DiscoveryError as exc:
        logger.warning("discovery failed for %s: %s", service_key, exc)
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    logger.info("forwarding %s -> %s/info", service_key, base_url)
    try:
        response = await get_client().get(f"{base_url}/info", timeout=timeout)
        response.raise_for_status()
    except httpx.ConnectError as exc:
        logger.warning("%s unreachable at %s", service_key, base_url)
        raise HTTPException(status_code=503, detail=f"{service_key} unavailable") from exc
    except httpx.TimeoutException as exc:
        logger.warning("%s timed out at %s", service_key, base_url)
        raise HTTPException(status_code=504, detail=f"{service_key} timed out") from exc
    except httpx.HTTPStatusError as exc:
        logger.warning("%s error at %s: %s", service_key, base_url, exc.response.status_code)
        raise HTTPException(
            status_code=502, detail=f"{service_key} error: {exc.response.status_code}"
        ) from exc
    return response.json()
