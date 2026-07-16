# Code Review Lite Checklist

> Checklist rápido para revisão de código leve (code-review-lite)

---

## Pré-Revisão

- [ ] Branch atual identificado
- [ ] Arquivos modificados listados (`git diff --name-only`)
- [ ] Contexto da task/issue carregado
- [ ] ADRs referenciadas identificadas
- [ ] TODOs referenciados identificados

---

## Fase 1: Context Loading

- [ ] Comportamento esperado entendido
- [ ] Output esperado definido
- [ ] Constraints arquiteturais conhecidas

---

## Fase 2: Five Dimensions

### 1. Plan Alignment
- [ ] Implementação = Requisitos
- [ ] Escopo respeitado (sem gold-plating)
- [ ] Funcionalidade desnecessária ausente

### 2. Obvious Bugs
- [ ] Sem referências nulas
- [ ] Imports resolvem
- [ ] Condições válidas
- [ ] Returns presentes
- [ ] Exceções tratadas
- [ ] Sem race conditions óbvias

### 3. Security Regression
- [ ] Sem secrets expostos
- [ ] Input sanitizado
- [ ] Auth checks presentes
- [ ] Sem injection vectors (SQL, command, path)
- [ ] Deserialization segura

### 4. Architecture Drift
- [ ] Sem duplicação nova
- [ ] Abstrações intactas
- [ ] Sem dependências circulares
- [ ] ADRs respeitadas
- [ ] Responsabilidades não vazando

### 5. Testing
- [ ] Testes existentes passam
- [ ] Novo comportamento testado
- [ ] Gaps óbvios cobertos

---

## Decisão

- [ ] **APPROVED** — Sem issues bloqueantes
- [ ] **APPROVED_WITH_WARNINGS** — Issues menores documentados
- [ ] **REQUIRES_FIXES** — Issues bloqueantes listados
- [ ] **ESCALATE_TO_FULL_REVIEW** — Confidence < 70% ou triggers de escala

---

## Escalation Triggers (Auto)

- [ ] Auth alterado
- [ ] Payment flow alterado
- [ ] Infrastructure alterado
- [ ] Public API alterado
- [ ] DB schema alterado
- [ ] Lockfile alterado

---

## Notas

Issues encontrados:
-
-

Warnings:
-
-

---

*Template: `skills/code-review-lite/templates/review-checklist.md`*