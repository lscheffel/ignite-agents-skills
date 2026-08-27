---
name: api-design
version: 2.0.0
description: Comprehensive guide to designing robust, consistent, and scalable RESTful and GraphQL APIs. Define standards for endpoints, versioning, error contracts, pagination, and idempotence. Use when designing new APIs, reviewing existing contracts, or standardizing interface design practices.
related_skills:
  - cap
  - implementation
  - technical-documentation
domain: architecture-systems
triggers:
  - api-design
  - rest-api
  - graphql-design
  - api-contract
  - design-de-api
  - projetar-api
  - contrato-de-api
  - error-contracts
  - api-versioning
tags:
- api
- rest
- graphql
- endpoints
- versioning
metadata:
  author: Antigravity Refactored Architecture
  provenance: internal
  last_audited: '2026-08-05'
---

# API Design

Guide to designing robust, consistent, and scalable APIs.

## When to Use

### Use when:
- You need to design new endpoints
- You need to define an API contract
- You need to implement versioning
- You need to standardize error handling
- You need to review an existing API

### Do not use when:
- You need a quick prototype without formal contracts
- You are working on an internal API between services of the same team
- An SDK already exists and is well-defined

### Related Skills:
- `documentation` — for API documentation
- `testing` — for contract testing
- `governance` — for review processes

## Decision Tree

```mermaid
graph TD
    A[Do you need to expose data?] -->|Yes| B[Is the API public?]
    A -->|No| C[Use messaging]
    B -->|Yes| D[REST or GraphQL?]
    B -->|No| E[Internal API]
    D -->|Simple CRUD| F[REST]
    D -->|Complex queries| G[GraphQL]
    F --> H[Define CRUD endpoints]
    H --> I[Versioning]
    I --> J[Error format]
    J --> K[ pagination]
    K --> L[Idempotence]
    L --> M[API ready]
    G --> N[GraphQL schema]
    N --> O[Resolvers]
    O --> I
```

## Fundamental Concepts

### RESTful Design

API based on HTTP resources.

- **Resources** represent entities
- **Methods** define actions
- **Status codes** communicate results

```
GET    /users         → List users
POST   /users         → Create user
GET    /users/{id}    → Get user
PUT    /users/{id}    → Update user
DELETE /users/{id}    → Delete user
```

### Idempotence

Operations that produce the same result even if executed multiple times.

- **Idempotent**: GET, PUT, DELETE
- **Not idempotent**: POST, PATCH (by default)
- **Safe**: GET, HEAD, OPTIONS

### Versioning

Strategies to evolve the API without breaking clients.

- **URL path**: `/v1/users` (recommended)
- **Header**: `Accept: application/vnd.api.v1+json`
- **Query param**: `/users?version=1`

### API Contract

Formal agreement on data format.

- Request/Response schema
- Error codes
- Date formatting
- Pagination

## Workflow

### Phase 1: Define Resources

1. Identify domain entities:
   ```bash
   # List entities from the model
   grep -r "model\|entity" src/
   ```
2. Create resource-URL mapping:
   ```
   /users          → User
   /orders         → Order
   /products       → Product
   ```
3. Define relationships:
   ```
   /users/{id}/orders   → Orders of the user
   /orders/{id}/items   → Items of the order
   ```
4. **Checkpoint**: Approved list of resources

### Phase 2: Specify Endpoints

1. For each resource, define operations:
   ```yaml
   /users:
     get:
       summary: List users
       parameters:
         - name: page
           in: query
           schema:
             type: integer
             default: 1
       responses:
         200:
           description: List of users
related_skills:
  - cap
  - implementation
  - technical-documentation
   ```
2. Use the `endpoint-spec.md` template
3. Document request/response
4. **Checkpoint**: Complete specification

### Phase 3: Define Error Handling

1. Create a standardized error contract:
   ```json
   {
     "error": {
       "code": "VALIDATION_ERROR",
       "message": "Invalid email",
       "details": [
         {
           "field": "email",
           "message": "Invalid format"
         }
       ]
     }
   }
   ```
2. Use the `error-contract.md` template
3. Map HTTP status codes to errors
4. **Checkpoint**: Error contract defined

### Phase 4: Implement Versioning

1. Choose a versioning strategy:
   ```bash
   # Recommended: URL path
   /v1/users
   /v2/users
   ```
2. Use the `api-versioning.md` template
3. Define deprecation policy
4. **Checkpoint**: Versioning working

### Phase 5: Add Pagination

1. Implement consistent pagination:
   ```json
   {
     "data": [...],
     "pagination": {
       "page": 1,
       "per_page": 20,
       "total": 100,
       "total_pages": 5
     }
   }
   ```
2. Define default limits
3. Add pagination headers
4. **Checkpoint**: Pagination tested

### Phase 6: Ensure Idempotence

1. Identify non-idempotent operations
2. Implement idempotency keys:
   ```http
   POST /payments
   Idempotency-Key: 550e8400-e29b-41d4-a716-446655440000
   ```
3. Store temporary responses
4. **Checkpoint**: Idempotence verified

## Templates

### endpoint-spec.md
Location: `templates/endpoint-spec.md`

Template for endpoint specification.

**Usage:**
```bash
cp templates/endpoint-spec.md docs/api/users.md
```

### error-contract.md
Location: `templates/error-contract.md`

Template for error contract.

**Usage:**
```bash
cp templates/error-contract.md docs/api/errors.md
```

