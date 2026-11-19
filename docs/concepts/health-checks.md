# Concept: Health checks (liveness vs readiness)

## What it is

A health check is a cheap probe that something outside a service (Docker Compose, a load balancer, Kubernetes, a monitor) calls to decide what to do with that service. The two common kinds answer different questions:

- **Liveness**: "Is this process alive and able to respond?" If not, restart it.
- **Readiness**: "Can this instance usefully serve traffic right now?" That means its dependencies are reachable and any warm-up is done. If not, stop routing requests to it, but don't restart it.

## Why it matters here

The ai-tutor substrate has two health checks, described in [M03 — backend & data store](../curriculum/03-backend-and-data-store.md):

- `pg_isready` on the `db` container. Compose uses it to hold back the API until Postgres accepts connections, so migrations don't fail on startup.
- `GET /health` on the API. It returns `{"status": "ok"}` and deliberately never touches the database: it's a liveness check.

## How it works

- **Why liveness shouldn't check dependencies.** If `/health` queried Postgres, a 30-second database blip would make *every* API instance report unhealthy, and an orchestrator would restart them all. Restarting doesn't fix the database, and the restarted instances all reconnect at once just as it recovers. That makes the outage worse.
- **Readiness is where dependency checks belong.** A `/ready` endpoint running `SELECT 1` is safe to fail, because the response is only "send traffic elsewhere for now." Add one when something (a deploy platform, a load balancer) actually consumes it.
- **A dependency-free liveness check is easy to test.** It can be called in-process with no database running.
- **Compose healthcheck knobs.** `interval` sets how often to probe, `timeout` how long one probe may take, and `retries` how many consecutive failures mark the container unhealthy. Until the first probe passes, its status is `starting`.

## Further reading

- Kubernetes liveness, readiness, and startup probes: https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/
- `pg_isready`: https://www.postgresql.org/docs/current/app-pg-isready.html
