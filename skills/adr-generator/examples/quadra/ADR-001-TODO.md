---
id: ADR-001-TODO
type: todo
title: Execução - Implementação do JWT
created: 2026-01-01
updated: 2026-01-01
adr_ref: ADR-001
---

# ADR-001-TODO: Execução - Implementação do JWT

> Referência: [ADR-001](./ADR-001.md) | Status: ⬜ PENDENTE

## Fase A: Core Authentication

### A1: Criação do JWT Service

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| A1.1 | Criar JWT Adapter com PyJWT | ⬜ | 🔴 | — | 4h |
| A1.2 | Implementar Auth Middleware | ⬜ | 🔴 | A1.1 | 3h |

**Checkpoint A1:**
- [ ] PyJWT instalado.
- [ ] Endpoints retornando 401 para requests sem token.
