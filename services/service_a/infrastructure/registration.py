import httpx
async def register() -> None:
    try:
        httpx.put("http://localhost:8500/v1/agent/service/register",json={"ID":"service-a", "Name": "Service A", "Address":"127.0.0.0.1", "Port":8001})
    except Exception as e:
        pass
    return None


async def deregister() -> None:
    try:
        httpx.put("http://localhost:8500/v1/agent/service/deregister/service-a")
    except Exception as e:
        pass
    return None

