---
id: ADR-001-PI
type: pi
title: Implementation Plan - Implementação do JWT
created: 2026-01-01
updated: 2026-01-01
adr_ref: ADR-001
---

# ADR-001-PI: Implementation Plan - Implementação do JWT

> Reference: [ADR-001](./ADR-001.md) | [ADR-001-TODO](./ADR-001-TODO.md)

## 1. Overview
This plan describes how the autonomous agent will implement, test, and deploy the JWT service and Middleware in the application, ensuring ECDSA security.

## 2. Quality Standards
- **Test Coverage:** 100% coverage requirement for the `auth/` module.
- **Linter/Typing:** `mypy --strict` and `ruff check`.
- **Libraries:** Mandatory use of `PyJWT[crypto]`.

## 3. Granular Execution Plan (TDD & Step-by-Step)

### Phase A: Core Authentication

#### Step A1.1: Create JWT Adapter with PyJWT

**1. TDD Specs (What to test first):**
- **Test File:** `tests/auth/test_jwt_service.py`
- **Required Mocks:** Inject fake ECDSA keys for testing.
- **Expected Assertions:** 
  - `test_generate_token_success()`: Verifies if the payload contains `exp` and `sub`.
  - `test_decode_token_expired()`: Throws a custom `TokenExpiredError` when `exp` is in the past.
- **Test Command:** `pytest tests/auth/test_jwt_service.py -v`

**2. Code Specs (Implementation of the business rule):**
- **Affected Files:** `src/auth/jwt_service.py` and `src/auth/exceptions.py`
- **Signatures/Interfaces:**
  ```python
  import jwt
  
  class JWTService:
      def __init__(self, private_key: str, public_key: str): ...
      def create_access_token(self, user_id: str) -> str: ...
      def decode_token(self, token: str) -> dict[str, Any]: ...
  ```
- **Logic and Constants:**
  - `ALGORITHM = "ES256"`
  - Access token expiration time set to 15 minutes (use `datetime.utcnow()`).

**3. Integration and Terminal Commands:**
- `pip install "PyJWT[crypto]"`
- `pip freeze > requirements.txt`

**4. Edge Cases and Rollback (Failure Prevention):**
- **If PyJWT fails due to missing C dependencies (cryptography):** Add instructions to run `apt-get install build-essential libssl-dev libffi-dev` or use a fallback to `HS256` provisional, notifying the user.
- **Rollback:** In case of persistent failure, undo imports and revert the commit.

#### Step A1.2: Implement Auth Middleware

**1. TDD Specs (What to test first):**
- **Test File:** `tests/auth/test_middleware.py`
- **Mocks:** Mock the `JWTService` class to return fixed payloads. Use `httpx.AsyncClient` to simulate requests to the app ASGI.
- **Expected Assertions:**
  - Request without `Authorization` header returns HTTP 401.
  - Request with expired token returns HTTP 401 and JSON `{"detail": "Token expired"}`.
- **Test Command:** `pytest tests/auth/test_middleware.py -v`

**2. Code Specs:**
- **Affected Files:** `src/auth/middleware.py` and `src/main.py`
- **Logic:**
  - Extract the token from the HTTP header: `header.split("Bearer ")[1]`.
  - Catch `TokenExpiredError` from `jwt_service.py` and map it to the Web Framework's exception.

**3. Integration:**
- Register the middleware in the FastAPI instance in `src/main.py`.

**4. Edge Cases and Rollback:**
- Ensure that login endpoints do not pass through the Middleware (Whitelist or unprotected route).

## 4. Continuous Validation
```bash
# Validate Typing
mypy src/auth/

# Validate Linting
ruff check src/auth/

# Ensure Final Module Coverage
pytest tests/auth/ --cov=src/auth --cov-fail-under=100
```