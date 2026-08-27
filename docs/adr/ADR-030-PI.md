# ADR-030 Implementation Plan (PI): Core Architecture & Governance Domain SOTA Hardening

> **Companion Artifact to:** [ADR-030.md](./ADR-030.md) & [ADR-030-BP.md](./ADR-030-BP.md)  
> **Type:** Phased Implementation Plan (Tier II)  
> **Status:** READY FOR EXECUTION  

---

## 1. Execution Phases

### Phase 1: Architectural Decision & Challenge Skills Hardening
- [x] 1.1 Ingest Blast Radius & Two-Way Door algebra into `skills/adr-architecture-elevation/SKILL.md`.
- [x] 1.2 Ingest Decision Complexity Index and cross-schema validation into `skills/adr-generator/SKILL.md`.
- [x] 1.3 Ingest Cryptographic SHA-256 commit binding into `skills/adr-archive/SKILL.md`.

### Phase 2: Code Review, Discovery & Context Skills Hardening
- [x] 2.1 Ingest Robert C. Martin's Package Distance ($D = |A+I-1|$) and AST rules into `skills/architecture-review/SKILL.md`.
- [x] 2.2 Ingest Dynamic Token Budgeting Equation into `skills/cap/SKILL.md`.
- [x] 2.3 Ingest Double Diamond Ambiguity Metric ($A_{\text{score}} \le 0.15$) into `skills/brainstorming/SKILL.md`.

### Phase 3: Repository Governance & SSOT Synchronization Hardening
- [x] 3.1 Ingest Governance-as-Code schema and automated validation into `skills/governance/SKILL.md`.
- [x] 3.2 Ingest SSOT Drift Detection Matrix into `skills/agents-md-management/SKILL.md`.
- [x] 3.3 Create canonical policy file `.github/governance/agent-policies.json`.

### Phase 4: Validation, Batch Audit & Ledger Recalculation
- [x] 4.1 Execute `scripts/batch_skill_auditor.py` over Batch 1 skills.
- [x] 4.2 Verify all 8 skills achieve Score $\ge 96.0/100$ (Grade S).
- [x] 4.3 Synchronize `docs/audit/skills/SKILL_AUDIT_LEDGER.md`.
- [x] 4.4 Run test suite and pages build.
