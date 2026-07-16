# Example: Code Review Lite Session

> Exemplo de uso da skill `code-review-lite` para uma feature típica

---

## Cenário

**Feature:** Adicionar endpoint `/api/users/:id/profile` com cache Redis
**Commit:** `feat: add user profile endpoint with caching`
**Files Changed:** 5 files, ~280 lines

---

## Fase 1: Context Loading

```bash
# Changed files
git diff --name-only HEAD~1
# src/routes/user.ts
# src/services/user-service.ts
# src/middleware/cache.ts
# tests/user-profile.test.ts
# docs/api.md
```

**Task Reference:** ADR-023 (API Caching Strategy)
**Expected Behavior:** GET `/api/users/:id/profile` returns cached profile, 5min TTL
**Architectural Constraints:** 
- Cache layer via `src/middleware/cache.ts` (per ADR-023)
- No direct Redis calls in routes
- Error handling via `AppError` class

---

## Fase 2: Fast Review (5 Dimensions)

### 1. Plan Alignment ✅
- [x] Scope matches: endpoint + cache only
- [x] No gold-plating: no rate limiting, no auth changes

### 2. Obvious Bugs ⚠️
```typescript
// src/routes/user.ts:45 - POTENTIAL BUG
const profile = await userService.getProfile(userId); // Missing null check
return res.json(profile); // Could return null → 500
```
**Finding:** Missing null check on service return

### 3. Security Regression ✅
- [x] No secrets exposed
- [x] Input sanitized (userId validated via `:id` param middleware)
- [x] Auth check present (`requireAuth` middleware)
- [x] No injection vectors (parameterized query in service)

### 4. Architecture Drift ⚠️
```typescript
// src/services/user-service.ts:12 - DRIFT
import { redis } from '../config/redis'; // Direct Redis import!
```
**Finding:** Violates ADR-023 — should use `cacheMiddleware` abstraction

### 5. Testing ⚠️
- [x] Unit tests for service exist
- [ ] **Missing:** Integration test for cache hit/miss
- [x] Existing tests pass

---

## Output

```
REQUIRES_FIXES

Blocking Issues:
1. src/routes/user.ts:45 — Missing null check on service return (potential 500)
2. src/services/user-service.ts:12 — Direct Redis import violates ADR-023 cache abstraction

Warnings:
- Missing integration test for cache hit/miss scenarios

Escalation: Not triggered (no auth/payment/infra/api/db/schema/lockfile changes)
```

---

## Fixes Applied

```typescript
// Fix 1: Null check
const profile = await userService.getProfile(userId);
if (!profile) return res.status(404).json({ error: 'Not found' });
return res.json(profile);

// Fix 2: Use cache abstraction
// Remove: import { redis } from '../config/redis';
// Use: cacheMiddleware.get/set in route handler
```

---

## Re-review

```
APPROVED

All blocking issues fixed. Cache abstraction respected. Tests pass.
```

---

*Exemplo: `skills/code-review-lite/examples/review-session.md`*