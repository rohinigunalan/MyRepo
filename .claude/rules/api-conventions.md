---
name: api-conventions
description: API design patterns and conventions for REST and internal APIs
globs:
  - "**/api/**/*.py"
  - "**/routes/**/*.py"
  - "**/endpoints/**/*.py"
  - "**/controllers/**/*.py"
---

# API Conventions

Standards for designing and implementing APIs (REST, internal, and external).

## REST API Design

### URL Structure

```
# Good - resource-oriented, hierarchical
GET    /api/v1/users
GET    /api/v1/users/{id}
POST   /api/v1/users
PUT    /api/v1/users/{id}
DELETE /api/v1/users/{id}
GET    /api/v1/users/{id}/orders
GET    /api/v1/users/{id}/orders/{order_id}

# Bad - action-oriented, inconsistent
GET    /api/v1/getAllUsers
POST   /api/v1/createNewUser
POST   /api/v1/user/delete/{id}
```

**Rules:**
- Use nouns for resources, not verbs
- Use plural nouns (`/users`, not `/user`)
- Hierarchical structure for relationships
- Version your API (`/v1/`, `/v2/`)
- Lowercase URLs with hyphens (`/user-profiles`)

### HTTP Methods

| Method | Purpose | Idempotent | Safe |
|--------|---------|------------|------|
| GET | Retrieve resource(s) | Yes | Yes |
| POST | Create new resource | No | No |
| PUT | Update/replace resource | Yes | No |
| PATCH | Partial update | No | No |
| DELETE | Remove resource | Yes | No |

**Idempotent**: Multiple identical requests have same effect as single request
**Safe**: Does not modify data

### HTTP Status Codes

#### Success (2xx)
```python
# 200 OK - Request succeeded
return jsonify(user), 200

# 201 Created - Resource created
return jsonify(user), 201, {"Location": f"/api/v1/users/{user.id}"}

# 204 No Content - Success with no response body
return "", 204
```

#### Client Errors (4xx)
```python
# 400 Bad Request - Invalid input
return jsonify({"error": "Invalid email format"}), 400

# 401 Unauthorized - Authentication required
return jsonify({"error": "Authentication required"}), 401

# 403 Forbidden - Authenticated but not allowed
return jsonify({"error": "Insufficient permissions"}), 403

# 404 Not Found - Resource doesn't exist
return jsonify({"error": "User not found"}), 404

# 409 Conflict - Resource conflict (duplicate)
return jsonify({"error": "Email already exists"}), 409

# 422 Unprocessable Entity - Validation failed
return jsonify({"error": "Validation failed", "details": errors}), 422
```

#### Server Errors (5xx)
```python
# 500 Internal Server Error - Unexpected error
return jsonify({"error": "Internal server error"}), 500

# 503 Service Unavailable - Service down
return jsonify({"error": "Database unavailable"}), 503
```

### Request/Response Format

#### Request Body (JSON)
```python
# POST /api/v1/users
{
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
}
```

#### Response Body (JSON)
```python
# Success response
{
    "id": 123,
    "username": "john_doe",
    "email": "john@example.com",
    "created_at": "2024-03-27T10:30:00Z",
    "updated_at": "2024-03-27T10:30:00Z"
}

# Error response
{
    "error": "Validation failed",
    "message": "Email format is invalid",
    "code": "VALIDATION_ERROR",
    "details": {
        "email": ["Must be a valid email address"]
    }
}
```

#### Headers
```python
# Request headers
Content-Type: application/json
Authorization: Bearer <token>
Accept: application/json

# Response headers
Content-Type: application/json
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1711540800
```

## Pagination

### Offset-based
```python
# Request
GET /api/v1/users?page=2&per_page=20

# Response
{
    "data": [...],
    "pagination": {
        "page": 2,
        "per_page": 20,
        "total": 150,
        "total_pages": 8,
        "has_next": true,
        "has_prev": true
    }
}
```

### Cursor-based
```python
# Request
GET /api/v1/users?cursor=abc123&limit=20

# Response
{
    "data": [...],
    "pagination": {
        "next_cursor": "xyz789",
        "prev_cursor": "def456",
        "has_more": true
    }
}
```

## Filtering, Sorting, Searching

```python
# Filtering
GET /api/v1/users?role=admin&is_active=true

# Sorting
GET /api/v1/users?sort_by=created_at&order=desc

# Searching
GET /api/v1/users?search=john

# Combined
GET /api/v1/users?role=admin&sort_by=email&order=asc&page=1
```

## API Versioning

### URL Versioning (Recommended)
```python
# Version in URL
/api/v1/users
/api/v2/users

# Easy to understand and test
# Clear separation between versions
```

### Header Versioning
```python
# Version in header
GET /api/users
Accept: application/vnd.api.v1+json

# Cleaner URLs
# More complex to implement
```

## Authentication

### Bearer Token (JWT)
```python
# Request
GET /api/v1/users/me
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Implementation
from flask import request
from functools import wraps

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({"error": "Authentication required"}), 401

        try:
            payload = decode_token(token)
            request.user = payload
        except InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/v1/users/me')
@require_auth
def get_current_user():
    return jsonify(request.user), 200
```

## Rate Limiting

```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=lambda: request.headers.get('Authorization'),
    default_limits=["100 per hour"]
)

@app.route('/api/v1/users')
@limiter.limit("20 per minute")
def list_users():
    pass

# Response headers
X-RateLimit-Limit: 20
X-RateLimit-Remaining: 15
X-RateLimit-Reset: 1711540800
```

## Error Handling

### Consistent Error Format
```python
{
    "error": "Short error type",
    "message": "Human-readable error message",
    "code": "ERROR_CODE",
    "details": {
        "field": ["Specific validation error"]
    },
    "timestamp": "2024-03-27T10:30:00Z",
    "request_id": "abc-123-def-456"
}
```

