# Concept: FastAPI app structure

## What it is

FastAPI is a Python web framework built on ASGI (the async successor to WSGI) and Pydantic. You create an `app = FastAPI()` object and register route functions on it with decorators (`@app.get("/health")`). An ASGI server (uvicorn) runs that object and turns each HTTP request into a call to one of your functions. FastAPI validates the inputs, and serializes what you return, based on the function's type hints.

## Why it matters here

Every learner-facing capability in ai-tutor (creating a course, editing the outline, the Tutor chat, submitting an exercise) would be exposed as a FastAPI route, and the routes are the doorway into the shared Postgres database. [M03 — backend & data store](../curriculum/03-backend-and-data-store.md) traces one request through this structure.

## How it works

- **App object and server.** `uvicorn app.main:app` means "import module `app.main` and serve the variable `app`." Inside a container it's run with `--host 0.0.0.0` so it accepts connections from outside the container.
- **Routes.** A decorated function is a *path operation*. Path and query parameters are parsed and validated from the type hints (`course_id: int`). Return a dict or a Pydantic model and it becomes JSON. A response model (`-> list[KnowledgeOut]`) also controls which fields leave the server, and it feeds the auto-generated OpenAPI docs at `/docs`.
- **`def` vs `async def`.** FastAPI runs plain `def` endpoints in a threadpool, so blocking calls (sync SQLAlchemy, for example) don't stall the server. `async def` endpoints run on the event loop itself and must never block. Sync is the simpler starting point. Async matters once there are many long-lived concurrent connections, such as streaming Tutor responses.
- **Settings.** Configuration lives in one pydantic-settings `BaseSettings` class that reads environment variables (`DATABASE_URL`), cached so it's built once per process. Code asks for settings instead of reading `os.environ` all over the place.
- **Dependencies.** `Depends(get_session)` injects a per-request resource. The usual pattern is a generator that yields a SQLAlchemy session and closes it when the request finishes. Tests can override the dependency with a fake one.
- **Routers.** As routes multiply, they move into `APIRouter` modules (for example `routes/courses.py`) that the main app includes, so the entry file stays small.
- **Testing.** `TestClient(app)` calls the app in-process. No server or port is needed.

## Further reading

- FastAPI tutorial: https://fastapi.tiangolo.com/tutorial/
- Concurrency and `async def` vs `def`: https://fastapi.tiangolo.com/async/
- Settings with pydantic-settings: https://fastapi.tiangolo.com/advanced/settings/
- Dependencies: https://fastapi.tiangolo.com/tutorial/dependencies/
