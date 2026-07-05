# Error Contract

## Overview

This document defines the standard error format for all API endpoints.

## Error Response Format

All errors follow this structure:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": [
      {
        "field": "field_name",
        "message": "Specific error for this field"
      }
    ]
  }
}
```

## Error Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| code | string | Yes | Machine-readable error code |
| message | string | Yes | Human-readable error message |
| details | array | No | Additional error details |

## HTTP Status Codes

| Status | Code | Description |
|--------|------|-------------|
| 400 | BAD_REQUEST | Invalid request format |
| 400 | VALIDATION_ERROR | Request validation failed |
| 401 | UNAUTHORIZED | Authentication required |
| 403 | FORBIDDEN | Insufficient permissions |
| 404 | NOT_FOUND | Resource not found |
| 409 | CONFLICT | Resource conflict |
| 422 | UNPROCESSABLE_ENTITY | Business logic error |
| 429 | TOO_MANY_REQUESTS | Rate limit exceeded |
| 500 | INTERNAL_ERROR | Server error |
| 503 | SERVICE_UNAVAILABLE | Service temporarily unavailable |

## Error Codes

### Authentication Errors

| Code | Status | Description |
|------|--------|-------------|
| UNAUTHORIZED | 401 | Authentication required |
| INVALID_TOKEN | 401 | Token is invalid or expired |
| INSUFFICIENT_PERMISSIONS | 403 | User lacks required permissions |

### Validation Errors

| Code | Status | Description |
|------|--------|-------------|
| VALIDATION_ERROR | 400 | Request validation failed |
| REQUIRED_FIELD | 400 | Required field is missing |
| INVALID_FORMAT | 400 | Field format is invalid |
| INVALID_VALUE | 400 | Field value is invalid |

### Resource Errors

| Code | Status | Description |
|------|--------|-------------|
| NOT_FOUND | 404 | Resource not found |
| ALREADY_EXISTS | 409 | Resource already exists |
| CONFLICT | 409 | Resource conflict detected |

### Business Logic Errors

| Code | Status | Description |
|------|--------|-------------|
| UNPROCESSABLE_ENTITY | 422 | Business rule violation |
| INVALID_STATE | 422 | Invalid resource state |
| OPERATION_NOT_ALLOWED | 422 | Operation not permitted |

### Rate Limiting

| Code | Status | Description |
|------|--------|-------------|
| TOO_MANY_REQUESTS | 429 | Rate limit exceeded |

### Server Errors

| Code | Status | Description |
|------|--------|-------------|
| INTERNAL_ERROR | 500 | Unexpected server error |
| SERVICE_UNAVAILABLE | 503 | Service temporarily unavailable |

## Error Examples

### 400 Bad Request

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      },
      {
        "field": "password",
        "message": "Password must be at least 8 characters"
      }
    ]
  }
}
```

### 401 Unauthorized

```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Authentication required"
  }
}
```

### 404 Not Found

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "User with id '123' not found"
  }
}
```

### 409 Conflict

```json
{
  "error": {
    "code": "ALREADY_EXISTS",
    "message": "User with email 'john@example.com' already exists"
  }
}
```

### 429 Too Many Requests

```json
{
  "error": {
    "code": "TOO_MANY_REQUESTS",
    "message": "Rate limit exceeded. Try again in 60 seconds"
  }
}
```

## Headers

When returning errors, include these headers:

```http
X-Request-Id: unique-request-id
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1623456789
```

## Notes

- Always return JSON for errors
- Use consistent error codes across all endpoints
- Include request ID for debugging
- Log errors server-side with full context
- Never expose internal implementation details
