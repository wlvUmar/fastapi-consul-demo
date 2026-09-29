# FastAPI Microservices + Gateway (Consul discovery)

Three independent dummy microservices (A, B, C) plus an API Gateway.
Services register themselves with Consul on startup and deregister on
shutdown; the gateway resolves downstream addresses through Consul at
request time. Logging uses `colorlog` throughout.

## Structure

```text
services/service_a|service_b|service_c/
  main.py            # app factory + lifespan (register/deregister)
  config.py          # env-based settings (name, id, host, port, consul)
  schemas.py         # InfoResponse, HealthResponse
  service.py         # business logic (builds payloads)
  routes.py          # GET /info, GET /health (thin handlers)
  infrastructure/
    registration.py  # Consul register/deregister via agent API
    logging.py       # colorlog setup
gateway/
  main.py            # app factory + lifespan (httpx client lifecycle)
  config.py          # CONSUL_HOST/PORT, REQUEST_TIMEOUT
  routes.py          # GET /service-a|b|c/info (thin handlers)
  service.py         # forwards to downstream via resolver + httpx
  schemas.py         # ErrorResponse
  infrastructure/
    discovery.py     # ServiceResolver protocol + ConsulServiceResolver
    http_client.py   # shared httpx.AsyncClient
    logging.py       # colorlog setup
```

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
Copy-Item .env.example .env   # optional
```

Start a local Consul agent (dev mode) first:

```powershell
consul agent -dev
```

## Run

From the project root, one terminal each (after Consul is up):

```powershell
.\.venv\Scripts\python -m uvicorn services.service_a.main:app --host 127.0.0.1 --port 8001
.\.venv\Scripts\python -m uvicorn services.service_b.main:app --host 127.0.0.1 --port 8002
.\.venv\Scripts\python -m uvicorn services.service_c.main:app --host 127.0.0.1 --port 8003
.\.venv\Scripts\python -m uvicorn gateway.main:app --host 127.0.0.1 --port 8000
```

Watch each terminal: services log `registering` / `registered` on startup
and `deregistering` / `deregistered` on shutdown; the gateway logs
`resolving` / `resolved` per request and `forwarding` lines.

## Endpoints

| App     | Method | Path              | Returns                          |
| ------- | ------ | ----------------- | -------------------------------- |
| Service | GET    | `/info`           | `{service, timestamp}` (UTC)     |
| Service | GET    | `/health`         | `{status: ok, service}`          |
| Gateway | GET    | `/service-a/info` | Proxied Service A `/info`        |
| Gateway | GET    | `/service-b/info` | Proxied Service B `/info`        |
| Gateway | GET    | `/service-c/info` | Proxied Service C `/info`        |

## Configuration

| Variable          | Used by      | Default                 |
| ----------------- | ------------ | ----------------------- |
| `HOST` / `PORT`   | service      | `127.0.0.1` / per-svc  |
| `SERVICE_NAME`    | service      | `Service A` (B, C…)    |
| `SERVICE_ID`      | service      | `service-a` (b, c…)    |
| `SERVICE_ADDRESS` | service      | `127.0.0.1`            |
| `CONSUL_HOST`     | all          | `127.0.0.1`            |
| `CONSUL_PORT`     | all          | `8500`                 |
| `REQUEST_TIMEOUT` | gateway      | `5.0` (seconds)         |

## Gateway error handling

| Situation                        | Gateway status |
| -------------------------------- | -------------- |
| Consul unreachable / no instance | `503`          |
| Downstream unreachable           | `503`          |
| Downstream timeout               | `504`          |
| Downstream HTTP error            | `502`          |

## Consul

* **Services:** `lifespan` in `main.py` calls `register()` on startup
  (PUT `/v1/agent/service/register` with an HTTP `/health` check) and
  `deregister()` on shutdown. Registration failures are logged and do
  not crash the service.
* **Gateway:** `get_resolver()` returns a `ConsulServiceResolver` that
  queries `/v1/health/service/<name>?passing=1` and picks a random
  healthy instance (naive client-side load balancing). To point at a
  different agent, set `CONSUL_HOST` / `CONSUL_PORT`.

## Reference

Assignment spec: <https://roadmap.sh/projects/service-discovery>
