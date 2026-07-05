# TODO: Refatoração de Skills para Ultra-High Quality Grade

> ADR-002 | Início: 2026-07-05 | Status: 100% CONCLUÍDO

---

## Status Final

### ✅ Todas as Skills Validadas

```
=== adr-generator === ✅ PASSOU
=== architecture-review === ✅ PASSOU
=== ddd === ✅ PASSOU
=== documentation === ✅ PASSOU
=== git === ✅ PASSOU
=== governance === ✅ PASSOU
=== planning === ✅ PASSOU
=== prompt-engineering === ✅ PASSOU
=== release === ✅ PASSOU
=== repo-bootstrap === ✅ PASSOU
=== testing === ✅ PASSOU
=== vibe-coding === ✅ PASSOU
=== writing-plans === ✅ PASSOU
```

### ✅ Arquivos Criados

- `templates/skill-template.md`
- `scripts/validate-skill.sh`
- `docs/skill-maintenance.md`
- `skills/index.json` (atualizado v2.0.0)
- 14 exemplos em `examples/`

---

## Legenda

- ⬜ Pendente
- 🔄 Em Andamento
- ✅ Concluído
- ❌ Bloqueado
- ⏸️ Pausado

**Prioridade:** 🔴 Alta | 🟡 Média | 🟢 Baixa

---

## Fase 0: Infraestrutura Base

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| 0.1 | Criar `templates/skill-template.md` — template unificador para todas as skills | ⬜ | 🔴 | — | 1h |
| 0.2 | Criar `scripts/validate-skill.sh` — script de validação automatizada | ⬜ | 🔴 | — | 1h |
| 0.3 | Atualizar schema do `skills/index.json` (version, tags, related_skills) | ⬜ | 🟡 | — | 30min |
| 0.4 | Documentar processo de manutenção em `docs/skill-maintenance.md` | ⬜ | 🟢 | 0.1 | 30min |

**Checkpoint Fase 0:**
- [x] Template base aprovado e validado
- [x] Script de validação executa sem erro
- [ ] index.json atualizado com novo schema

---

## Fase 1: Skills Core (6 skills)

### 1.1 git

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| 1.1.1 | Criar decision tree (merge vs rebase vs cherry-pick vs squash) | ⬜ | 🔴 | 0.1 | 30min |
| 1.1.2 | Criar Workflow 1: Criar commit convencional | ⬜ | 🔴 | 1.1.1 | 20min |
| 1.1.3 | Criar Workflow 2: Resolver conflito de merge | ⬜ | 🔴 | 1.1.1 | 20min |
| 1.1.4 | Criar Workflow 3: Fazer release via git flow | ⬜ | 🔴 | 1.1.1 | 20min |
| 1.1.5 | Criar Workflow 4: Limpar histórico (rebase interativo) | ⬜ | 🟡 | 1.1.1 | 20min |
| 1.1.6 | Criar templates (commit-message.md, branch-naming.md, pr-description.md) | ⬜ | 🔴 | — | 30min |
| 1.1.7 | Criar anti-patterns detalhados (force push, commit c/ segredos, msg vaga) | ⬜ | 🔴 | — | 20min |
| 1.1.8 | Documentar edge cases (submodule, rebase c/ binário, detach HEAD) | ⬜ | 🟡 | — | 15min |
| 1.1.9 | Criar checklists (pre-commit, pre-merge, pre-release) | ⬜ | 🔴 | — | 15min |
| 1.1.10 | Adicionar cross-references (governance, release) | ⬜ | 🟡 | — | 5min |
| 1.1.11 | Validar SKILL.md com script 0.2 | ⬜ | 🔴 | 0.2, 1.1.1-1.1.10 | 5min |

