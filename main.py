from fastapi import FastAPI

# Simple API used for health checks and service metadata.
app = FastAPI(title="my-app-1 FastAPI App", version="1.0.0")


# Liveness-style endpoint for quick monitoring checks.
@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


# Exposes the API version configured on the FastAPI app object.
@app.get("/version")
def version() -> dict[str, str]:
    return {"version": app.version}