### Error Handler
```python
from flask import Flask, jsonify
import logging

app = Flask(__name__)
logger = logging.getLogger(__name__)

@app.errorhandler(400)
def bad_request(error):
    logger.warning(f"Bad request: {error}")
    return jsonify({
        "error": "Bad Request",
        "message": str(error),
        "code": "BAD_REQUEST"
    }), 400

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal error: {error}", exc_info=True)
    return jsonify({
        "error": "Internal Server Error",
        "message": "An unexpected error occurred",
        "code": "INTERNAL_ERROR"
    }), 500

# Custom exception
class ValidationError(Exception):
    def __init__(self, message, details=None):
        self.message = message
        self.details = details

@app.errorhandler(ValidationError)
def validation_error(error):
    return jsonify({
        "error": "Validation Failed",
        "message": error.message,
        "code": "VALIDATION_ERROR",
        "details": error.details
    }), 422
```

## Input Validation

```python
from marshmallow import Schema, fields, validate, ValidationError

class UserSchema(Schema):
    username = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=50)
    )
    email = fields.Email(required=True)
    age = fields.Int(
        validate=validate.Range(min=0, max=150)
    )
    role = fields.Str(
        validate=validate.OneOf(['user', 'admin', 'moderator'])
    )

@app.route('/api/v1/users', methods=['POST'])
def create_user():
    schema = UserSchema()

    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({
            "error": "Validation failed",
            "details": err.messages
        }), 422

    user = create_user_in_db(data)
    return jsonify(user), 201
```

## API Documentation

### Docstrings
```python
@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Get a user by ID.

    Args:
        user_id: Integer ID of the user

    Returns:
        200: User object
        404: User not found
        401: Authentication required

    Example:
        GET /api/v1/users/123
        Authorization: Bearer <token>

        Response:
        {
            "id": 123,
            "username": "john_doe",
            "email": "john@example.com"
        }
    """
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200
```

### OpenAPI/Swagger
Use tools like:
- **Flask**: Flask-RESTX, flasgger
- **FastAPI**: Built-in OpenAPI support
- **Django**: drf-spectacular

## Security

### Input Sanitization
```python
# Never trust user input
def create_user():
    data = request.json

    # Validate and sanitize
    username = data.get('username', '').strip()
    email = data.get('email', '').strip().lower()

    # Validate format
    if not is_valid_email(email):
        return jsonify({"error": "Invalid email"}), 400

    # Check for SQL injection patterns
    if contains_sql_injection(username):
        return jsonify({"error": "Invalid input"}), 400
```

### SQL Injection Prevention
```python
# Bad - SQL injection vulnerable
query = f"SELECT * FROM users WHERE username = '{username}'"
cursor.execute(query)

# Good - parameterized query
query = "SELECT * FROM users WHERE username = ?"
cursor.execute(query, (username,))

# Good - ORM
user = User.query.filter_by(username=username).first()
```

### CORS Configuration
```python
from flask_cors import CORS

# Development - allow all
CORS(app)

# Production - restrict origins
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://example.com"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

## Internal API Functions

### Function Design
```python
# Good - clear interface, type hints
def get_user_by_id(user_id: int) -> Optional[dict]:
    """
    Retrieve user by ID.

    Args:
        user_id: User ID to look up

    Returns:
        User dict if found, None otherwise

    Raises:
        DatabaseError: If database connection fails
    """
    try:
        user = User.query.get(user_id)
        return user.to_dict() if user else None
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        raise DatabaseError("Failed to fetch user") from e

# Good - specific parameters
def create_user(
    username: str,
    email: str,
    password: str,
    role: str = "user"
) -> dict:
    """Create a new user."""
    pass

# Bad - takes dict, unclear what's needed
def create_user(data: dict) -> dict:
    """Create a new user."""
    pass
```

### Return Values
```python
# Good - consistent return type
def get_users(filters: dict) -> List[dict]:
    """Returns list of users (empty if none found)."""
    users = User.query.filter_by(**filters).all()
    return [u.to_dict() for u in users]

# Good - optional return
def find_user(username: str) -> Optional[dict]:
    """Returns user if found, None otherwise."""
    user = User.query.filter_by(username=username).first()
    return user.to_dict() if user else None

# Bad - inconsistent return types
def get_user(user_id: int):
    """Returns user dict or False or None... unclear!"""
    user = User.query.get(user_id)
    if not user:
        return False  # or None? or empty dict?
    return user.to_dict()
```

## Testing APIs

### Unit Tests
```python
def test_create_user_endpoint(client):
    """Test user creation."""
    response = client.post('/api/v1/users', json={
        "username": "test_user",
        "email": "test@example.com"
    })

    assert response.status_code == 201
    data = response.json
    assert data["username"] == "test_user"
    assert "id" in data

def test_create_user_validation_error(client):
    """Test validation on invalid input."""
    response = client.post('/api/v1/users', json={
        "username": "a",  # Too short
        "email": "invalid-email"
    })

    assert response.status_code == 422
    assert "error" in response.json
```

### Integration Tests
```python
def test_user_workflow(client):
    """Test complete user CRUD workflow."""
    # Create
    response = client.post('/api/v1/users', json={
        "username": "test_user",
        "email": "test@example.com"
    })
    user_id = response.json["id"]

    # Read
    response = client.get(f'/api/v1/users/{user_id}')
    assert response.status_code == 200

    # Update
    response = client.put(f'/api/v1/users/{user_id}', json={
        "email": "updated@example.com"
    })
    assert response.json["email"] == "updated@example.com"

    # Delete
    response = client.delete(f'/api/v1/users/{user_id}')
    assert response.status_code == 204
```

---

*Good API design is about consistency and developer experience*