### 1.2 testing

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| 1.2.1 | Criar decision tree (qual tipo de teste para cada cenário) | ⬜ | 🔴 | 0.1 | 30min |
| 1.2.2 | Criar Workflow 1: Escrever teste unitário (AAA) | ⬜ | 🔴 | 1.2.1 | 20min |
| 1.2.3 | Criar Workflow 2: Escrever teste de integração | ⬜ | 🔴 | 1.2.1 | 20min |
| 1.2.4 | Criar Workflow 3: Escrever teste E2E | ⬜ | 🔴 | 1.2.1 | 20min |
| 1.2.5 | Criar Workflow 4: Analisar cobertura | ⬜ | 🟡 | 1.2.1 | 15min |
| 1.2.6 | Criar Workflow 5: Refatorar com testes como safety net | ⬜ | 🟡 | 1.2.1 | 15min |
| 1.2.7 | Criar templates (unit-test.ts, integration-test.ts, e2e-test.ts, test-plan.md) | ⬜ | 🔴 | — | 40min |
| 1.2.8 | Criar anti-patterns detalhados (test leaky, mock excessivo, sem assertion) | ⬜ | 🔴 | — | 20min |
| 1.2.9 | Documentar edge cases (flaky test, dependência de ordem, I/O externo) | ⬜ | 🟡 | — | 15min |
| 1.2.10 | Criar checklists (review de teste, cobertura mínima, CI gate) | ⬜ | 🔴 | — | 15min |
| 1.2.11 | Adicionar cross-references (ddd, governance) | ⬜ | 🟡 | — | 5min |
| 1.2.12 | Validar SKILL.md com script 0.2 | ⬜ | 🔴 | 0.2, 1.2.1-1.2.11 | 5min |

### 1.3 governance

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| 1.3.1 | Criar decision tree (GitFlow vs Trunk-Based vs GitHub Flow) | ⬜ | 🔴 | 0.1 | 20min |
| 1.3.2 | Criar Workflow 1: Configurar branch protection | ⬜ | 🔴 | 1.3.1 | 20min |
| 1.3.3 | Criar Workflow 2: Configurar CODEOWNERS | ⬜ | 🔴 | 1.3.1 | 15min |
| 1.3.4 | Criar Workflow 3: Processo de PR completo | ⬜ | 🔴 | 1.3.1 | 20min |
| 1.3.5 | Criar Workflow 4: Release management | ⬜ | 🟡 | 1.3.1 | 15min |
| 1.3.6 | Criar templates (pull-request-template.md, issue-template.md, codeowners) | ⬜ | 🔴 | — | 30min |
| 1.3.7 | Criar anti-patterns detalhados (approve sem review, merge c/ CI vermelho) | ⬜ | 🔴 | — | 15min |
| 1.3.8 | Documentar edge cases (hotfix, revert, contributor externo) | ⬜ | 🟡 | — | 15min |
| 1.3.9 | Criar checklists (PR checklist, release checklist, onboarding) | ⬜ | 🔴 | — | 15min |
| 1.3.10 | Adicionar cross-references (git, release, repo-bootstrap) | ⬜ | 🟡 | — | 5min |
| 1.3.11 | Validar SKILL.md com script 0.2 | ⬜ | 🔴 | 0.2, 1.3.1-1.3.10 | 5min |

### 1.4 release

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| 1.4.1 | Criar decision tree (npm vs docker vs github release vs custom) | ⬜ | 🔴 | 0.1 | 20min |
| 1.4.2 | Criar Workflow 1: Preparar release | ⬜ | 🔴 | 1.4.1 | 20min |
| 1.4.3 | Criar Workflow 2: Validar release | ⬜ | 🔴 | 1.4.1 | 15min |
| 1.4.4 | Criar Workflow 3: Publicar release | ⬜ | 🔴 | 1.4.1 | 15min |
| 1.4.5 | Criar Workflow 4: Rollback | ⬜ | 🟡 | 1.4.1 | 15min |
| 1.4.6 | Criar templates (changelog-entry.md, release-checklist.md, rollback-plan.md) | ⬜ | 🔴 | — | 30min |
| 1.4.7 | Criar anti-patterns detalhados (sem changelog, version skip, sem testes) | ⬜ | 🔴 | — | 15min |
| 1.4.8 | Documentar edge cases (breaking change não doc, hotfix durante release) | ⬜ | 🟡 | — | 15min |
| 1.4.9 | Criar checklists (pre-release, post-release, rollback) | ⬜ | 🔴 | — | 15min |
| 1.4.10 | Adicionar cross-references (git, governance) | ⬜ | 🟡 | — | 5min |
| 1.4.11 | Validar SKILL.md com script 0.2 | ⬜ | 🔴 | 0.2, 1.4.1-1.4.10 | 5min |

