# Feature: Backend skeleton + Postgres/pgvector + Docker

- Issue: #1 (PLAT-01)
- PR: #TBD
- Status: in progress

## What was built and why

This is the base every later feature runs on. Before this story the repo held only docs. After it there is:

- a Python package (`backend/app`) with a FastAPI app that answers `GET /health`,
- a typed settings object that reads configuration from environment variables,
- a SQLAlchemy engine/session setup and a declarative `Base` that future tables will inherit from,
- Alembic migrations, with one migration so far: it turns on the `vector` extension (pgvector) in Postgres,
- a Dockerfile for the API and a `docker-compose.yml` that starts Postgres (with pgvector) and the API together,
- pytest tests for the health endpoint and the migration chain, with CI running them against a real Postgres.

Why it matters: the architecture says agents and workflows share state through the database ([ADR 0001](../decisions/0001-agents-share-state-through-database.md)), and the knowledge store needs vector search. So the first thing to build is a database that can store vectors, plus a repeatable way to change its schema. No application tables exist yet. Each later story (courses, knowledge store, learner model) adds its tables as new migrations on top of `0001`.

## How it works

### 1. Configuration: `backend/app/config.py`

- `Settings` is a pydantic-settings `BaseSettings` class with two fields: `database_url` and `environment`. Pydantic-settings fills each field from the environment variable with the same name, case-insensitive (`DATABASE_URL`, `ENVIRONMENT`). If no variable is set, it reads a `.env` file in the current working directory. If neither exists, it uses the defaults in the class.
- The default `database_url` is `postgresql+psycopg://ai_tutor:ai_tutor@localhost:5432/ai_tutor`. The `+psycopg` part tells SQLAlchemy to use the psycopg 3 driver.
- `extra="ignore"` means unrelated variables in `.env` don't cause errors.
- `get_settings()` has `@lru_cache` on it, so the environment is read once per process and every caller gets the same object. One consequence: if you change `os.environ` after the first call, the app won't see the change unless you call `get_settings.cache_clear()`.
- `backend/.env.example` shows the one variable you'd normally set. Copy it to `backend/.env` for local runs. `.env` is gitignored and excluded from the Docker image.

### 2. Database plumbing: `backend/app/db.py`

- `Base(DeclarativeBase)` is the SQLAlchemy 2.0 base class. Every future ORM model (`class Course(Base): ...`) subclasses it, which registers the model's table on `Base.metadata`. Alembic reads that metadata to autogenerate migrations.
- `make_engine(url=None)` creates an `Engine` from the given URL, or from settings if none is passed. `pool_pre_ping=True` makes the pool check each connection with a cheap ping before handing it out, so a connection Postgres has dropped (say, after a container restart) is replaced quietly instead of raising an error.
- Module-level `engine = make_engine()` and `SessionLocal = sessionmaker(...)` are the shared objects the app will use. `create_engine` is lazy: it doesn't open a connection until one is first requested. That's why `import app.db` works on a laptop with no Postgres running.
- `SessionLocal` uses `autoflush=False` (no hidden writes before every query) and `expire_on_commit=False` (objects keep their loaded attributes after commit, so you can return them from a request handler without triggering a reload).

### 3. The API: `backend/app/main.py`

- `app = FastAPI(title="ai-tutor")` is the ASGI application. uvicorn serves it as `app.main:app`.
- `health()` handles `GET /health` and returns `{"status": "ok"}`. This is a liveness check on purpose: it shows the process is up and serving HTTP, and it never touches the database (see Design decisions).

### 4. Migrations: `backend/alembic.ini`, `backend/migrations/`

- `alembic.ini` sets `script_location` to `migrations/` and `prepend_sys_path` to the backend folder, so `import app...` works inside migration code. It has no `sqlalchemy.url` line. The URL comes from the app's own settings instead, so there's only one place to configure it.
- `migrations/env.py` runs every time you call an `alembic` command:
  - sets `target_metadata = Base.metadata` (used by `alembic revision --autogenerate` later),
  - `run_migrations_online()` opens a connection with `make_engine()` and runs the pending migration scripts inside a transaction,
  - `run_migrations_offline()` handles `alembic upgrade --sql`, which prints the SQL instead of running it.
