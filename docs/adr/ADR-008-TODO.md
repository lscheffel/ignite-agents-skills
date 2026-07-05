# TODO: Ultra-Avaliação v2.0.3 — Correção de Débitos Estruturais

> ADR-008 | Início: 2026-07-05 | Conclusão: 2026-07-05 | Status: ✅ CONCLUÍDO (8/9 débitos)

---

## Legenda

- ⬜ Pendente
- 🔄 Em Andamento
- ✅ Concluído
- ❌ Bloqueado
- ⏸️ Pausado

**Prioridade:** 🔴 Alta | 🟡 Média | 🟢 Baixa

---

## Fase 1: Bugs de CI e Links Mortos (~1h)

### F1.1: Corrigir `((WARNINGS++))` em validate-skill.sh [D-001]

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| F1.1.1 | Substituir `((ERRORS++))` por `ERRORS=$((ERRORS + 1))` na linha 18 | ⬜ | 🔴 | — | 2min |
| F1.1.2 | Substituir `((WARNINGS++))` por `WARNINGS=$((WARNINGS + 1))` na linha 24 | ⬜ | 🔴 | — | 2min |
| F1.1.3 | Testar com skill que gera warning (ex: writing-plans sem examples/) | ⬜ | 🔴 | F1.1.1, F1.1.2 | 5min |
| F1.1.4 | Verificar que resumo é impresso e exit code = 0 | ⬜ | 🔴 | F1.1.3 | 3min |
| F1.1.5 | Rodar em todas as 22 skills e verificar que nenhuma morre | ⬜ | 🟡 | F1.1.4 | 5min |

**Checkpoint F1.1:**
- [ ] `((ERRORS++))` → `ERRORS=$((ERRORS + 1))`
- [ ] `((WARNINGS++))` → `WARNINGS=$((WARNINGS + 1))`
- [ ] Script roda todos os 10 checks mesmo com warnings
- [ ] Exit code = 0 com warnings, 1 com errors

---

### F1.2: Corrigir links quebrados para ADRs arquivadas [D-002]

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| F1.2.1 | Corrigir link ADR-005 em implementation/SKILL.md L401 | ⬜ | 🔴 | — | 1min |
| F1.2.2 | Corrigir link ADR-005-BP em implementation/SKILL.md L402 | ⬜ | 🔴 | — | 1min |
| F1.2.3 | Corrigir link ADR-002 em implementation/SKILL.md L403 | ⬜ | 🔴 | — | 1min |
| F1.2.4 | Corrigir link ADR-007 em agents-md-generator/SKILL.md L292 | ⬜ | 🔴 | — | 1min |
| F1.2.5 | Verificar que zero links apontam para path sem archive/ | ⬜ | 🔴 | F1.2.1-F1.2.4 | 3min |

**Checkpoint F1.2:**
- [ ] Todos os 4 links corrigidos para `../../docs/adr/archive/ADR-XXX.md`
- [ ] `grep -rn '../../docs/adr/ADR-' skills/ | grep -v archive` retorna ZERO

---

**Checkpoint Geral Fase 1:**
- [ ] F1.1 e F1.2 concluídas
- [ ] `validate-skill.sh` funciona corretamente
- [ ] Zero links quebrados

---

## Fase 2: Automação e Governança (~3-4h)

### F2.1: Atualizar archive-adrs.sh [D-003]

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| F2.1.1 | Adicionar `-execution-contract.md` ao array de sufixos (linha 60) | ⬜ | 🟡 | F1.1 | 2min |
| F2.1.2 | Adicionar `-execution-report.md` ao array de sufixos | ⬜ | 🟡 | F2.1.1 | 1min |
| F2.1.3 | Adicionar `-change-plan.md` ao array de sufixos | ⬜ | 🟡 | F2.1.2 | 1min |
| F2.1.4 | Mover ADR-007-change-plan.md para archive/ | ⬜ | 🟡 | F2.1.3 | 1min |
| F2.1.5 | Mover ADR-007-execution-contract.md para archive/ | ⬜ | 🟡 | F2.1.4 | 1min |
| F2.1.6 | Mover ADR-007-execution-report.md para archive/ | ⬜ | 🟡 | F2.1.5 | 1min |
| F2.1.7 | Verificar que docs/adr/ só tem INDEX.md e archive/ | ⬜ | 🟡 | F2.1.6 | 2min |

