# FastAPI Microservices + Gateway (Consul-ready)

Three independent dummy microservices (A, B, C) plus an API Gateway.
Service discovery is environment-based for now; the architecture has
dedicated seams for adding Consul registration/discovery later
without restructuring.

## Structure

```text
services/service_a|service_b|service_c/
  main.py            # app factory + lifespan (Consul hook point)
  config.py          # env-based settings (name, host, port)
  schemas.py         # InfoResponse, HealthResponse
  service.py         # business logic (builds payloads)
  routes.py          # GET /info, GET /health (thin handlers)
  infrastructure/
    registration.py  # no-op stub; Consul registration goes here
gateway/
  main.py            # app factory + lifespan (httpx client lifecycle)
  config.py          # SERVICE_A/B/C_URL, REQUEST_TIMEOUT
  routes.py          # GET /service-a|b|c/info (thin handlers)
  service.py         # forwards to downstream via resolver + httpx
  schemas.py         # ErrorResponse
  infrastructure/
    discovery.py     # ServiceResolver protocol + EnvServiceResolver
    http_client.py   # shared httpx.AsyncClient
```

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
Copy-Item .env.example .env   # optional
```

## Run

From the project root, one terminal each:

```powershell
.\.venv\Scripts\python -m uvicorn services.service_a.main:app --host 127.0.0.1 --port 8001
.\.venv\Scripts\python -m uvicorn services.service_b.main:app --host 127.0.0.1 --port 8002
.\.venv\Scripts\python -m uvicorn services.service_c.main:app --host 127.0.0.1 --port 8003
.\.venv\Scripts\python -m uvicorn gateway.main:app --host 127.0.0.1 --port 8000
```

## Endpoints

| App     | Method | Path              | Returns                          |
| ------- | ------ | ----------------- | -------------------------------- |
| Service | GET    | `/info`           | `{service, timestamp}` (UTC)     |
| Service | GET    | `/health`         | `{status: ok, service}`          |
| Gateway | GET    | `/service-a/info` | Proxied Service A `/info`        |
| Gateway | GET    | `/service-b/info` | Proxied Service B `/info`        |
| Gateway | GET    | `/service-c/info` | Proxied Service C `/info`        |

## Configuration

| Variable          | Used by | Default                 |
| ----------------- | ------- | ----------------------- |
| `HOST` / `PORT`   | service | `127.0.0.1` / per-svc  |
| `SERVICE_NAME`    | service | `Service A` (B, C…)    |
| `SERVICE_A_URL`   | gateway | `http://localhost:8001` |
| `SERVICE_B_URL`   | gateway | `http://localhost:8002` |
| `SERVICE_C_URL`   | gateway | `http://localhost:8003` |
| `REQUEST_TIMEOUT` | gateway | `5.0` (seconds)         |

## Gateway error handling

| Situation              | Gateway status |
| ---------------------- | -------------- |
| Downstream unreachable | `503`          |
| Downstream timeout     | `504`          |
| Downstream HTTP error  | `502`          |
| Unknown service key    | `500`          |

## Adding Consul later

* **Services:** implement `register()` / `deregister()` in
  `services/<svc>/infrastructure/registration.py`. `main.py`
  already calls them in `lifespan`; nothing else changes.
* **Gateway:** add a `ConsulServiceResolver` implementing the
  `ServiceResolver` protocol in `gateway/infrastructure/discovery.py`
  and return it from `get_resolver()`. Routes and `service.py`
  stay untouched.
