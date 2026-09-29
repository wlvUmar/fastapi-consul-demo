from typing import Protocol

from ..config import settings


class ServiceResolver(Protocol):
    def resolve(self, service_key: str) -> str: ...


class EnvServiceResolver:
    def __init__(self, urls: dict[str, str]) -> None:
        self._urls = urls

    def resolve(self, service_key: str) -> str:
        return self._urls[service_key]


def get_resolver() -> ServiceResolver:
    return EnvServiceResolver(
        {
            "service-a": settings.service_a_url,
            "service-b": settings.service_b_url,
            "service-c": settings.service_c_url,
        }
    )
