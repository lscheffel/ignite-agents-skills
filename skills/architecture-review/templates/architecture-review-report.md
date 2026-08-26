# Architecture Review Report Template

## Executive Summary

{Summary in 3-5 lines of what was reviewed and main findings}

## Scope

- **Repository:** {repository name}
- **Branch:** {analyzed branch}
- **Date:** {review date}
- **Reviewer:** {reviewer name}

## Findings by Severity

### 🔴 Critical

| File | Issue | Suggestion |
|------|-------|------------|
| src/... | ... | ... |

### 🟡 Medium

| File | Issue | Suggestion |
|------|-------|------------|
| src/... | ... | ... |

### 🟢 Low

| File | Issue | Suggestion |
|------|-------|------------|
| src/... | ... | ... |

## Adherence Score

| Standard | Score | Comment |
|----------|-------|----------|
| SOLID | 85% | SRP violated in UserService |
| Clean Architecture | 70% | Domain depends on Express |
| DDD | 90% | Aggregates well defined |

## Recommendations

1. **Short-term (1-2 sprints):**
   - {action 1}
   - {action 2}

2. **Medium-term (1-3 months):**
   - {action 3}
   - {action 4}

3. **Long-term (3+ months):**
   - {action 5}

## Next Steps

- [ ] Create issues for each critical finding
- [ ] Schedule refinement session
- [ ] Update architectural documentation