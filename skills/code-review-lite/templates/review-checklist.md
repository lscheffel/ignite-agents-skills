# Code Review Lite Checklist

> Quick checklist for lightweight code review (code-review-lite)

---

## Pre-Review

- [ ] Current branch identified
- [ ] Modified files listed (`git diff --name-only`)
- [ ] Task/issue context loaded
- [ ] ADRs referenced identified
- [ ] TODOs referenced identified

---

## Phase 1: Context Loading

- [ ] Expected behavior understood
- [ ] Expected output defined
- [ ] Architectural constraints known

---

## Phase 2: Five Dimensions

### 1. Plan Alignment
- [ ] Implementation = Requirements
- [ ] Scope respected (no gold-plating)
- [ ] Unnecessary functionality absent

### 2. Obvious Bugs
- [ ] No null references
- [ ] Imports resolved
- [ ] Valid conditions
- [ ] Returns present
- [ ] Exceptions handled
- [ ] No obvious race conditions

### 3. Security Regression
- [ ] No exposed secrets
- [ ] Input sanitized
- [ ] Auth checks present
- [ ] No injection vectors (SQL, command, path)
- [ ] Secure deserialization

### 4. Architecture Drift
- [ ] No duplicated code
- [ ] Abstractions intact
- [ ] No circular dependencies
- [ ] ADRs respected
- [ ] Responsibilities not leaking

### 5. Testing
- [ ] Existing tests pass
- [ ] New behavior tested
- [ ] Obvious gaps covered

---

## Decision

- [ ] **APPROVED** — No blocking issues
- [ ] **APPROVED_WITH_WARNINGS** — Minor issues documented
- [ ] **REQUIRES_FIXES** — Blocking issues listed
- [ ] **ESCALATE_TO_FULL_REVIEW** — Confidence < 70% or escalation triggers

---

## Escalation Triggers (Auto)

- [ ] Auth changed
- [ ] Payment flow changed
- [ ] Infrastructure changed
- [ ] Public API changed
- [ ] DB schema changed
- [ ] Lockfile changed

---

## Notes

Found issues:
-
-

Warnings:
-
-

---

*Template: `skills/code-review-lite/templates/review-checklist.md`*