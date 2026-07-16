---
name: code-review-lite
description: Lightweight code review optimized for AI-first and vibe-coding workflows. Use after completing features, refactors, or before commits to detect regressions, architectural drift, security mistakes, and broken assumptions while preserving development velocity.
version: 4.0-lite
maturity: daily-development
classification: fast-quality-gate
owner: Development Runtime
---

tags:

* code-review
* vibe-coding
* quality-gate
* ai-development
* fast-feedback

triggers:

* feature_completed
* refactor_completed
* before_commit
* before_push
* major_file_change

execution_target: 30-90_seconds

required_before_merge: false
required_before_release: true

capabilities:

* plan_alignment
* regression_detection
* security_regression_detection
* architecture_drift_detection
* test_validation

integrations:

* planning
* adr
* todo
* verification-before-completion

## skill_type: FAST_GUARDRAIL

# Code Review Lite v4

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
