# Example: Writing Plans — Feature Breakdown

> Exemplo de criação de Implementation Plan (PI) para feature de autenticação social

---

## Cenário

**Feature:** Login com Google OAuth 2.0
**ADR:** ADR-015 (Social Authentication Strategy)
**Tipo:** Nova feature, Tier 2 (Zen-Mode Quadra)

---

## Fase 1: ADR + Blueprint + TODO (Pré-requisito)

Já existem:
- `docs/adr/ADR-015.md` — Decisão: Google OAuth, JWT tokens, refresh rotation
- `docs/adr/ADR-015-BP.md` — 3 fases: Config, Auth Flow, Token Management
- `docs/adr/ADR-015-TODO.md` — 12 tasks mapeadas

---

## Fase 2: Gerar PI (Implementation Plan)

**Arquivo:** `docs/adr/ADR-015-PI.md`

```markdown
# ADR-015: Social Authentication — Implementation Plan

## 1. Visão Geral
**Objetivo:** Implementar login Google OAuth 2.0 com JWT + refresh rotation
**ADR:** docs/adr/ADR-015.md
**Blueprint:** docs/adr/ADR-015-BP.md

## 2. Tasks

### Fase 1: Configuração Google Cloud

#### Task 1.1: Criar OAuth Client no Google Cloud Console
- **Arquivos:** `docs/google-oauth-setup.md` (doc interno)
- **Validação:** Client ID/Secret gerados
- **Teste:** N/A (manual)
- **Rollback:** Deletar client no console

#### Task 1.2: Adicionar env vars
- **Arquivos:** `.env.example`, `.env.local`
- **Validação:** `grep GOOGLE_CLIENT_ID .env.local`
- **Teste:** N/A
- **Rollback:** `git checkout HEAD -- .env.example .env.local`

### Fase 2: Auth Flow

#### Task 2.1: Instalar dependências
- **Arquivos:** `package.json`, `pnpm-lock.yaml`
- **Validação:** `pnpm install && pnpm audit`
- **Teste:** N/A
- **Rollback:** `git checkout HEAD -- package.json pnpm-lock.yaml`

#### Task 2.2: Implementar Google Strategy (Passport)
- **Arquivos:** `src/auth/strategies/google.strategy.ts`
- **Validação:** `npm run typecheck`
- **Teste:** `tests/unit/auth/google.strategy.test.ts`
- **Rollback:** `git checkout HEAD -- src/auth/strategies/google.strategy.ts`

#### Task 2.3: Criar rotas /auth/google e /auth/google/callback
- **Arquivos:** `src/routes/auth.ts`
- **Validação:** `curl -I http://localhost:3000/auth/google` → 302
- **Teste:** `tests/integration/auth/google-oauth.test.ts`
- **Rollback:** `git checkout HEAD -- src/routes/auth.ts`

#### Task 2.4: Implementar callback handler + user upsert
- **Arquivos:** `src/services/auth.service.ts`, `src/repositories/user.repository.ts`
- **Validação:** `npm run typecheck && npm test`
- **Teste:** `tests/unit/auth/auth.service.test.ts`
- **Rollback:** `git checkout HEAD -- src/services/auth.service.ts src/repositories/user.repository.ts`

### Fase 3: Token Management

#### Task 3.1: JWT Access Token (15min) + Refresh Token (7d)
- **Arquivos:** `src/utils/jwt.ts`
- **Validação:** `npm run typecheck`
- **Teste:** `tests/unit/utils/jwt.test.ts`
- **Rollback:** `git checkout HEAD -- src/utils/jwt.ts`

#### Task 3.2: Refresh Rotation Endpoint
- **Arquivos:** `src/routes/auth.ts` (add `/auth/refresh`)
- **Validação:** `curl -X POST /auth/refresh` → new access token
- **Teste:** `tests/integration/auth/refresh.test.ts`
- **Rollback:** `git checkout HEAD -- src/routes/auth.ts`

#### Task 3.3: Logout + Revoke Refresh Token
- **Arquivos:** `src/services/auth.service.ts`, `src/routes/auth.ts`
- **Validação:** `npm test`
- **Teste:** `tests/integration/auth/logout.test.ts`
- **Rollback:** `git checkout HEAD -- src/services/auth.service.ts src/routes/auth.ts`

## 3. Mapeamento Task → Arquivos

