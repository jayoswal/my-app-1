### Python Version
> 3.12.3

### Run Command
`uvicorn main:app --reload`

### API Endpoints

#### GET /health
Returns the liveness status of the service.

**Example Request**
```bash
curl -X GET http://localhost:8000/health
```

**Example Response**
```json
{"status": "ok"}
```

#### GET /version
Returns the API version string.

**Example Request**
```bash
curl -X GET http://localhost:8000/version
```

**Example Response**
```json
{"version": "1.0.0"}
```

#### GET /users
Returns the full list of users.

**Example Request**
```bash
curl -X GET http://localhost:8000/users
```

**Example Response**
```json
[
  {"id": 1, "name": "Alice Johnson", "email": "alice@example.com"},
  {"id": 2, "name": "Bob Smith", "email": "bob@example.com"},
  {"id": 3, "name": "Carol White", "email": "carol@example.com"},
  {"id": 4, "name": "David Brown", "email": "david@example.com"},
  {"id": 5, "name": "Eva Martinez", "email": "eva@example.com"}
]
```
#### GET /users/{user_id}
Returns a single user by ID, or 404 if not found.

**Example Request**
```bash
curl -X GET http://localhost:8000/users/1
```

**Example Response**
```json
{"id": 1, "name": "Alice Johnson", "email": "alice@example.com"}
```

#### POST /users
Creates a new user and returns the created user object.

**Example Request**
```bash
curl -X POST http://localhost:8000/users -H "Content-Type: application/json" -d '{"name": "Frank Lee", "email": "frank@example.com"}'
```

**Example Response**
```json
{"id": 6, "name": "Frank Lee", "email": "frank@example.com"}
```