**Checkpoint F2.1:**
- [ ] Script reconhece 6 sufixos
- [ ] 3 arquivos órfãos movidos para archive/
- [ ] `ls docs/adr/` mostra só `INDEX.md archive/`

---

### F2.2: Remover sync-pages.yml [D-004]

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| F2.2.1 | Deletar `.github/workflows/sync-pages.yml` | ⬜ | 🟡 | — | 1min |
| F2.2.2 | Verificar que nenhum arquivo referencia sync-pages | ⬜ | 🟡 | F2.2.1 | 2min |

**Checkpoint F2.2:**
- [ ] `sync-pages.yml` não existe
- [ ] Zero referências a `sync-pages` no repo

---

### F2.3: Sincronizar versão [D-005]

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| F2.3.1 | Corrigir README L153: `v2.1.0` → `v2.0.3` | ⬜ | 🟡 | — | 1min |
| F2.3.2 | Verificar que index.json já diz `2.0.3` (sem mudança) | ⬜ | 🟢 | — | 1min |
| F2.3.3 | Verificar que CHANGELOG já tem entry `[2.0.3]` (sem mudança) | ⬜ | 🟢 | — | 1min |

**Checkpoint F2.3:**
- [ ] README, index.json, CHANGELOG todos dizem `2.0.3`

---

### F2.4: Adicionar agents-md-generator ao CHANGELOG [D-006]

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| F2.4.1 | Adicionar entrada na seção Added de [2.0.3] | ⬜ | 🟡 | F2.3 | 5min |
| F2.4.2 | Verificar que entrada menciona ADR-007, 7 templates, 3 examples | ⬜ | 🟢 | F2.4.1 | 2min |

**Checkpoint F2.4:**
- [ ] CHANGELOG tem entrada para agents-md-generator dentro de [2.0.3]

---

### F2.5: Validação encoding + limpar vazamentos [D-007]

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| F2.5.1 | Adicionar check #11 (encoding) em validate-skill.sh | ⬜ | 🟡 | F1.1 | 5min |
| F2.5.2 | Corrigir AGENTS.md L77: `空行` → `linhas vazias` | ⬜ | 🟡 | — | 1min |
| F2.5.3 | Corrigir AGENTS-skills-repo.md L41: `空行` → `linhas vazias` | ⬜ | 🟡 | — | 1min |
| F2.5.4 | Corrigir test-before-refactor.md L116: `分支` → `branches` | ⬜ | 🟡 | — | 1min |
| F2.5.5 | Corrigir refactoring/SKILL.md L216: `难以` → `difícil de` | ⬜ | 🟡 | — | 1min |
| F2.5.6 | Corrigir refactoring/SKILL.md L231: `难以` → `difícil de` | ⬜ | 🟡 | — | 1min |
| F2.5.7 | Corrigir refactoring/SKILL.md L305: `替换` → `substituir` | ⬜ | 🟡 | — | 1min |
| F2.5.8 | Corrigir data-modeling/SKILL.md L56: Mermaid corrompido | ⬜ | 🟡 | — | 2min |
| F2.5.9 | Corrigir data-modeling/SKILL.md L239: `覆盖索covers` → `covering index` | ⬜ | 🟡 | — | 1min |
| F2.5.10 | Corrigir AGENTS-webapp.md L226: `难 de refactor` → `difícil de refatorar` | ⬜ | 🟡 | — | 1min |
| F2.5.11 | Verificar zero vazamentos com grep | ⬜ | 🟡 | F2.5.2-F2.5.10 | 3min |

**Checkpoint F2.5:**
- [ ] Check #11 existe em validate-skill.sh
- [ ] 9/9 vazamentos corrigidos
- [ ] `grep -rnP` retorna ZERO

---

**Checkpoint Geral Fase 2:**
- [ ] F2.1-F2.5 concluídas
- [ ] archive-adrs.sh completo
- [ ] sync-pages.yml removido
- [ ] Versão consistente
- [ ] CHANGELOG atualizado
- [ ] Encoding limpo

---

## Fase 3: Completude e Dogfooding (~4-6h)

