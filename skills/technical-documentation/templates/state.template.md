# Project State & Agent Memory (STATE.md)

> **Persistent and Live Memory of the Repository.**  
> This document stores operational context, current architecture, pipeline states, recent decisions, and outstanding technical debts for immediate guidance of AI agents.

---

## 1. Repository General Context

- **Project:** {{PROJECT_NAME}}
- **Last Updated:** {{LAST_UPDATED_DATE}}
- **Active Branch:** `{{CURRENT_BRANCH}}`
- **Lifecycle Stage:** `{{LIFECYCLE_STAGE}}` (e.g., Active Development, Stabilization, Maintenance)

---

## 2. Recent Architectural Decisions (Active & Consolidated ADRs)

| ADR | Title | Implementation Status | Archival Status |
|---|---|---|---|
{{#each ADR_LIST}}
| `{{ID}}` | {{TITLE}} | `{{IMPL_STATUS}}` | {{ARCHIVED_LABEL}} |
{{/each}}

---

## 3. Outstanding Technical Debt Status

Consolidated from `docs/governance/tech-debt-registry.json`:

| ID | Severity | Domain | Description | Status | Mitigation Reference |
|---|---|---|---|---|---|
{{#each DEBTS_LIST}}
| `{{ID}}` | `{{SEVERITY}}` | `{{DOMAIN}}` | {{DESCRIPTION}} | `{{STATUS}}` | {{MITIGATION}} |
{{/each}}

---

## 4. Session History & Key Decisions

### Session: {{SESSION_DATE}}
- **Objective:** {{SESSION_GOAL}}
- **Changes Made:** {{SESSION_CHANGES}}
- **Challenges/Blocks Overcome:** {{SESSION_BLOCKERS}}
- **Immediate Next Steps:** {{SESSION_NEXT_STEPS}}

---

## 5. Invariants & Critical Rules of the Repository

1. **ADR Governance:** All code is driven by ADRs with Triad/Quadrant. Manual mocking of `ER.md` is strictly prohibited.
2. **Scope Isolation:** Peripheral smells are not corrected during the task; they must be registered via CLI in `tech-debt-registry.json`.
3. **SOTA Documentation Pattern:** All documentation must be dense, rich in context, and maintain the principle of *single source of truth*.