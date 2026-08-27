---
name: code-review-lite
version: 5.0.0-alias
description: Lightweight code review optimized for AI-first and vibe-coding workflows. Delegates directly to unified code-review (mode: lite).
related_skills:
  - cap
  - implementation
  - technical-documentation
domain: engineering-quality
triggers:
  - code-review-lite
  - quick-code-review
  - fast-pr-check
  - diff-review
  - revisao-rapida-codigo
  - revisao-lite
  - analisar-diff
  - lightweight-review
tags:
- code-review-lite
- engineering-quality
- vibe-coding
- fast-feedback
metadata:
  author: Antigravity Refactored Architecture
  provenance: internal
  last_audited: '2026-08-24'
---

# Code Review Lite (Unified Alias)

> 💡 **Nota de Arquitetura (ADR-024):** Esta skill opera como alias canônico e rápido do motor consolidado [`code-review`](../code-review/SKILL.md) configurado no modo `mode: lite`.

## Execução Rápida (30-90 segundos)

Ao receber solicitações de revisão iterativa, inspeção pré-commit ou vibe-coding:
1. Ative o motor `code-review` com diretriz `mode: lite`.
2. Analise o delta de diff recente (`git diff`).
3. Avalie regressões lógicas, segurança imediata (OWASP Top 10) e cobertura de testes.
4. Retorne feedback direto e conciso sem o overhead do protocolo multi-agente.

## Mission

Catch the mistakes that actually matter during day-to-day development while preserving momentum.

# Review Philosophy

Prioritize detection of:

1. Broken behavior
2. Architectural drift
3. Security regressions
4. Missing validation
5. Technical debt explosions

Ignore:

* cosmetic style issues
* micro optimizations
* theoretical edge cases
* premature abstractions

---

# Review Scope

Review only:

* modified files
* directly affected modules
* changed interfaces
* modified dependencies

Never review:

* entire repository
* unrelated modules
* historical commits

---

# Phase 1 — Context Loading

Collect:

* changed files
* current task
* ADR references
* TODO references

Determine:

* intended behavior
* expected output
* architectural constraints

If requirements are unclear:

```text
ASK_FOR_CONTEXT
```

---

# Phase 2 — Fast Review

Evaluate only five dimensions.

## 1. Plan Alignment

Questions:

* Does implementation match requirements?
* Was scope respected?
* Was unnecessary functionality introduced?

---

## 2. Obvious Bugs

Look for:

* null references
* missing imports
* broken conditions
* invalid assumptions
* missing returns
* race conditions
* unhandled exceptions

---

## 3. Security Regression

Look for:

* exposed secrets
* unsafe input handling
* missing authorization checks
* command injection
* path traversal
* unsafe deserialization

Do not perform full security audit.

---

## 4. Architecture Drift

Look for:

* duplicated logic
* broken abstractions
* circular dependencies
* leaking responsibilities
* violation of ADRs

---

## 5. Testing

Verify:

* existing tests still make sense
* new behavior is covered
* obvious missing tests

---

# Review Modes

## SMALL_CHANGE

Criteria:

* less than 5 files
* less than 300 lines

Focus:

* bugs
* regressions

---

## NORMAL_CHANGE

Criteria:

* 5-20 files
* less than 1500 lines

Focus:

* architecture
* tests
* security regressions

---

## LARGE_CHANGE

Criteria:

* more than 20 files
* more than 1500 lines

Action:

```text
RECOMMEND_FULL_REVIEW
```

---

# Output Format

## APPROVED

No blocking issues found.

---

## APPROVED_WITH_WARNINGS

Example:

* missing test
* minor duplication
* documentation lag

---

## REQUIRES_FIXES

Blocking examples:

* broken logic
* security issue
* ADR violation
* regression risk

---

# Escalation Rules

Automatically recommend full review if:

* authentication changed
* payment flow changed
* infrastructure changed
* public API changed
* database schema changed
* dependency lockfile changed

Escalation target:

```text
code-review-v4
```

---

# Anti-Patterns

Reject:

* massive god functions
* hidden side effects
* copy-paste programming
* bypassing architecture
* dead code accumulation