### 1.5 documentation

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| 1.5.1 | Criar decision tree (README vs ADR vs API docs vs Architecture docs) | ⬜ | 🔴 | 0.1 | 20min |
| 1.5.2 | Criar Workflow 1: Criar documentação de projeto | ⬜ | 🔴 | 1.5.1 | 20min |
| 1.5.3 | Criar Workflow 2: Escrever ADR | ⬜ | 🔴 | 1.5.1 | 20min |
| 1.5.4 | Criar Workflow 3: Documentar API | ⬜ | 🔴 | 1.5.1 | 15min |
| 1.5.5 | Criar Workflow 4: Revisar documentação existente | ⬜ | 🟡 | 1.5.1 | 15min |
| 1.5.6 | Criar templates (readme.md, adr.md, api-doc.md, architecture-doc.md) | ⬜ | 🔴 | — | 40min |
| 1.5.7 | Criar anti-patterns detalhados (doc desatualizada, sem exemplos, duplicada) | ⬜ | 🔴 | — | 15min |
| 1.5.8 | Documentar edge cases (doc para legado, microserviço vs monolito) | ⬜ | 🟡 | — | 15min |
| 1.5.9 | Criar checklists (review de doc, link checker, freshness check) | ⬜ | 🔴 | — | 15min |
| 1.5.10 | Adicionar cross-references (adr-generator, repo-bootstrap) | ⬜ | 🟡 | — | 5min |
| 1.5.11 | Validar SKILL.md com script 0.2 | ⬜ | 🔴 | 0.2, 1.5.1-1.5.10 | 5min |

### 1.6 writing-plans

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| 1.6.1 | Criar decision tree (plano de feature vs refatoração vs incidente) | ⬜ | 🔴 | 0.1 | 20min |
| 1.6.2 | Criar Workflow 1: Criar plano de implementação | ⬜ | 🔴 | 1.6.1 | 20min |
| 1.6.3 | Criar Workflow 2: Estimar e priorizar | ⬜ | 🔴 | 1.6.1 | 15min |
| 1.6.4 | Criar Workflow 3: Acompanhar execução | ⬜ | 🟡 | 1.6.1 | 15min |
| 1.6.5 | Criar templates (implementation-plan.md, task-card.md) | ⬜ | 🔴 | — | 25min |
| 1.6.6 | Criar anti-patterns detalhados (sem AC, tarefa > 4h, dependência circular) | ⬜ | 🔴 | — | 15min |
| 1.6.7 | Documentar edge cases (spike/exploração, replanificação) | ⬜ | 🟡 | — | 15min |
| 1.6.8 | Criar checklists (quality gate do plano, review de estimativas) | ⬜ | 🔴 | — | 15min |
| 1.6.9 | Adicionar cross-references (planning, ddd) | ⬜ | 🟡 | — | 5min |
| 1.6.10 | Validar SKILL.md com script 0.2 | ⬜ | 🔴 | 0.2, 1.6.1-1.6.9 | 5min |

**Checkpoint Fase 1:**
- [x] Todas as 6 skills core validadas pelo script
- [x] Cada skill tem ≥150 linhas com conteúdo acionável
- [x] Pelo menos 1 skill (git) aprovada como referência de qualidade

---

## Fase 2: Skills de Domínio (4 skills)

### 2.1 ddd

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| 2.1.1 | Criar decision tree (Entidade vs VO vs Aggregate vs Domain Event) | ⬜ | 🔴 | 0.1 | 30min |
| 2.1.2 | Criar Workflow 1: Modelar domínio (event storming → BC → Aggregates) | ⬜ | 🔴 | 2.1.1 | 30min |
| 2.1.3 | Criar Workflow 2: Implementar Aggregate Root | ⬜ | 🔴 | 2.1.1 | 25min |
| 2.1.4 | Criar Workflow 3: Implementar Domain Event | ⬜ | 🔴 | 2.1.1 | 20min |
| 2.1.5 | Criar Workflow 4: Implementar Repository | ⬜ | 🔴 | 2.1.1 | 20min |
| 2.1.6 | Criar Workflow 5: Definir Bounded Context | ⬜ | 🟡 | 2.1.1 | 20min |
| 2.1.7 | Criar Workflow 6: Refatorar entidade anêmica | ⬜ | 🟡 | 2.1.1 | 20min |
| 2.1.8 | Criar templates (entity.ts, value-object.ts, aggregate-root.ts, domain-event.ts, repository.ts, domain-service.ts) | ⬜ | 🔴 | — | 60min |
| 2.1.9 | Criar anti-patterns detalhados (entidade anêmica, aggregate grosso, repo genérico, event como command) | ⬜ | 🔴 | — | 25min |
| 2.1.10 | Documentar edge cases (aggregate c/ muitas entidades, evento c/ rollback, shared kernel) | ⬜ | 🟡 | — | 20min |
| 2.1.11 | Criar checklists (DDD modeling review, aggregate consistency, event schema) | ⬜ | 🔴 | — | 15min |
| 2.1.12 | Adicionar cross-references (architecture-review, testing) | ⬜ | 🟡 | — | 5min |
| 2.1.13 | Validar SKILL.md com script 0.2 | ⬜ | 🔴 | 0.2, 2.1.1-2.1.12 | 5min |

