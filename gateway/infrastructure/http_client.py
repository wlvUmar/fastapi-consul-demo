import httpx

_client: httpx.AsyncClient | None = None


async def init_client(timeout: float) -> None:
    global _client
    if _client is None:
        _client = httpx.AsyncClient(timeout=timeout)


async def close_client() -> None:
    global _client
    if _client is not None:
        await _client.aclose()
        _client = None


def get_client() -> httpx.AsyncClient:
    if _client is None:
        raise RuntimeError("http client not initialized")
    return _client