---

# Runtime Limits

| Metric         | Limit      |
| -------------- | ---------- |
| Files          | 20         |
| Changed Lines  | 1500       |
| Execution Time | 90 seconds |

---

# Final Rule

If confidence drops below:

```text
70%
```

Return:

```text
ESCALATE_TO_FULL_REVIEW
```

---

# Iron Law

```text
Move fast.
Do not move blindly.
```


## Decision Workflow

```mermaid
graph TD
    A["Início: Ativação da Skill (code-review-lite)"] --> B["Validação de Pré-requisitos & Escopo"]
    B --> C{"Requisitos Claros & Completos?"}
    C -->|Não| D["Solicitar Clarificação / Coletar Contexto (cap)"]
    C -->|Sim| E["Execução do Procedimento Canônico"]
    D --> E
    E --> F["Verificação de Qualidade & Critérios de Aceite"]
    F --> G{"Checklist 100% Aprovado?"}
    G -->|Não| E
    G -->|Sim| H["Completion Gate: Entrega do Artefato Certificado"]
```



## Anti-Patterns & Operational Guardrails

| Anti-Pattern | Severidade | Impacto Negativo | Mitigação Canônica |
|:---|:---:|:---|:---|
| **Execução Prematura sem Contexto** | 🔴 Critical | Alucinação de contexto e refatoração destrutiva | Ativar a skill `cap` para adquirir evidências mínimas antes de editar. |
| **Omissão de Checklists de Validação** | 🟡 Medium | Entrega de artefatos com inconsistências sintáticas | Executar rigorosamente o checklist passo a passo antes do handoff. |
| **Falta de Documentação de Decisões** | 🟢 Low | Perda de rastreabilidade técnica e drift arquitetural | Registrar trade-offs relevantes via skill `adr-generator`. |



## Edge Cases & Failure Modes

- **Ambiente Restrito / Read-Only:** Se o filesystem ou sandbox estiver bloqueado contra escrita, reportar o bloqueio com evidência imediata e gerar o patch em markdown diff.
- **Conflito de Especificação:** Caso encontre contradições entre a intenção do usuário e o SSOT (`AGENTS.md`), interromper e sinalizar as opções com trade-offs.
- **Timeout ou Exaustão de Contexto:** Em tarefas volumosas, decompor em sub-lotes atômicos utilizando a skill `subagent-driven-development`.



## Domain SOTA & Industry Engineering Standards

- **Triage Paradigms:** Fast-Path Pull Request Triage, Lightweight Linting, and Micro-Diff Reviews.
- **Scope Containment:** High-velocity verification for small, low-risk patches ($N_{\text{lines}} \le 200$).
- **Automated Pre-Checks:** CI gate green verification before starting human review.
- **Fast Turnaround:** SLA target for review turnaround $\le 4$ hours.

### Fast-Path Review Criteria:
A Pull Request qualifies for Lite Review if:

$$N_{\text{lines}} \le 200 \quad \text{and} \quad \text{FilesModified} \le 5 \quad \text{and} \quad \text{BreakingChanges} = \text{False}$$

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Fast-Path Escalation):** If a Lite Review reveals hidden architectural complexity or migration risk, immediately escalate to full `code-review`.
2. **Rule of Thumb 2 (Automated Test Pass Invariant):** Never approve a Lite Review if CI pipeline or automated tests have failing status.
3. **Rule of Thumb 3 (Focus on Correctness):** Focus exclusively on logic correctness, security, and test coverage; avoid bike-shedding on personal style preferences.
4. **Rule of Thumb 4 (Single-Pass Approval):** If only minor non-blocking nits remain, approve the PR and trust the author to apply them before merging.

## Operational Verification Checklist

- [ ] Todos os pré-requisitos e arquivos-alvo foram inspecionados antes da modificação.
- [ ] O procedimento seguiu estritamente as regras e boas práticas da especialização.
- [ ] As diretrizes de segurança, tipagem e estilo foram preservadas.
- [ ] Os testes unitários ou comandos de validação foram executados com sucesso.
- [ ] O artefato final foi inspecionado contra o completion gate.

