# Concept: Containerized local dev

## What it is

Instead of installing an app's services by hand on your laptop, you run them in Docker containers defined in files that live in the repo. Here those services are Postgres with pgvector, plus the API itself. One `docker compose up` gives everyone, and CI, the same versions configured the same way.

## Why it matters here

ai-tutor needs a specific Postgres major version *with* the pgvector extension compiled for it. Installing that on macOS by hand is fiddly and drifts over time. With Compose, the `pgvector/pgvector:pg16` image runs the same way on a laptop and in CI. [M03 — backend & data store](../curriculum/03-backend-and-data-store.md) walks through the two-container setup.

## How it works

- **Image vs container.** An *image* is a read-only filesystem snapshot plus a default command, built from a `Dockerfile`. A *container* is a running instance of an image. The API image would start from `python:3.12-slim`, install the app, and set its command to "migrate, then serve."
- **Layer caching.** Each Dockerfile instruction produces a cached layer. When a file copied in an early step changes, every later step reruns. That's why Dockerfiles copy the dependency manifest and install dependencies *before* copying the source code.
- **`.dockerignore`.** Keeps secrets (`.env`) and local clutter (`.venv`, caches) out of the image.
- **Compose services and DNS.** `docker-compose.yml` declares services (`db`, `api`) on a private network, where each one is reachable *by its service name*: the API connects to `db:5432`. Your laptop reaches the same database at `localhost:5432` only because `ports: "5432:5432"` publishes the port to the host. Inside the `api` container, `localhost` means the API container itself.
- **Volumes.** A container's filesystem is thrown away when the container is removed. A named volume (`pgdata` mounted at Postgres's data directory) keeps the database across `docker compose down`. `down -v` deletes it.
- **Startup ordering.** Plain `depends_on` only waits for the other container to *start*. `condition: service_healthy` waits for its healthcheck to pass, so migrations don't run against a Postgres that's still initialising. See [health checks](health-checks.md).
- **Configuration through env vars.** The same image runs locally, in CI, or in production with different `DATABASE_URL` values.

An illustrative compose file for this substrate:

```yaml
services:
  db:
    image: pgvector/pgvector:pg16
    environment: { POSTGRES_USER: ai_tutor, POSTGRES_PASSWORD: ai_tutor, POSTGRES_DB: ai_tutor }
    ports: ["5432:5432"]
    volumes: [pgdata:/var/lib/postgresql/data]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ai_tutor -d ai_tutor"]
      interval: 2s
  api:
    build: ./backend
    environment: { DATABASE_URL: "postgresql+psycopg://ai_tutor:ai_tutor@db:5432/ai_tutor" }
    ports: ["8000:8000"]
    depends_on: { db: { condition: service_healthy } }
volumes:
  pgdata:
```

## Further reading

- Docker Compose overview: https://docs.docker.com/compose/
- Networking in Compose: https://docs.docker.com/compose/how-tos/networking/
- Control startup order: https://docs.docker.com/compose/how-tos/startup-order/
