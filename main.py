from fastapi import FastAPI, HTTPException

# Simple API used for health checks and service metadata.
app = FastAPI(title="my-app-1 FastAPI App", version="1.0.0")

_USERS = [
    {"id": 1, "name": "Alice Johnson", "email": "alice@example.com"},
    {"id": 2, "name": "Bob Smith",     "email": "bob@example.com"},
    {"id": 3, "name": "Carol White",   "email": "carol@example.com"},
    {"id": 4, "name": "David Brown",   "email": "david@example.com"},
    {"id": 5, "name": "Eva Martinez",  "email": "eva@example.com"},
]


# Liveness-style endpoint for quick monitoring checks.
@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


# Exposes the API version configured on the FastAPI app object.
@app.get("/version")
def version() -> dict[str, str]:
    return {"version": app.version}


# Returns the full list of in-memory users.
@app.get("/users")
def get_users() -> list[dict]:
    return _USERS


# Returns a single user by ID, or 404 if not found.
@app.get("/users/{user_id}")
def get_user(user_id: int) -> dict:
    for user in _USERS:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")
