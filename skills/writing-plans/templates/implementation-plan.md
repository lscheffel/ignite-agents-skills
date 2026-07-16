# Implementation Plan (PI) Template

> Plano de Implementação Nível Enterprise — derivado de ADR aprovada

---

# ADR-XXX: [Título da ADR]

## Implementation Plan

**ADR Referência:** `docs/adr/ADR-XXX.md`
**Blueprint:** `docs/adr/ADR-XXX-BP.md`
**TODO:** `docs/adr/ADR-XXX-TODO.md`
**Data:** {{DATE}}
**Autor:** {{AUTHOR}}

---

## 1. Visão Geral

### Objetivo
{{OBJETIVO}}

### Escopo
- **Incluso:** {{INCLUSO}}
- **Fora de Escopo:** {{FORA_DE_ESCOPO}}

### Constraints Arquiteturais
- {{CONSTRAINT_1}}
- {{CONSTRAINT_2}}

### Dependências
- {{DEPENDENCIA_1}}
- {{DEPENDENCIA_2}}

---

## 2. Tasks (Ordenadas por Dependência)

### Fase 1: {{FASE_1_NOME}}

#### Task 1.1: {{TASK_1_1_DESC}}
- **Arquivos:** `{{FILE_1}}`, `{{FILE_2}}`
- **Validação:** `{{VALIDATION_CMD}}`
- **Teste:** `{{TEST_DESC}}`
- **Rollback:** `git checkout HEAD -- {{FILE_1}} {{FILE_2}}`

#### Task 1.2: {{TASK_1_2_DESC}}
- **Arquivos:** `{{FILE_3}}`
- **Validação:** `{{VALIDATION_CMD}}`
- **Teste:** `{{TEST_DESC}}`
- **Rollback:** `git checkout HEAD -- {{FILE_3}}`

### Fase 2: {{FASE_2_NOME}}

#### Task 2.1: {{TASK_2_1_DESC}}
- **Arquivos:** `{{FILE_4}}`
- **Validação:** `{{VALIDATION_CMD}}`
- **Teste:** `{{TEST_DESC}}`
- **Rollback:** `git checkout HEAD -- {{FILE_4}}`

---

## 3. Mapeamento Task → Arquivos

| Task | Arquivos | Tipo |
|------|----------|------|
| 1.1 | `src/...`, `tests/...` | Implementation + Test |
| 1.2 | `src/...` | Implementation |
| 2.1 | `docs/...`, `src/...` | Docs + Implementation |

---

## 4. Test Strategy

### Unit Tests (por Task)
- Task 1.1: `tests/unit/{{MODULE}}.test.ts` — coverage ≥ 80%
- Task 1.2: `tests/unit/{{MODULE}}.test.ts` — coverage ≥ 80%

### Integration Tests
- `tests/integration/{{FEATURE}}.test.ts` — fluxo completo

### E2E Tests
- `tests/e2e/{{FEATURE}}.test.ts` — critical path

### TDD Order
1. Escrever teste falhando
2. Implementar código mínimo
3. Passar teste
4. Refatorar

---

## 5. Rollback Plan

| Task | Rollback Command | Verification |
|------|------------------|--------------|
| 1.1 | `git revert {{COMMIT_1_1}}` | `npm test` passes |
| 1.2 | `git revert {{COMMIT_1_2}}` | `npm test` passes |
| 2.1 | `git revert {{COMMIT_2_1}}` | `npm test` passes |

**Full Rollback:** `git reset --hard {{BASE_COMMIT}}`

---

## 6. Edge Cases

| Cenário | Tratamento | Task Relacionada |
|---------|------------|------------------|
| {{EDGE_1}} | {{HANDLING_1}} | 1.1 |
| {{EDGE_2}} | {{HANDLING_2}} | 1.2 |
| {{EDGE_3}} | {{HANDLING_3}} | 2.1 |

---

## 7. Validação Final

- [ ] Todas tasks validadas com comandos especificados
- [ ] Testes unitários passando (coverage ≥ 80%)
- [ ] Testes integração passando
- [ ] Testes E2E passando
- [ ] Lint/TypeCheck limpo
- [ ] Documentação atualizada
- [ ] TODO sincronizado (todas `[x]`)

---

*Template: `skills/writing-plans/templates/implementation-plan.md`*