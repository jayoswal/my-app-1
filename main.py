from fastapi import FastAPI

app = FastAPI(title="my-app-1 FastAPI App", version="1.0.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/version")
def version() -> dict[str, str]:
    return {"version": app.version}
