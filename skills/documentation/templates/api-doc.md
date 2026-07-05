# API Documentation Template

## Endpoints

### GET /users

Retorna lista de usuários.

**Response:**
```json
[
  {
    "id": "1",
    "name": "John",
    "email": "john@example.com"
  }
]
```

**Errors:**
- 401: Unauthorized
- 500: Internal Server Error

### POST /users

Cria usuário.

**Request:**
```json
{
  "name": "John",
  "email": "john@example.com"
}
```

**Response:**
```json
{
  "id": "1",
  "name": "John",
  "email": "john@example.com"
}
```