| Task | Arquivos | Tipo |
|------|----------|------|
| 1.1 | `docs/google-oauth-setup.md` | Doc |
| 1.2 | `.env.example`, `.env.local` | Config |
| 2.1 | `package.json`, `pnpm-lock.yaml` | Deps |
| 2.2 | `src/auth/strategies/google.strategy.ts` | Impl + Test |
| 2.3 | `src/routes/auth.ts` | Impl + Test |
| 2.4 | `src/services/auth.service.ts`, `src/repositories/user.repository.ts` | Impl + Test |
| 3.1 | `src/utils/jwt.ts` | Impl + Test |
| 3.2 | `src/routes/auth.ts` | Impl + Test |
| 3.3 | `src/services/auth.service.ts`, `src/routes/auth.ts` | Impl + Test |

## 4. Test Strategy

### Unit (por task)
- 2.2: Strategy config validation
- 2.4: User upsert logic (new vs existing)
- 3.1: Token generation/validation, expiry

### Integration
- 2.3: Full OAuth flow (mock Google)
- 3.2: Refresh rotation (new access + new refresh)
- 3.3: Logout revokes refresh

### E2E
- Happy path: Login → Access protected → Refresh → Logout
- Edge: Expired refresh → re-login required

## 5. Rollback Plan

| Task | Rollback | Verification |
|------|----------|--------------|
| 1.1 | Delete Google Client | N/A |
| 1.2 | `git checkout HEAD -- .env*` | `grep` fails |
| 2.1 | `git checkout HEAD -- package.json pnpm-lock.yaml` | `pnpm install` |
| 2.2 | `git checkout HEAD -- google.strategy.ts` | Tests pass |
| 2.3 | `git checkout HEAD -- auth.ts` (routes) | Tests pass |
| 2.4 | `git checkout HEAD -- auth.service.ts user.repository.ts` | Tests pass |
| 3.1 | `git checkout HEAD -- jwt.ts` | Tests pass |
| 3.2 | `git checkout HEAD -- auth.ts` (routes) | Tests pass |
| 3.3 | `git checkout HEAD -- auth.service.ts auth.ts` | Tests pass |

## 6. Edge Cases

| Cenário | Tratamento | Task |
|---------|------------|------|
| Google retorna email não verificado | Rejeitar login, logar warning | 2.4 |
| Usuário já existe com email (local auth) | Link accounts, merge profiles | 2.4 |
| Refresh token roubado (reuse detection) | Revoke all user sessions, alert | 3.2 |
| Clock skew entre servers | Leeway 60s na validação JWT | 3.1 |
| Rate limit Google API | Exponential backoff, circuit breaker | 2.2 |

## 7. Validação Final

- [x] Tasks 1.1-3.3 validadas
- [x] Unit tests: 15 passing, coverage 87%
- [x] Integration tests: 8 passing
- [x] E2E tests: 3 passing
- [x] Lint/TypeCheck clean
- [x] Docs: `docs/api.md` atualizado
- [x] TODO sincronizado: 12/12 `[x]`
```

---

## Fase 3: Atualizar TODO

**Arquivo:** `docs/adr/ADR-015-TODO.md`

```markdown
## Fase 1: Configuração Google Cloud

- [x] Task 1.1: Criar OAuth Client no Google Cloud Console | Validação: Client ID/Secret gerados
- [x] Task 1.2: Adicionar env vars | Validação: `grep GOOGLE_CLIENT_ID .env.local`

## Fase 2: Auth Flow

- [x] Task 2.1: Instalar dependências | Validação: `pnpm install && pnpm audit`
- [x] Task 2.2: Google Strategy (Passport) | Validação: `npm run typecheck` | Teste: `tests/unit/auth/google.strategy.test.ts`
- [x] Task 2.3: Rotas /auth/google e callback | Validação: `curl -I /auth/google` → 302 | Teste: `tests/integration/auth/google-oauth.test.ts`
- [x] Task 2.4: Callback handler + user upsert | Validação: `npm test` | Teste: `tests/unit/auth/auth.service.test.ts`

## Fase 3: Token Management

- [x] Task 3.1: JWT Access (15min) + Refresh (7d) | Validação: `npm run typecheck` | Teste: `tests/unit/utils/jwt.test.ts`
- [x] Task 3.2: Refresh Rotation Endpoint | Validação: `curl -X POST /auth/refresh` | Teste: `tests/integration/auth/refresh.test.ts`
- [x] Task 3.3: Logout + Revoke Refresh | Validação: `npm test` | Teste: `tests/integration/auth/logout.test.ts`
```

---

## Fase 4: Entrega

Plano aprovado → Invocar skill `implementation` para execução.

---

*Exemplo: `skills/writing-plans/examples/social-auth-plan.md`*