import logging
import random
from typing import Protocol

import httpx

from ..config import settings
from .http_client import get_client

logger = logging.getLogger("gateway")


class DiscoveryError(Exception):
    pass


class ServiceResolver(Protocol):
    async def resolve(self, service_key: str) -> str: ...


class ConsulServiceResolver:
    def __init__(self, base_url: str, timeout: float) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    async def resolve(self, service_key: str) -> str:
        logger.info("resolving %s via consul", service_key)
        try:
            response = await get_client().get(
                f"{self._base_url}/v1/health/service/{service_key}",
                params={"passing": "1"},
                timeout=self._timeout,
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise DiscoveryError(f"consul lookup failed for {service_key}") from exc
        instances = response.json()
        if not instances:
            raise DiscoveryError(f"no healthy instances of {service_key}")
        chosen = random.choice(instances)
        service = chosen["Service"]
        address = service["Address"] or chosen["Node"]["Address"]
        target = f"http://{address}:{service['Port']}"
        logger.info("resolved %s -> %s (%d candidate(s))", service_key, target, len(instances))
        return target


def get_resolver() -> ServiceResolver:
    return ConsulServiceResolver(
        base_url=f"http://{settings.consul_host}:{settings.consul_port}",
        timeout=settings.request_timeout,
    )
