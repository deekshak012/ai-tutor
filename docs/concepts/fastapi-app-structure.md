# Concept: FastAPI app structure

## What it is

FastAPI is a Python web framework built on ASGI (the async successor to WSGI) and Pydantic. You create an `app = FastAPI()` object, register route functions on it with decorators (`@app.get("/health")`), and an ASGI server (uvicorn) runs that object and turns HTTP requests into calls to your functions. FastAPI validates inputs and serializes outputs from the type hints on those functions.

## Why it matters here

Every learner-facing capability (course creation, the Tutor chat, exercise submission) will be exposed as FastAPI routes. [PLAT-01](../features/PLAT-01-backend-skeleton.md) sets up the minimum: `backend/app/main.py` (the app and `/health`), `backend/app/config.py` (settings), and `backend/app/db.py` (engine and sessions).

## How it works

- **App object and server.** `uvicorn app.main:app` means "import module `app.main` and serve the variable `app`." The Dockerfile runs it with `--host 0.0.0.0` so it accepts connections from outside the container.
- **Routes.** A decorated function is a path operation. Return a dict or a Pydantic model and FastAPI turns it into JSON. The return type hint (`-> dict[str, str]`) also feeds the auto-generated OpenAPI docs at `/docs`.
- **`def` vs `async def`.** FastAPI runs plain `def` endpoints in a threadpool so they don't block the event loop. That's why sync SQLAlchemy works fine here. `async def` endpoints run on the event loop itself and must never make blocking calls.
- **Settings.** Configuration lives in one Pydantic `BaseSettings` class that reads env vars, cached with `@lru_cache` so it's built once. Code calls `get_settings()` instead of reading `os.environ` all over the place.
- **Dependencies (coming soon).** FastAPI's `Depends(...)` injects per-request resources. The usual pattern, which later stories will add, is a `get_session()` dependency that yields a `SessionLocal()` and closes it when the request finishes. Tests can override it.
- **Routers (coming soon).** As routes multiply, they move into `APIRouter` modules (for example `app/routes/courses.py`) that `main.py` includes, so `main.py` stays small.
- **Testing.** `fastapi.testclient.TestClient(app)` calls the app in-process over a fake transport. No server or port is needed.

## Further reading

- FastAPI tutorial: https://fastapi.tiangolo.com/tutorial/
- Concurrency and `async def` vs `def`: https://fastapi.tiangolo.com/async/
- Settings with pydantic-settings: https://fastapi.tiangolo.com/advanced/settings/