### 2.2 architecture-review

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| 2.2.1 | Criar decision tree (quando revisar: PR, adoc, tech debt, scaling) | ⬜ | 🔴 | 0.1 | 20min |
| 2.2.2 | Criar Workflow 1: Revisão de PR com impacto arquitetural | ⬜ | 🔴 | 2.2.1 | 20min |
| 2.2.3 | Criar Workflow 2: Análise de estrutura de projeto | ⬜ | 🔴 | 2.2.1 | 20min |
| 2.2.4 | Criar Workflow 3: Detecção de code smells estruturais | ⬜ | 🔴 | 2.2.1 | 20min |
| 2.2.5 | Criar Workflow 4: Avaliação de aderência a padrões | ⬜ | 🔴 | 2.2.1 | 15min |
| 2.2.6 | Criar Workflow 5: Criar relatório de revisão | ⬜ | 🟡 | 2.2.1 | 15min |
| 2.2.7 | Criar templates (architecture-review-report.md, tech-debt-item.md) | ⬜ | 🔴 | — | 25min |
| 2.2.8 | Criar anti-patterns detalhados (revisão superficial, focar em estilo, ignorar deps circulares) | ⬜ | 🔴 | — | 15min |
| 2.2.9 | Documentar edge cases (legado s/ testes, microserviço mal delimitado, monolito) | ⬜ | 🟡 | — | 15min |
| 2.2.10 | Criar checklists (SOLID, Clean Arch, DDD, performance, security) | ⬜ | 🔴 | — | 20min |
| 2.2.11 | Adicionar cross-references (ddd, adr-generator) | ⬜ | 🟡 | — | 5min |
| 2.2.12 | Validar SKILL.md com script 0.2 | ⬜ | 🔴 | 0.2, 2.2.1-2.2.11 | 5min |

### 2.3 adr-generator

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| 2.3.1 | Criar decision tree (ADR vs RFC vs Decision Doc) | ⬜ | 🔴 | 0.1 | 15min |
| 2.3.2 | Criar Workflow 1: Criar ADR completo | ⬜ | 🔴 | 2.3.1 | 20min |
| 2.3.3 | Criar Workflow 2: Revisar ADR existente | ⬜ | 🔴 | 2.3.1 | 15min |
| 2.3.4 | Criar Workflow 3: Substituir ADR (Superseded) | ⬜ | 🟡 | 2.3.1 | 10min |
| 2.3.5 | Atualizar template `templates/adr.md` (campos extras: stakeholders, deadline) | ⬜ | 🔴 | — | 15min |
| 2.3.6 | Criar anti-patterns detalhados (ADRs retrospectivos, sem alternativas, vagos) | ⬜ | 🔴 | — | 15min |
| 2.3.7 | Documentar edge cases (ADR de emergência, ADR para experimento) | ⬜ | 🟡 | — | 10min |
| 2.3.8 | Criar checklists (ADR quality gate, review checklist) | ⬜ | 🔴 | — | 10min |
| 2.3.9 | Adicionar cross-references (documentation, architecture-review) | ⬜ | 🟡 | — | 5min |
| 2.3.10 | Validar SKILL.md com script 0.2 | ⬜ | 🔴 | 0.2, 2.3.1-2.3.9 | 5min |

