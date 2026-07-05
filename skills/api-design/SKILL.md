---
name: api-design
description: Guia completo para design de APIs RESTful e GraphQL. Define padrões para endpoints, versionamento, contratos de erro, paginação e idempotência. Use quando projetar novas APIs, revisar contratos existentes ou padronizar práticas de design de interface.
version: 2.0.0
tags: [api, rest, graphql, endpoints, versioning]
related_skills: [documentation, testing, governance]
---

# API Design

Guia para design de APIs robustas, consistentes e escaláveis.

## Quando Usar

### Use quando:
- Precisa projetar novos endpoints
- Precisa definir contrato de API
- Precisa implementar versionamento
- Precisa padronizar tratamento de erros
- Precisa revisar API existente

### Não use quando:
- Protótipo rápido sem contratos formais
- API interna entre serviços do mesmo time
- SDK já existe e está bem definido

### Skills relacionadas:
- `documentation` — para documentação de API
- `testing` — para testes de contrato
- `governance` — para processos de review

## Decision Tree

```mermaid
graph TD
    A[Precisa expor dados?] -->|Sim| B[API pública?]
    A -->|Não| C[Use mensageria]
    B -->|Sim| D[REST ou GraphQL?]
    B -->|Não| E[API interna]
    D -->|CRUD simples| F[REST]
    D -->|Consultas complexas| G[GraphQL]
    F --> H[Definir endpoints CRUD]
    H --> I[Versionamento]
    I --> J[Formato de erro]
    J --> K[ paginação]
    K --> L[Idempotência]
    L --> M[API Pronta]
    G --> N[Schema GraphQL]
    N --> O[Resolvers]
    O --> I
```

## Conceitos Fundamentais

### RESTful Design

API baseada em recursos HTTP.

- **Recursos** representam entidades
- **Métodos** definem ações
- **Status codes** comunicam resultado

```
GET    /users         → Listar usuários
POST   /users         → Criar usuário
GET    /users/{id}    → Obter usuário
PUT    /users/{id}    → Atualizar usuário
DELETE /users/{id}    → Deletar usuário
```

### Idempotência

Operações que produzem mesmo resultado mesmo que executadas múltiplas vezes.

- **Idempotente**: GET, PUT, DELETE
- **Não idempotente**: POST, PATCH (por padrão)
- **Seguro**: GET, HEAD, OPTIONS

### Versionamento

Estratégias para evoluir API sem quebrar clientes.

- **URL path**: `/v1/users` (recomendado)
- **Header**: `Accept: application/vnd.api.v1+json`
- **Query param**: `/users?version=1`

### Contrato de API

Acordo formal sobre formato de dados.

- Request/Response schema
- Códigos de erro
- Formatação de datas
- Paginação

## Workflow

### Fase 1: Definir Recursos

1. Identifique entidades do domínio:
   ```bash
   # Listar entidades do modelo
   grep -r "model\|entity" src/
   ```
2. Crie mapeamento recurso-URL:
   ```
   /users          → User
   /orders         → Order
   /products       → Product
   ```
3. Defina relacionamentos:
   ```
   /users/{id}/orders   → Orders do user
   /orders/{id}/items   → Items da order
   ```
4. **Checkpoint**: Lista de recursos aprovada

### Fase 2: Especificar Endpoints

1. Para cada recurso, defina operações:
   ```yaml
   /users:
     get:
       summary: Listar usuários
       parameters:
         - name: page
           in: query
           schema:
             type: integer
             default: 1
       responses:
         200:
           description: Lista de usuários
   ```
2. Use template `templates/endpoint-spec.md`
3. Documente request/response
4. **Checkpoint**: Especificação completa

### Fase 3: Definir Tratamento de Erros

1. Crie contrato de erro padronizado:
   ```json
   {
     "error": {
       "code": "VALIDATION_ERROR",
       "message": "Email inválido",
       "details": [
         {
           "field": "email",
           "message": "Formato inválido"
         }
       ]
     }
   }
   ```
2. Use template `templates/error-contract.md`
3. Mapeie códigos HTTP para erros
4. **Checkpoint**: Contrato de erro definido

### Fase 4: Implementar Versionamento

1. Escolha estratégia de versionamento:
   ```bash
   # Recomendado: URL path
   /v1/users
   /v2/users
   ```
2. Use template `templates/api-versioning.md`
3. Defina política de depreciação
4. **Checkpoint**: Versionamento funcionando

### Fase 5: Adicionar Paginação

1. Implemente paginação consistente:
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
2. Defina limites padrão
3. Adicione headers de paginação
4. **Checkpoint**: Paginação testada

### Fase 6: Garantir Idempotência

1. Identifique operações não idempotentes
2. Implemente chaves de idempotência:
   ```http
   POST /payments
   Idempotency-Key: 550e8400-e29b-41d4-a716-446655440000
   ```
3. Armazene respostas temporárias
4. **Checkpoint**: Idempotência verificada

## Templates

### endpoint-spec.md
Localização: `templates/endpoint-spec.md`

Template para especificação de endpoint.

**Uso:**
```bash
cp templates/endpoint-spec.md docs/api/users.md
```

### error-contract.md
Localização: `templates/error-contract.md`

Template para contrato de erro.

**Uso:**
```bash
cp templates/error-contract.md docs/api/errors.md
```

### api-versioning.md
Localização: `templates/api-versioning.md`

Template para versionamento de API.

**Uso:**
```bash
cp templates/api-versioning.md docs/api/versioning.md
```

## Anti-patterns

