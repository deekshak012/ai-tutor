# Concept: Containerized local dev

## What it is

The services an app depends on (here, Postgres with pgvector, plus the API itself) run in Docker containers defined in a file, instead of being installed by hand on your laptop. `docker compose up` gives everyone, and CI, the same versions configured the same way.

## Why it matters here

ai-tutor needs a specific Postgres major version *with* the pgvector extension installed. Installing that on macOS by hand is fiddly and drifts over time. [PLAT-01](../features/PLAT-01-backend-skeleton.md) adds `backend/Dockerfile` and a root `docker-compose.yml`, and CI uses the same `pgvector/pgvector:pg16` image as a service container.

## How it works

- **Image vs container.** An *image* is a read-only filesystem snapshot plus a default command, built from a `Dockerfile`. A *container* is a running instance of an image. `backend/Dockerfile` builds an image from `python:3.12-slim` with the app installed, and its `CMD` runs migrations and then uvicorn.
- **Layer caching.** Each Dockerfile instruction produces a cached layer. When a file copied in an early step changes, every later step reruns. That's why Dockerfiles usually copy dependency manifests and install dependencies *before* copying source code.
- **`.dockerignore`.** Keeps the build context small and prevents secrets (`.env`) and local junk (`.venv`, caches) from ending up in the image.
- **Compose services.** `docker-compose.yml` declares services (`db`, `api`). Compose puts them on a private network where each service is reachable *by its service name*: the API connects to `db:5432`. Your laptop reaches the same database at `localhost:5432` only because `ports: "5432:5432"` publishes the port to the host. Inside the `api` container, `localhost` means the API container itself.
- **Volumes.** Container filesystems are thrown away when the container is removed. The named volume `pgdata` mounted at `/var/lib/postgresql/data` keeps database files across `docker compose down`. `docker compose down -v` deletes the volume too.
- **Startup ordering.** Plain `depends_on` only waits for the other container to *start*. `condition: service_healthy` waits for its healthcheck (`pg_isready`) to pass, so migrations don't run against a Postgres that's still initializing. See [health checks](health-checks.md).
- **Environment variables.** Containers are configured through env vars (`DATABASE_URL`), which the app reads through pydantic-settings. The same image can then run locally, in CI, or in production with different settings.

Everyday commands:

```bash
docker compose up -d --build   # build and start in the background
docker compose ps              # status + health
docker compose logs -f api     # follow logs
docker compose exec db psql -U ai_tutor -d ai_tutor
docker compose down            # stop (keep data); add -v to wipe volumes
```

## Further reading

- Docker Compose overview: https://docs.docker.com/compose/
- Networking in Compose: https://docs.docker.com/compose/how-tos/networking/
- Control startup order: https://docs.docker.com/compose/how-tos/startup-order/
