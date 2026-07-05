# Exemplo: Plano de Implementação — Migração de API v1 para v2

## Contexto

Sistema legado expõe API REST v1 sem versionamento formal. Precisa migrar para v2 com:
- Versionamento por URL path (`/api/v1/` → `/api/v2/`)
- Contrato de erro padronizado (RFC 7807)
- Depreciação progressiva dos endpoints v1

## Especificação

- Backend: Express.js + TypeScript
- 12 endpoints v1 ativos
- 3 clientes dependentes (web, mobile, parceiro)
- Prazo: 2 semanas

## Plano de Implementação

### Fase 1: Fundação (3 dias)

| Tarefa | Arquivos | Critérios de Aceitação | Complexidade |
|--------|----------|----------------------|--------------|
| 1.1 Criar estrutura `/api/v2/` | `src/routes/v2/`, `src/middleware/versioning.ts` | Pasta existe, middleware registra versão | S |
| 1.2 Definir contrato de erro v2 | `src/types/error.ts`, `src/middleware/error-handler.ts` | Error response segue RFC 7807 | S |
| 1.3 Configurar roteador por versão | `src/app.ts` | `/api/v1/` e `/api/v2/` respondem independentemente | M |

**Dependências:** Nenhuma
**Estimativa:** 8h

### Fase 2: Migração (5 dias)

| Tarefa | Arquivos | Critérios de Aceitação | Complexidade |
|--------|----------|----------------------|--------------|
| 2.1 Migrar endpoints CRUD (4) | `src/routes/v2/users.ts`, `products.ts`, `orders.ts`, `categories.ts` | Todos respondem com contrato v2 | M |
| 2.2 Migrar endpoints de negócio (5) | `src/routes/v2/auth.ts`, `payments.ts`, `reports.ts`, `search.ts`, `webhooks.ts` | Lógica preservada, contratos atualizados | L |
| 2.3 Migrar endpoints admin (3) | `src/routes/v2/admin.ts`, `audit.ts`, `config.ts` | Acesso restrito mantido | M |
| 2.4 Adicionar headers de depreciação | `src/middleware/deprecation.ts` | Headers `Deprecation: true` e `Sunset: <date>` nos endpoints v1 | S |

**Dependências:** Fase 1 completa
**Estimativa:** 16h

### Fase 3: Validação (2 dias)

| Tarefa | Arquivos | Critérios de Aceitação | Complexidade |
|--------|----------|----------------------|--------------|
| 3.1 Testes de contrato v2 | `tests/v2/contract/` | 100% dos endpoints v2 têm teste de contrato | M |
| 3.2 Testes de compatibilidade v1 | `tests/v1/compatibility/` | Endpoints v1 continuam respondendo | M |
| 3.3 Testes de migração | `tests/migration/` | Cenário completo v1→v2 sem perda de dados | M |

**Dependências:** Fase 2 completa
**Estimativa:** 8h

### Fase 4: Deploy (2 dias)

| Tarefa | Arquivos | Critérios de Aceitação | Complexidade |
|--------|----------|----------------------|--------------|
| 4.1 Feature flag para v2 | `src/config/flags.ts` | v2 acessível via header `X-API-Version: 2` | S |
| 4.2 Deploy canário | `docker-compose.yml`, `k8s/` | 10% do tráfego vai para v2 | M |
| 4.3 Monitoramento pós-deploy | `src/middleware/metrics.ts` | Métricas de erro comparadas v1 vs v2 | S |

**Dependências:** Fase 3 completa
**Estimativa:** 8h

## DAG de Dependências

```
1.1 → 1.2 → 1.3 → 2.1 → 2.2 → 2.3 → 2.4 → 3.1 → 3.2 → 3.3 → 4.1 → 4.2 → 4.3
```

## Estimativa Total

| Fase | Horas | Dias |
|------|-------|------|
| Fundação | 8h | 3 |
| Migração | 16h | 5 |
| Validação | 8h | 2 |
| Deploy | 8h | 2 |
| **Total** | **40h** | **2 semanas** |

## Riscos

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| Clientes quebram com mudança de contrato | Alto | Headers de depreciação + sunset de 30 dias |
| Regressão em endpoints v1 | Alto | Testes de compatibilidade obrigatórios |
| Dados inconsistentes entre v1/v2 | Médio | Feature flag + deploy canário |