### 🔴 Crítico

#### Endpoint sem Tratamento de Erro Consistente
**O que é:** Endpoints que retornam erros em formatos diferentes.
**Por que é ruim:** Clientes não conseguem tratar erros programaticamente.
**Como evitar:** Use contrato de erro padronizado em todos endpoints.
**Exemplo:**
```
# ❌ ERRADO
GET /users/999
{ "msg": "user not found" }

GET /orders/999
Status: 404 Not Found
# Sem body

# ✅ CORRETO
GET /users/999
{
  "error": {
    "code": "NOT_FOUND",
    "message": "User not found",
    "details": [{"field": "id", "message": "User with id 999 does not exist"}]
  }
}
```

#### PUT sem Idempotência
**O que é:** PUT que cria recursos duplicados em chamadas repetidas.
**Por que é ruim:** Viola contrato REST, causa inconsistências.
**Como evitar:** PUT deve ser idempotente, use POST para criação.
**Exemplo:**
```
# ❌ ERRADO
PUT /users
{ "name": "John" }
# Cria novo user a cada chamada

# ✅ CORRETO
PUT /users/123
{ "name": "John" }
# Atualiza user existente, idempotente
```

### 🟡 Médio

#### POST para Operações de Leitura
**O que é:** Usar POST para buscar dados.
**Por que é ruim:** Confunde semântica HTTP, dificulta cache.
**Como evitar:** Use GET para leitura, POST para criação.
**Exemplo:**
```
# ❌ ERRADO
POST /search
{ "query": "users" }

# ✅ CORRETO
GET /users?q=users
# ou
GET /search?q=users
```

#### Versionamento Quebrando Clientes
**O que é:** Mudanças incompatíveis sem nova versão.
**Por que é ruim:** Quebra clientes existentes.
**Como evitar:** Use versionamento, mantenha backward compatibility.
**Exemplo:**
```
# ❌ ERRADO
# v1: GET /users retorna { "name": "John" }
# v2: GET /users retorna { "fullName": "John" }
# Sem migração

# ✅ CORRETO
# v1: GET /users retorna { "name": "John" }
# v2: GET /users retorna { "fullName": "John", "name": "John" }
# Mantém compatibilidade
```

### 🟢 Baixo

#### Query Params Opcionais sem Default
**O que é:** Parâmetros sem valor padrão definido.
**Por que é ruim:** Comportamento imprevisível, diferentes clientes podem ter diferentes comportamentos.
**Como evitar:** Sempre defina valores padrão para parâmetros opcionais.
**Exemplo:**
```
# ❌ ERRADO
GET /users?page=&limit=

# ✅ CORRETO
GET /users?page=1&limit=20
# Ou documente que omitir usa defaults: page=1, limit=20
```

## Checklists

### Checklist de Design de Endpoint
- [ ] Recurso identificado claramente
- [ ] Método HTTP correto (GET, POST, PUT, DELETE)
- [ ] Path naming consistente (kebab-case ou camelCase)
- [ ] Parâmetros documentados
- [ ] Request body definido
- [ ] Responses definidos (200, 201, 204, 400, 404, 500)
- [ ] Headers necessários listados

### Checklist de Tratamento de Erros
- [ ] Formato de erro padronizado
- [ ] Códigos de erro documentados
- [ ] Mensagens de erro claras
- [ ] Details quando aplicável
- [ ] Status codes corretos

### Checklist de Versionamento
- [ ] Estratégia de versionamento definida
- [ ] Versão atual documentada
- [ ] Política de depreciação definida
- [ ] Migração documentada
- [ ] Compatibilidade backward verificada

### Checklist de Paginação
- [ ] Formato de paginação definido
- [ ] Limites padrão documentados
- [ ] Headers de paginação implementados
- [ ] Total items disponível
- [ ] Navegação (next/prev) funcional

### Checklist de Idempotência
- [ ] Operações idempotentes identificadas
- [ ] Chaves de idempotência implementadas
- [ ] Armazenamento temporário configurado
- [ ] Timeout de chaves definido
- [ ] Testes de idempotência escritos

## Edge Cases

### API que Precisa de Autenticação
**Situação:** Endpoints que requerem autenticação.
**Solução:** Defina scheme de autenticação (OAuth2, JWT, API Key).
**Exceção:** Endpoints públicos não devem requerer autenticação.

```http
GET /users/me
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

### API com Operações Assíncronas
**Situação:** Operações que levam tempo para completar.
**Solução:** Use polling ou webhooks, retorne 202 Accepted.

```http
POST /reports/generate
Status: 202 Accepted
{
  "jobId": "abc123",
  "status": "processing",
  "pollUrl": "/jobs/abc123"
}
```

### API com Dados Sensíveis
**Situação:** Dados que precisam de proteção especial.
**Solução:** Implemente criptografia em trânsito e repouso, mascare dados sensíveis.

```json
{
  "creditCard": "****-****-****-1234",
  "email": "j***@example.com"
}
```

### API com Rate Limiting
**Situação:** Proteger API de abuso.
**Solução:** Implemente rate limiting com headers informativos.

```http
HTTP/1.1 429 Too Many Requests
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1623456789
```

## Referências

- [REST API Design Rulebook](https://www.oreilly.com/library/view/rest-api-design/9781449317843/)
- [HTTP Status Codes](https://httpstatuses.com/)
- [JSON API Specification](https://jsonapi.org/)
- `documentation` — para documentação de API
- `testing` — para testes de contrato
- `governance` — para processos de review
