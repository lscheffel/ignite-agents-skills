# Example: REST CRUD Specification — Product Management

## Context

API for product catalog management in e-commerce. Backend: Express + TypeScript + PostgreSQL.

## Contract

### Resources

| Resource | URL | Method | Description |
|---------|-----|--------|-----------|
| Product | `/api/v1/products` | GET | List products (paginated) |
| Product | `/api/v1/products/:id` | GET | Product details |
| Product | `/api/v1/products` | POST | Create product |
| Product | `/api/v1/products/:id` | PUT | Update product completely |
| Product | `/api/v1/products/:id` | PATCH | Partial update |
| Product | `/api/v1/products/:id` | DELETE | Remove product |
| Categories | `/api/v1/products/:id/categories` | GET | List product categories |
| Categories | `/api/v1/products/:id/categories` | POST | Add category |

### Product Schema

```typescript
interface Product {
  id: string;           // UUID v4
  name: string;         // 3-200 characters
  description: string;  // max 5000 characters
  price: number;        // > 0, max 2 decimal places
  sku: string;          // unique, regex: ^[A-Z]{3}-\d{4}$
  status: 'active' | 'inactive' | 'draft';
  created_at: string;   // ISO 8601
  updated_at: string;   // ISO 8601
}
```

### Pagination

```
GET /api/v1/products?page=1&limit=20&sort=created_at&order=desc

Response Headers:
  X-Total-Count: 156
  X-Page-Count: 8
  Link: </api/v1/products?page=2&limit=20>; rel="next"
```

### Error Format (RFC 7807)

```json
{
  "type": "https://api.example.com/errors/validation",
  "title": "Invalid data",
  "status": 422,
  "detail": "The 'price' field must be greater than 0",
  "instance": "/api/v1/products",
  "errors": [
    {
      "field": "price",
      "message": "must be greater than 0",
      "rejected_value": -5
    }
  ]
}
```

### Status Codes

| Method | Success | Common Error |
|--------|---------|------------|
| GET | 200 OK | 404 Not Found |
| POST | 201 Created | 422 Unprocessable Entity |
| PUT | 200 OK | 404 Not Found, 422 Unprocessable |
| PATCH | 200 OK | 404 Not Found, 422 Unprocessable |
| DELETE | 204 No Content | 404 Not Found |

### Versioning

- URL path: `/api/v1/products`
- Accepted header: `Accept: application/vnd.api.v1+json`
- Breaking changes require new version (v2)
- Non-breaking changes (new fields) go to current version

### Idempotence

- PUT and DELETE are idempotent by design
- POST accepts `Idempotency-Key: <uuid>` header to prevent duplication
- Idempotency key expires after 24 hours

### Authentication

- Bearer token via `Authorization: Bearer <token>` header
- Rate limiting: 100 req/min per user
- Write endpoints require `admin` or `editor` role