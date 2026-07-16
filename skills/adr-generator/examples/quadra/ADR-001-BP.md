---
id: ADR-001-BP
type: bp
title: Blueprint - Implementação do JWT
created: 2026-01-01
updated: 2026-01-01
adr_ref: ADR-001
---

# Blueprint — ADR-001-BP: Implementação do JWT

> Referência: [ADR-001](./ADR-001.md)

## 1. Visão Geral (C4 Model - System Context / Container)

### Objetivo
Habilitar endpoints seguros via `Authorization: Bearer <token>`.

### Métricas de Sucesso
| Métrica | Antes | Depois | Status |
|---------|-------|--------|--------|
| Cobertura Autenticação | 0% | 100% dos endpoints privados protegidos | ⬜ |

## 2. Estrutura de Artefatos a Serem Alterados (C4 - Component/Code)
```text
src/auth/jwt_service.py
src/auth/middleware.py
tests/auth/test_jwt.py
```

## 3. Workflow de Execução (Visão Dinâmica)
### Workflow 1: Criar Serviço e Middleware
**Objetivo:** Assinar e validar tokens.
**Steps:**
1. Criar chaves ECDSA.
2. Implementar PyJWT adapter.
3. Criar Middleware ASGI.
