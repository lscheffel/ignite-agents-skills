# API Versioning Strategy

## Overview

This document defines the versioning strategy for the API.

## Versioning Approach

### URL Path Versioning (Recommended)

All versions are included in the URL path:

```
GET /v1/users
GET /v2/users
```

**Advantages:**
- Clear and explicit
- Easy to route
- Cache-friendly
- Browser-testable

### Header Versioning (Alternative)

Version specified in Accept header:

```
GET /users
Accept: application/vnd.api.v1+json
```

**Advantages:**
- Clean URLs
- Content negotiation

**Disadvantages:**
- Harder to test in browser
- Less visible

## Version Lifecycle

### Active Version

- Current stable version
- Fully supported
- Bug fixes applied

### Deprecated Version

- Still functional
- Warning headers included
- Migration timeline defined

### Retired Version

- No longer available
- Returns 410 Gone

## Versioning Rules

### When to Create New Version

Create a new version when:

- Breaking change to response structure
- Breaking change to request format
- Removing endpoints
- Changing authentication method

### When NOT to Create New Version

Do NOT create new version for:

- Adding new endpoints
- Adding new optional fields
- Adding new query parameters
- Adding new headers
- Bug fixes

## Backward Compatibility

### Safe Changes (No New Version Needed)

- Adding new field to response
- Adding new optional query parameter
- Adding new endpoint
- Adding new header
- Making field nullable

### Breaking Changes (New Version Required)

- Removing field from response
- Changing field type
- Renaming field
- Changing endpoint URL
- Requiring new field in request
- Changing authentication method

## Migration Guide

### Version 1 → Version 2

**Changes:**
- Response structure changed from `data` to `results`
- Added `metadata` field
- Renamed `id` to `uuid`

**Migration Steps:**

1. Update request URL:
   ```
   # Before
   GET /v1/users
   
   # After
   GET /v2/users
   ```

2. Update response handling:
   ```javascript
   // Before
   const users = response.data;
   
   // After
   const users = response.results;
   const metadata = response.metadata;
   ```

3. Update field references:
   ```javascript
   // Before
   const userId = user.id;
   
   // After
   const userId = user.uuid;
   ```

## Headers

### Deprecation Headers

When version is deprecated, include:

```http
Deprecation: true
Sunset: Sat, 01 Jan 2025 00:00:00 GMT
Link: <https://api.example.com/v2/docs>; rel="successor-version"
```

### Version Headers

Always include current version:

```http
X-API-Version: 1.0.0
X-API-Latest-Version: 2.0.0
```

## Error Responses

### Retired Version

```json
{
  "error": {
    "code": "VERSION_RETIRED",
    "message": "API version 1 has been retired",
    "details": [
      {
        "field": "version",
        "message": "Please migrate to version 2"
      }
    ]
  }
}
```

## Version Documentation

Each version should have:

- Changelog
- Migration guide
- Breaking changes list
- Deprecation timeline

## Examples

### Version 1 Request

```http
GET /v1/users?page=1&limit=20
Accept: application/json
Authorization: Bearer token123
```

### Version 1 Response

```json
{
  "data": [
    {
      "id": "123",
      "name": "John Doe",
      "email": "john@example.com"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100
  }
}
```

### Version 2 Request

```http
GET /v2/users?page=1&limit=20
Accept: application/json
Authorization: Bearer token123
```

### Version 2 Response

```json
{
  "results": [
    {
      "uuid": "123e4567-e89b-12d3-a456-426614174000",
      "name": "John Doe",
      "email": "john@example.com",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "metadata": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

## Notes

- Always document version changes
- Provide clear migration guides
- Use semantic versioning for API versions
- Plan deprecation timeline in advance
- Communicate changes to API consumers