- `migrations/versions/0001_enable_pgvector.py`:
  - `upgrade()` runs `CREATE EXTENSION IF NOT EXISTS vector`,
  - `downgrade()` runs `DROP EXTENSION IF EXISTS vector`,
  - `revision = "0001"`, `down_revision = None`, which makes it the root of the chain. The next migration will set `down_revision = "0001"`.
- Alembic records the current revision in a table it owns, `alembic_version`. Running `alembic upgrade head` compares that value with the scripts on disk and applies only what's missing.
- `migrations/script.py.mako` is the template for new migration files (`alembic revision -m "..."`).

### 5. Containers: `backend/Dockerfile`, `docker-compose.yml`

- The Dockerfile starts from `python:3.12-slim`, copies `pyproject.toml` and `app/`, runs `pip install .`, and then copies `alembic.ini` and `migrations/`. `tests/` and `.env` are excluded by `backend/.dockerignore`.
- `CMD` runs `alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000`. Because of `&&`, a failed migration stops uvicorn from starting, so you never get an API running against a half-migrated schema.
- `docker-compose.yml` defines two services:
  - `db`: image `pgvector/pgvector:pg16` (stock Postgres 16 with the pgvector extension files already installed), user/password/db all `ai_tutor`, port 5432 published to the host, data kept in the named volume `pgdata`, and a healthcheck that runs `pg_isready` every 2s.
  - `api`: built from `./backend`, `DATABASE_URL` points at host `db` (Compose's internal DNS name for the database container, not `localhost`), port 8000 published, and `depends_on: db: condition: service_healthy`, so the API container doesn't start until Postgres accepts connections.

### 6. Tests and CI

- `backend/tests/test_health.py::test_health_returns_ok` calls `/health` through FastAPI's in-process `TestClient`. No server or database is needed.
- `backend/tests/test_migrations.py` is marked `db` and skipped when `DATABASE_URL` isn't set:
  - `test_migrations_upgrade_and_downgrade_cleanly` runs upgrade to head, downgrade to base, then upgrade to head again. If any migration's `downgrade()` is broken, or a migration can't be re-applied, this test fails.
  - `test_pgvector_extension_enabled` upgrades, then checks `pg_extension` for a row where `extname = 'vector'`.
- `.github/workflows/ci.yml`: both jobs now pin Python 3.12. The `lint` job installs `backend[dev]`, so CI uses the same pinned ruff version (`ruff==0.17.5` in `pyproject.toml`) as local dev and the post-edit hook. The `test` job starts a `pgvector/pgvector:pg16` service container with a health check and sets `DATABASE_URL`, so the db-marked tests run in CI instead of being skipped. Tests run from inside `backend/` (`cd backend && pytest`), so `testpaths` and the relative paths resolve correctly.

## Data flow

Two flows matter: starting the stack, and what a request does once it's running.

```mermaid
flowchart TB
    subgraph Host["Your laptop"]
        DEV[docker compose up]
        CURL[curl localhost:8000/health]
        PYTEST[pytest with DATABASE_URL=...localhost:5432]
    end

    subgraph Compose["docker compose network"]
        subgraph DBC["db container: pgvector/pgvector:pg16"]
            PG[(Postgres 16)]
            HC{{pg_isready healthcheck}}
            VOL[(volume: pgdata)]
        end

        subgraph APIC["api container: python:3.12-slim"]
            ALE[alembic upgrade head<br/>migrations/env.py]
            MIG[0001_enable_pgvector.upgrade<br/>CREATE EXTENSION vector]
            UV[uvicorn app.main:app]
            H[main.py: health]
            CFG[config.py: get_settings<br/>DATABASE_URL=...@db:5432]
            ENG[db.py: make_engine]
        end
    end

    DEV --> DBC
    HC -- healthy --> APIC
    CFG --> ENG
    ENG --> ALE
    ALE --> MIG
    MIG -- SQL --> PG
    ALE -- writes revision 0001 --> PG
    PG --- VOL
    ALE -- success && --> UV
    UV --> H
    CURL --> H
    H -- "{status: ok} (no DB call)" --> CURL
    PYTEST -- upgrade/downgrade/upgrade --> PG
```

## Data stored

No application tables yet. After `alembic upgrade head` the database contains:

- **Extension `vector`** (pgvector, version 0.8.7 in the current image). It adds the `vector(n)` column type, distance operators (`<->` L2, `<=>` cosine, `<#>` negative inner product), and the HNSW/IVFFlat index types. Nothing uses it yet. The knowledge store will.
- **Table `alembic_version`**, owned by Alembic. It has one column, `version_num`, and one row holding the current head revision (`0001`).

Both are recorded in [docs/data/guide.md](../data/guide.md).

Data survives `docker compose down` because it's in the `pgdata` volume. Only `docker compose down -v` deletes it.

## Concepts used

- [FastAPI app structure](../concepts/fastapi-app-structure.md): how an ASGI app, routes, and uvicorn fit together, and where settings and DB sessions will plug in.
- [Database migrations](../concepts/database-migrations.md): why schema changes are versioned scripts (Alembic) rather than `create_all()` or hand-run SQL.
- [pgvector](../concepts/pgvector.md): the Postgres extension that will let the knowledge store hold embeddings and run similarity search in the same database as everything else.
- [Containerized local dev](../concepts/containerized-local-dev.md): Docker images, Compose services, internal DNS names, volumes, and dependency ordering.
- [Health checks: liveness vs readiness](../concepts/health-checks.md): what `/health` and `pg_isready` each prove, and why they're kept separate.

## Design decisions and rejected alternatives

| Decision | Chosen | Rejected | Why |
|---|---|---|---|
| Schema management | Alembic versioned migrations | `Base.metadata.create_all()`; hand-run `.sql` files | `create_all` only creates missing tables. It can't alter a column or add an index to a table that already exists, and it keeps no history. Raw SQL files need a home-made runner and version table. Alembic gives ordered, reversible scripts, an `alembic_version` record of where each database stands, and autogenerate from `Base.metadata`. |
| DB access style | Sync SQLAlchemy 2.0 + psycopg 3 | Async SQLAlchemy (`asyncpg` / async psycopg) | Sync code is easier to read, debug, and test while learning, and FastAPI runs plain `def` endpoints in a threadpool, so sync doesn't block the server. psycopg 3 also supports async, so switching later (for example if the live Tutor needs many concurrent streaming connections) doesn't mean changing drivers. |
| When migrations run | On container start (`CMD alembic upgrade head && uvicorn ...`) | A separate migrate step or one-off job | For local dev, one command bringing up a fully migrated stack is what you want. In production, running migrations from every replica on start can race, and it ties app startup to schema changes. PLAT-04 moves migrations to a deploy step. |
| `/health` semantics | Liveness only, no DB call | Readiness check that runs `SELECT 1` | Liveness should answer "is this process alive?" quickly and without dependencies. If it checked the DB, a Postgres blip would make an orchestrator restart healthy API containers, which doesn't fix anything. It also keeps `test_health.py` runnable with no database. A separate readiness endpoint can be added when something consumes it. |
| DB tests without a DB | `pytest.mark.skipif("DATABASE_URL" not in os.environ)` | Always require Postgres; mock the DB | `pytest` stays green on a laptop with nothing running, and CI (which provides Postgres) still runs the real tests. Mocking a migration test would prove nothing, because the point is that real Postgres accepts the SQL. |
| Postgres image | `pgvector/pgvector:pg16` | Stock `postgres:16` and compiling/installing pgvector ourselves | The official pgvector image is stock Postgres with the extension files pre-installed, so `CREATE EXTENSION vector` just works. Using the same image locally and in CI keeps the environments identical. |
| DB URL source | One `Settings.database_url`, read by app and Alembic | `sqlalchemy.url` in `alembic.ini` | One source of truth. With two, the app and the migrations can quietly point at different databases. |

Known trade-offs, accepted for now:

- The Dockerfile copies `app/` before `pip install .`, so any code edit invalidates the dependency-install layer and rebuilds take longer. Fine at this size. If builds get slow, install dependencies from `pyproject.toml` alone first.
- `test_migrations_upgrade_and_downgrade_cleanly` downgrades to `base`. Once real tables exist, running it against your local compose database will drop them along with their data. Point `DATABASE_URL` at a throwaway database when you run the db tests, or accept a reset.

## How to run and test it

Full stack in containers:

```bash
docker compose up -d --build          # from repo root
curl -i localhost:8000/health         # 200 {"status":"ok"}
docker compose logs api               # look for "Running upgrade  -> 0001, enable pgvector extension"
docker compose exec db psql -U ai_tutor -d ai_tutor \
  -c "SELECT extname, extversion FROM pg_extension;" \
  -c "SELECT * FROM alembic_version;"
docker compose down                   # keep data   (add -v to wipe the pgdata volume)
```

Tests on the host:

```bash
cd backend
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest                                 # 1 passed, 2 skipped (no DB)
docker compose up -d db                # from repo root, in another shell
DATABASE_URL=postgresql+psycopg://ai_tutor:ai_tutor@localhost:5432/ai_tutor pytest   # 3 passed
ruff check . && ruff format --check .
```

Note the host name: from your laptop the database is `localhost:5432`, because Compose publishes the port. From inside the `api` container it's `db:5432`.

## Check your understanding

1. `app/db.py` calls `make_engine()` when the module is imported, yet `test_health.py` passes with no Postgres running. Why? What would have to change in `main.py` for that test to start needing a database?
2. Suppose a future migration `0002` adds a `courses` table and you've already run `0001` on your local database. Which table tells Alembic to skip `0001` and run only `0002`, and what will it contain afterwards? Why would `Base.metadata.create_all()` be a poor substitute once `0003` needs to add a column to `courses`?
3. In `docker-compose.yml` the API's URL uses host `db`, but your `pytest` command uses `localhost`. Explain why both are correct, and what would happen if you put `localhost` in the `api` service's `DATABASE_URL`.
4. `/health` deliberately doesn't query the database. Describe a failure where a DB-checking health endpoint makes an outage worse rather than better.

Small experiments:

- **Break a migration on purpose.** With the stack running, temporarily change `0001`'s `upgrade()` SQL to `CREATE EXTENSION IF NOT EXISTS vectorx`, run `docker compose down -v && docker compose up --build`, and read `docker compose logs api`. Confirm that uvicorn never starts (that's the `&&`) and that `alembic_version` doesn't exist at all: Postgres runs DDL transactionally, so Alembic's creation of its own version table rolled back together with the failed migration (`SELECT * FROM alembic_version` gives "relation does not exist"). Revert afterwards.
- **Use the extension by hand.** In `docker compose exec db psql -U ai_tutor -d ai_tutor`, run
  `CREATE TEMP TABLE t (id int, v vector(3)); INSERT INTO t VALUES (1,'[1,0,0]'),(2,'[0,1,0]'),(3,'[0.9,0.1,0]'); SELECT id, v <=> '[1,0,0]' AS cosine_distance FROM t ORDER BY 2;`
  and predict the order before you look. Exit psql (the temp table depends on the extension and would block dropping it), then run `alembic downgrade base` from the host and try `SELECT '[1,2,3]'::vector;` again. What error do you get, and why?
- **Watch the dependency ordering.** Run `docker compose up` (not detached) and see that `api` logs nothing until `db` reports healthy. Then remove the `condition: service_healthy` line locally and run `docker compose down -v && docker compose up` a few times to see whether Alembic ever loses the race against a Postgres that's still starting.