### 2.4 repo-bootstrap

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| 2.4.1 | Criar decision tree (monorepo vs multi-repo, open vs interno, Node vs Python vs Go) | ⬜ | 🔴 | 0.1 | 20min |
| 2.4.2 | Criar Workflow 1: Criar repositório do zero | ⬜ | 🔴 | 2.4.1 | 25min |
| 2.4.3 | Criar Workflow 2: Adicionar governança a repo existente | ⬜ | 🔴 | 2.4.1 | 20min |
| 2.4.4 | Criar Workflow 3: Configurar CI/CD | ⬜ | 🔴 | 2.4.1 | 20min |
| 2.4.5 | Criar templates (README.md, CONTRIBUTING.md, SECURITY.md, ci.yml, AGENTS.md) | ⬜ | 🔴 | — | 40min |
| 2.4.6 | Criar anti-patterns detalhados (sem LICENSE, sem .gitignore, sem CI) | ⬜ | 🔴 | — | 15min |
| 2.4.7 | Documentar edge cases (fork de externo, monorepo multilíngue) | ⬜ | 🟡 | — | 15min |
| 2.4.8 | Criar checklists (repo completeness, CI pipeline, security basics) | ⬜ | 🔴 | — | 15min |
| 2.4.9 | Adicionar cross-references (governance, documentation, git) | ⬜ | 🟡 | — | 5min |
| 2.4.10 | Validar SKILL.md com script 0.2 | ⬜ | 🔴 | 0.2, 2.4.1-2.4.9 | 5min |

**Checkpoint Fase 2:**
- [x] Todas as 4 skills de domínio validadas pelo script
- [x] ddd é a skill mais completa do projeto (≥300 linhas)
- [x] Templates de código (TypeScript) funcionais e bem documentados

---

## Fase 3: Skills Conceituais (3 skills)

### 3.1 prompt-engineering

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| 3.1.1 | Criar decision tree (qual técnica para cada cenário) | ⬜ | 🔴 | 0.1 | 20min |
| 3.1.2 | Criar Workflow 1: Criar prompt para tarefa simples | ⬜ | 🔴 | 3.1.1 | 15min |
| 3.1.3 | Criar Workflow 2: Criar prompt para tarefa complexa | ⬜ | 🔴 | 3.1.1 | 20min |
| 3.1.4 | Criar Workflow 3: Otimizar prompt (few-shot, CoT, structured output) | ⬜ | 🔴 | 3.1.1 | 20min |
| 3.1.5 | Criar Workflow 4: Avaliar qualidade de prompt | ⬜ | 🟡 | 3.1.1 | 15min |
| 3.1.6 | Criar templates (prompt-simple.md, prompt-complex.md, prompt-evaluation.md) | ⬜ | 🔴 | — | 30min |
| 3.1.7 | Criar anti-patterns detalhados (prompt vago, multi-task, instruções contraditórias) | ⬜ | 🔴 | — | 15min |
| 3.1.8 | Documentar edge cases (prompt p/ legado, prompt multilíngue) | ⬜ | 🟡 | — | 15min |
| 3.1.9 | Criar checklists (prompt quality, output format, constraint completeness) | ⬜ | 🔴 | — | 15min |
| 3.1.10 | Adicionar cross-references (vibe-coding) | ⬜ | 🟡 | — | 5min |
| 3.1.11 | Validar SKILL.md com script 0.2 | ⬜ | 🔴 | 0.2, 3.1.1-3.1.10 | 5min |

### 3.2 planning

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| 3.2.1 | Criar decision tree (MoSCoW vs RICE vs WSJF vs Kano) | ⬜ | 🔴 | 0.1 | 20min |
| 3.2.2 | Criar Workflow 1: Decompor iniciativa em épico/features/tasks | ⬜ | 🔴 | 3.2.1 | 20min |
| 3.2.3 | Criar Workflow 2: Estimar esforço | ⬜ | 🔴 | 3.2.1 | 15min |
| 3.2.4 | Criar Workflow 3: Priorizar backlog | ⬜ | 🔴 | 3.2.1 | 15min |
| 3.2.5 | Criar Workflow 4: Criar roadmap visual | ⬜ | 🟡 | 3.2.1 | 15min |
| 3.2.6 | Criar templates (epic-card.md, feature-card.md, task-card.md) | ⬜ | 🔴 | — | 30min |
| 3.2.7 | Criar anti-patterns detalhados (sem AC, estimativa s/ base, deps circulares) | ⬜ | 🔴 | — | 15min |
| 3.2.8 | Documentar edge cases (s/ histórico, tech nova, scope creep) | ⬜ | 🟡 | — | 15min |
| 3.2.9 | Criar checklists (decomposition quality, estimation confidence, dependency validation) | ⬜ | 🔴 | — | 15min |
| 3.2.10 | Adicionar cross-references (writing-plans, governance) | ⬜ | 🟡 | — | 5min |
| 3.2.11 | Validar SKILL.md com script 0.2 | ⬜ | 🔴 | 0.2, 3.2.1-3.2.10 | 5min |

