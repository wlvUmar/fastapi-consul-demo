import logging

import httpx

from ..config import settings

logger = logging.getLogger(settings.service_id)


async def register() -> None:
    payload = {
        "ID": settings.service_id,
        "Name": settings.service_id,
        "Address": settings.service_address,
        "Port": settings.port,
        "Check": {
            "HTTP": f"http://{settings.service_address}:{settings.port}/health",
            "Interval": "10s",
            "DeregisterCriticalServiceAfter": "1m",
        },
    }
    url = f"http://{settings.consul_host}:{settings.consul_port}/v1/agent/service/register"
    logger.info("registering with consul at %s", url)
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.put(url, json=payload)
            response.raise_for_status()
    except httpx.HTTPError as exc:
        logger.error("consul registration failed: %s", exc)
        return
    logger.info(
        "registered %s -> %s:%d", settings.service_id, settings.service_address, settings.port
    )


async def deregister() -> None:
    url = (
        f"http://{settings.consul_host}:{settings.consul_port}"
        f"/v1/agent/service/deregister/{settings.service_id}"
    )
    logger.info("deregistering %s", settings.service_id)
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.put(url)
            response.raise_for_status()
    except httpx.HTTPError as exc:
        logger.warning("consul deregistration failed: %s", exc)
        return
    logger.info("deregistered %s", settings.service_id)