### F3.1: Adicionar exemplos práticos [D-008]

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| F3.1.1 | Criar writing-plans/examples/api-migration-plan.md | ⬜ | 🟢 | Fase 2 | 30min |
| F3.1.2 | Criar writing-plans/examples/feature-breakdown.md | ⬜ | 🟢 | F3.1.1 | 30min |
| F3.1.3 | Criar api-design/examples/rest-crud-spec.md | ⬜ | 🟢 | Fase 2 | 30min |
| F3.1.4 | Criar api-design/examples/error-handling-contract.md | ⬜ | 🟢 | F3.1.3 | 30min |
| F3.1.5 | Criar security-review/examples/dependency-audit.md | ⬜ | 🟢 | Fase 2 | 30min |
| F3.1.6 | Criar security-review/examples/crypto-validation.md | ⬜ | 🟢 | F3.1.5 | 30min |
| F3.1.7 | Verificar que cada exemplo tem ≥30 linhas | ⬜ | 🟢 | F3.1.1-F3.1.6 | 5min |

**Checkpoint F3.1:**
- [ ] writing-plans: ≥2 exemplos
- [ ] api-design: ≥2 exemplos
- [ ] security-review: ≥2 exemplos
- [ ] Cada exemplo ≥30 linhas

---

### F3.2: Executar skill-audit-bulletin no repo [D-009]

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| F3.2.1 | Criar diretório `docs/audits/` | ⬜ | 🟢 | Fase 2 | 1min |
| F3.2.2 | Gerar audit bulletin seguindo template | ⬜ | 🟢 | F3.2.1 | 2h |
| F3.2.3 | Cobrir ≥5 skills críticas | ⬜ | 🟢 | F3.2.2 | — |
| F3.2.4 | Verificar score ≥ 90/100 | ⬜ | 🟢 | F3.2.3 | 10min |

**Checkpoint F3.2:**
- [ ] `docs/audits/` existe
- [ ] Audit bulletin gerado
- [ ] Score ≥ 90/100

---

**Checkpoint Geral Fase 3:**
- [ ] F3.1 e F3.2 concluídas
- [ ] Exemplos criados para 3 skills
- [ ] Audit bulletin existe

---

## Fase 4: Validação Final

### F4.1: Validação cruzada completa

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| F4.1.1 | Executar `validate-index.sh` — 22/22 skills, 0 erros | ⬜ | 🔴 | Todas | 3min |
| F4.1.2 | Executar `validate-skill.sh` em todas as 22 skills | ⬜ | 🔴 | F4.1.1 | 10min |
| F4.1.3 | Verificar zero links quebrados | ⬜ | 🔴 | F4.1.2 | 2min |
| F4.1.4 | Verificar zero vazamentos CJK/árabe | ⬜ | 🔴 | F4.1.3 | 2min |
| F4.1.5 | Verificar versão consistente | ⬜ | 🔴 | F4.1.4 | 1min |
| F4.1.6 | Verificar sync-pages.yml removido | ⬜ | 🟡 | — | 1min |
| F4.1.7 | Verificar archive-adrs.sh com 6 sufixos | ⬜ | 🟡 | — | 1min |
| F4.1.8 | Verificar exemplos existem | ⬜ | 🟡 | — | 2min |
| F4.1.9 | Verificar audit bulletin existe | ⬜ | 🟡 | — | 1min |

**Checkpoint F4.1:**
- [ ] validate-index.sh passa
- [ ] validate-skill.sh passa para todas as 22 skills
- [ ] Zero links quebrados
- [ ] Zero vazamentos
- [ ] Versão consistente
- [ ] sync-pages.yml removido
- [ ] archive-adrs.sh completo
- [ ] Exemplos criados
- [ ] Audit bulletin existe

---

## Resumo Geral

| Fase | Tarefas | Horas Est. | Status | Commit |
|------|---------|------------|--------|--------|
| Fase 1: Bugs de CI e Links | 10 | ~1h | ✅ Concluído | `b14c224` |
| Fase 2: Automação e Governança | 17 | ~3-4h | ✅ Concluído | `7203f89` |
| Fase 3: Exemplos | 7 | ~2h | ✅ Concluído | `cb081b2` |
| Fase 3: Dogfooding audit | 4 | ~2h | ⏸️ Adiado | — |
| Fase 4: Validação | 9 | ~30min | ✅ Concluído | — |
| **Total** | **47** | **~6-8h** | **✅ 86% (8/9 débitos)** | |

---

*Documento gerado em 2026-07-05. Referência: ADR-008.*
*Implementação concluída em 2026-07-05.*
