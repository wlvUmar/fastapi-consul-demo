import httpx
async def register() -> None:
    try:
        httpx.put("http://localhost:8500/v1/agent/service/register",json={"ID":"service-c", "Name": "Service C", "Address":"127.0.0.0.1", "Port":8003})
    except Exception as e:
        pass
    return None


async def deregister() -> None:
    try:
        httpx.put("http://localhost:8500/v1/agent/service/deregister/service-c")
    except Exception as e:
        pass
    return None

