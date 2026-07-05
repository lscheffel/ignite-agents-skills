# Endpoint Specification: {Resource}

## Overview

| Field | Value |
|-------|-------|
| Resource | {Resource} |
| Base URL | `/v1/{resource}` |
| Description | {Brief description} |

## Endpoints

### GET /v1/{resource}

**Description:** List all {resource}

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| page | integer | No | 1 | Page number |
| limit | integer | No | 20 | Items per page |
| sort | string | No | created_at | Sort field |
| order | string | No | desc | Sort order (asc/desc) |

**Response 200:**

```json
{
  "data": [
    {
      "id": "string",
      "name": "string",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

**Response 401:**
```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Authentication required"
  }
}
```

### POST /v1/{resource}

**Description:** Create a new {resource}

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Resource name |
| description | string | No | Resource description |

**Request Example:**

```json
{
  "name": "Example",
  "description": "Example description"
}
```

**Response 201:**

```json
{
  "data": {
    "id": "string",
    "name": "Example",
    "description": "Example description",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
}
```

**Response 400:**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [
      {
        "field": "name",
        "message": "Name is required"
      }
    ]
  }
}
```

### GET /v1/{resource}/{id}

**Description:** Get a specific {resource}

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| id | string | Yes | Resource ID |

**Response 200:**

```json
{
  "data": {
    "id": "string",
    "name": "string",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
}
```

**Response 404:**
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Resource not found"
  }
}
```

### PUT /v1/{resource}/{id}

**Description:** Update a {resource}

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| id | string | Yes | Resource ID |

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Resource name |
| description | string | No | Resource description |

**Request Example:**

```json
{
  "name": "Updated Name",
  "description": "Updated description"
}
```

**Response 200:**

```json
{
  "data": {
    "id": "string",
    "name": "Updated Name",
    "description": "Updated description",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
}
```

### DELETE /v1/{resource}/{id}

**Description:** Delete a {resource}

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| id | string | Yes | Resource ID |

**Response 204:**
No content

**Response 404:**
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Resource not found"
  }
}
```

## Notes

- All timestamps are in ISO 8601 format (UTC)
- IDs are strings (UUID format recommended)
- Use pagination for list endpoints
- PUT is idempotent
- DELETE returns 204 No Content on success
