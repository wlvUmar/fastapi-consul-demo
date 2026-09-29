import httpx
async def register() -> None:
    try:
        httpx.put("http://localhost:8500/v1/agent/service/register",json={"ID":"service-b", "Name": "Service B", "Address":"127.0.0.0.1", "Port":8002})
    except Exception as e:
        pass
    return None


async def deregister() -> None:
    try:
        httpx.put("http://localhost:8500/v1/agent/service/deregister/service-b")
    except Exception as e:
        pass
    return None