### api-versioning.md
Location: `templates/api-versioning.md`

Template for API versioning.

**Usage:**
```bash
cp templates/api-versioning.md docs/api/versioning.md
```

## Anti-patterns

### Critical

#### Endpoint without Consistent Error Handling
**What is it:** Endpoints that return errors in different formats.
**Why is it bad:** Clients cannot handle errors programmatically.
**How to avoid:** Use a standardized error contract on all endpoints.
**Example:**
```
# ❌ WRONG
GET /users/999
{ "msg": "user not found" }

GET /orders/999
Status: 404 Not Found
# No body

# ✅ RIGHT
GET /users/999
{
  "error": {
    "code": "NOT_FOUND",
    "message": "User not found",
    "details": [{"field": "id", "message": "User with id 999 does not exist"}]
  }
}
```

#### PUT without Idempotence
**What is it:** PUT that creates duplicate resources on repeated calls.
**Why is it bad:** Violates the REST contract, causes inconsistencies.
**How to avoid:** PUT must be idempotent, use POST for creation.
**Example:**
```
# ❌ WRONG
PUT /users
{ "name": "John" }
# Creates new user on each call

# ✅ RIGHT
PUT /users/123
{ "name": "John" }
# Updates existing user, idempotent
```

### Medium

#### POST for Read Operations
**What is it:** Using POST for fetching data.
**Why is it bad:** Confuses HTTP semantics, hinders caching.
**How to avoid:** Use GET for reading, POST for creation.
**Example:**
```
# ❌ WRONG
POST /search
{ "query": "users" }

# ✅ RIGHT
GET /users?q=users
# or
GET /search?q=users
```

#### Versioning Breaking Clients
**What is it:** Incompatible changes without a new version.
**Why is it bad:** Breaks existing clients.
**How to avoid:** Use versioning, maintain backward compatibility.
**Example:**
```
# ❌ WRONG
# v1: GET /users returns { "name": "John" }
# v2: GET /users returns { "fullName": "John" }
# No migration

# ✅ RIGHT
# v1: GET /users returns { "name": "John" }
# v2: GET /users returns { "fullName": "John", "name": "John" }
# Maintains compatibility
```

### Low

#### Optional Query Params without Default
**What is it:** Parameters without a defined default value.
**Why is it bad:** Unpredictable behavior, different clients may behave differently.
**How to avoid:** Always define default values for optional parameters.
**Example:**
```
# ❌ WRONG
GET /users?page=&limit=

# ✅ RIGHT
GET /users?page=1&limit=20
# Or document that omitting uses defaults: page=1, limit=20
```

## Checklists

### Checklist for Endpoint Design
- [ ] Resource clearly identified
- [ ] Correct HTTP method (GET, POST, PUT, DELETE)
- [ ] Consistent path naming (kebab-case or camelCase)
- [ ] Parameters documented
- [ ] Request body defined
- [ ] Responses defined (200, 201, 204, 400, 404, 500)
- [ ] Necessary headers listed

### Checklist for Error Handling
- [ ] Standardized error format
- [ ] Error codes documented
- [ ] Clear error messages
- [ ] Details when applicable
- [ ] Correct status codes

### Checklist for Versioning
- [ ] Versioning strategy defined
- [ ] Current version documented
- [ ] Deprecation policy defined
- [ ] Migration documented
- [ ] Backward compatibility verified

### Checklist for Pagination
- [ ] Consistent pagination format
- [ ] Default limits documented
- [ ] Pagination headers implemented
- [ ] Total items available
- [ ] Navigation (next/prev) functional

### Checklist for Idempotence
- [ ] Non-idempotent operations identified
- [ ] Idempotency keys implemented
- [ ] Temporary response storage configured
- [ ] Timeout for keys defined
- [ ] Idempotence tests written

## Edge Cases

### API Requiring Authentication
**Situation:** Endpoints requiring authentication.
**Solution:** Define an authentication scheme (OAuth2, JWT, API Key).
**Exception:** Public endpoints should not require authentication.

```http
GET /users/me
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

### API with Asynchronous Operations
**Situation:** Operations taking time to complete.
**Solution:** Use polling or webhooks, return 202 Accepted.

```http
POST /reports/generate
Status: 202 Accepted
{
  "jobId": "abc123",
  "status": "processing",
  "pollUrl": "/jobs/abc123"
}
```

### API with Sensitive Data
**Situation:** Data requiring special protection.
**Solution:** Implement encryption in transit and at rest, mask sensitive data.

```json
{
  "creditCard": "****-****-****-1234",
  "email": "j***@example.com"
}
```

### API with Rate Limiting
**Situation:** Protecting the API from abuse.
**Solution:** Implement rate limiting with informative headers.

```http
HTTP/1.1 429 Too Many Requests
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1623456789
```

## References

- [REST API Design Rulebook](https://www.oreilly.com/library/view/rest-api-design/9781449317843/)
- [HTTP Status Codes](https://httpstatuses.com/)
- [JSON API Specification](https://jsonapi.org/)
- `documentation` — for API documentation
- `testing` — for contract testing
- `governance` — for review processes

## Completion Gate

A tarefa associada à skill `api-design` só pode ser declarada concluída quando:
1. Todas as verificações do checklist operacional foram atendidas.
2. O resultado foi validado deterministamente através de evidências de execução.
3. Não restam pendências estruturais, placeholders ou erros não tratados.

