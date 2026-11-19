# Concept: Health checks (liveness vs readiness)

## What it is

A health check is a cheap probe that something outside a service (Docker Compose, a load balancer, Kubernetes, a monitoring tool) calls to decide what to do with the service. There are two common kinds, and they answer different questions:

- **Liveness**: "Is this process alive and able to respond?" If not, restart it.
- **Readiness**: "Can this instance usefully serve traffic right now?" (dependencies reachable, warm-up done). If not, stop sending it requests, but don't restart it.

## Why it matters here

[PLAT-01](../features/PLAT-01-backend-skeleton.md) has two health checks:

- `pg_isready` on the `db` service in `docker-compose.yml`. Compose uses it to hold back the `api` service until Postgres accepts connections (`depends_on: condition: service_healthy`). CI uses the same command for its Postgres service container.
- `GET /health` in `backend/app/main.py`. This is a liveness check: it returns `{"status": "ok"}` without touching the database.

## How it works

- If a liveness check depends on the database, a short database outage makes *every* API instance report unhealthy, and an orchestrator would restart them all. Restarting doesn't fix the database, and it adds a wave of reconnects just as the database recovers. So liveness checks should depend only on the process itself.
- A readiness check (for example `/ready` running `SELECT 1`) is where dependency checks belong, because the response to failing it is "route traffic elsewhere", which is harmless. ai-tutor doesn't have one yet because nothing consumes it. PLAT-04 (deployment) is the natural place to add one.
- Keeping `/health` dependency-free also makes it testable in-process with no infrastructure (`backend/tests/test_health.py`).
- A Compose `healthcheck` has `interval` (how often to probe), `timeout` (how long one probe may take), and `retries` (how many consecutive failures count as unhealthy). Until the first probe passes, the container's status is `starting`.

## Further reading

- Kubernetes liveness, readiness, and startup probes: https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/
- `pg_isready`: https://www.postgresql.org/docs/current/app-pg-isready.html
