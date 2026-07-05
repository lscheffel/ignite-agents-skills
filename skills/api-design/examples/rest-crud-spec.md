# Exemplo: Especificação REST CRUD — Gestão de Produtos

## Contexto

API para gestão de catálogo de produtos em e-commerce. Backend: Express + TypeScript + PostgreSQL.

## Contrato

### Recursos

| Recurso | URL | Método | Descrição |
|---------|-----|--------|-----------|
| Produto | `/api/v1/products` | GET | Lista produtos (paginado) |
| Produto | `/api/v1/products/:id` | GET | Detalhes de um produto |
| Produto | `/api/v1/products` | POST | Cria produto |
| Produto | `/api/v1/products/:id` | PUT | Atualiza produto completo |
| Produto | `/api/v1/products/:id` | PATCH | Atualização parcial |
| Produto | `/api/v1/products/:id` | DELETE | Remove produto |
| Categorias | `/api/v1/products/:id/categories` | GET | Lista categorias do produto |
| Categorias | `/api/v1/products/:id/categories` | POST | Adiciona categoria |

### Schema do Produto

```typescript
interface Product {
  id: string;           // UUID v4
  name: string;         // 3-200 caracteres
  description: string;  // máx 5000 caracteres
  price: number;        // > 0, máx 2 casas decimais
  sku: string;          // único, regex: ^[A-Z]{3}-\d{4}$
  status: 'active' | 'inactive' | 'draft';
  created_at: string;   // ISO 8601
  updated_at: string;   // ISO 8601
}
```

### Paginação

```
GET /api/v1/products?page=1&limit=20&sort=created_at&order=desc

Response Headers:
  X-Total-Count: 156
  X-Page-Count: 8
  Link: </api/v1/products?page=2&limit=20>; rel="next"
```

### Formato de Erro (RFC 7807)

```json
{
  "type": "https://api.example.com/errors/validation",
  "title": "Dados inválidos",
  "status": 422,
  "detail": "O campo 'price' deve ser maior que 0",
  "instance": "/api/v1/products",
  "errors": [
    {
      "field": "price",
      "message": "deve ser maior que 0",
      "rejected_value": -5
    }
  ]
}
```

### Status Codes

| Método | Sucesso | Erro Comum |
|--------|---------|------------|
| GET | 200 OK | 404 Not Found |
| POST | 201 Created | 422 Unprocessable Entity |
| PUT | 200 OK | 404 Not Found, 422 Unprocessable |
| PATCH | 200 OK | 404 Not Found, 422 Unprocessable |
| DELETE | 204 No Content | 404 Not Found |

### Versionamento

- URL path: `/api/v1/products`
- Header aceito: `Accept: application/vnd.api.v1+json`
- Breaking changes requerem nova versão (v2)
- Non-breaking changes (campos novos) vão para versão atual

### Idempotência

- PUT e DELETE são idempotentes por design
- POST aceita header `Idempotency-Key: <uuid>` para prevenir duplicação
- Chave de idempotência expira após 24h

### Autenticação

- Bearer token via header `Authorization: Bearer <token>`
- Rate limiting: 100 req/min por usuário
- Endpoints de escrita requerem role `admin` ou `editor`