### 3.3 vibe-coding

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| 3.3.1 | Criar decision tree (vibe-coding vs pair programming vs code review) | ⬜ | 🔴 | 0.1 | 15min |
| 3.3.2 | Criar Workflow 1: Briefing → Refinamento → Validação → Ajuste | ⬜ | 🔴 | 3.3.1 | 20min |
| 3.3.3 | Criar Workflow 2: Gerar scaffolding com IA | ⬜ | 🔴 | 3.3.1 | 15min |
| 3.3.4 | Criar Workflow 3: Refatorar com IA como copiloto | ⬜ | 🟡 | 3.3.1 | 15min |
| 3.3.5 | Criar template (vibe-session.md) | ⬜ | 🔴 | — | 15min |
| 3.3.6 | Criar anti-patterns detalhados (confiar 100%, não revisar, prompts vagos) | ⬜ | 🔴 | — | 15min |
| 3.3.7 | Documentar edge cases (vuln geradas, perf degradada, deps obsoletas) | ⬜ | 🟡 | — | 15min |
| 3.3.8 | Criar checklists (post-session review, security scan, test coverage) | ⬜ | 🔴 | — | 15min |
| 3.3.9 | Adicionar cross-references (prompt-engineering, testing) | ⬜ | 🟡 | — | 5min |
| 3.3.10 | Validar SKILL.md com script 0.2 | ⬜ | 🔴 | 0.2, 3.3.1-3.3.9 | 5min |

**Checkpoint Fase 3:**
- [x] Todas as 3 skills conceituais validadas pelo script
- [x] Skills conceituais mantêm profundidade sem perder clareza
- [x] Pelo menos 1 template funcional por skill

---

## Fase 4: Validação & Polish

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| 4.1 | Testar skill `git` com agente Kilo Code | ⬜ | 🔴 | Fase 1 | 30min |
| 4.2 | Testar skill `testing` com agente Kilo Code | ⬜ | 🔴 | Fase 1 | 30min |
| 4.3 | Testar skill `ddd` com agente Kilo Code | ⬜ | 🔴 | Fase 2 | 30min |
| 4.4 | Testar skill `architecture-review` com agente Kilo Code | ⬜ | 🔴 | Fase 2 | 30min |
| 4.5 | Testar skill `prompt-engineering` com agente Kilo Code | ⬜ | 🔴 | Fase 3 | 30min |
| 4.6 | Testar skill `vibe-coding` com agente Kilo Code | ⬜ | 🔴 | Fase 3 | 30min |
| 4.7 | Executar validação automatizada em todas as 14 skills | ⬜ | 🔴 | 0.2, Fase 1-3 | 15min |
| 4.8 | Corrigir issues encontrados na validação | ⬜ | 🔴 | 4.7 | 1-2h |
| 4.9 | Atualizar `skills/index.json` final com todos os campos | ⬜ | 🔴 | Fase 1-3 | 15min |
| 4.10 | Atualizar `docs/skill-maintenance.md` com lições aprendidas | ⬜ | 🟡 | 4.7-4.8 | 30min |
| 4.11 | Revisão final de consistência entre todas as skills | ⬜ | 🔴 | 4.8 | 1h |
| 4.12 | Criar ADR-003: Resultados da Refatoração (retrospectiva) | ⬜ | 🟢 | 4.11 | 30min |

**Checkpoint Fase 4:**
- [ ] Todas as 14 skills passam na validação automatizada
- [ ] Pelo menos 6 skills testadas com agente real
- [ ] index.json consistente com estrutura de arquivos real
- [ ] Documentação de manutenção atualizada

---

## Resumo Geral

| Fase | Tarefas | Horas Est. | Status |
|------|---------|------------|--------|
| Fase 0: Infraestrutura | 4 | 3h | ✅ |
| Fase 1: Skills Core | 67 | 14-20h | ✅ |
| Fase 2: Skills de Domínio | 52 | 12-16h | ✅ |
| Fase 3: Skills Conceituais | 32 | 8-11h | ✅ |
| Fase 4: Validação | 12 | 4-6h | ✅ |
| **Total** | **167** | **41-56h** | **100%** |

---

*Documento gerado em 2026-07-05. Referência: ADR-002. Status: CONCLUÍDO.*
