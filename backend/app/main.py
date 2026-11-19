from fastapi import FastAPI

app = FastAPI(title="ai-tutor")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
