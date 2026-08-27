# ADR-032 Implementation Plan (PI): Engineering, Coding & Quality Domain SOTA

> **Companion Artifact to:** [ADR-032.md](./ADR-032.md) & [ADR-032-BP.md](./ADR-032-BP.md)  
> **Type:** Phased Implementation Plan (Tier II)  
> **Status:** READY FOR EXECUTION  

---

## 1. Execution Phases

### Phase 1: Code Quality, Complexity Bounds & Refactoring
- [x] 1.1 Ingest Thomas McCabe Cyclomatic Complexity ($CC \le 10$) and Sonar Cognitive Complexity rules into `skills/clean-code/SKILL.md`.
- [x] 1.2 Ingest Martin Fowler's Refactoring transformations and Strangler Fig patterns into `skills/refactoring/SKILL.md`.
- [x] 1.3 Ingest Atomic Change Transaction protocol and Evidence Record handoffs into `skills/implementation/SKILL.md`.

### Phase 2: Scientific Debugging & Root Cause Analysis
- [x] 2.1 Ingest Scientific Debugging Method, Git Bisect search algebra ($O(\log N)$), and RCA 5-Whys into `skills/systematic-debugging/SKILL.md`.

### Phase 3: Testing Invariants, Mutation Scores & Test Pyramid
- [x] 3.1 Ingest Kent Beck TDD invariants and Mutation Score ($MS \ge 0.85$) into `skills/test-driven-development/SKILL.md`.
- [x] 3.2 Ingest Mike Cohn Test Pyramid ratio algebra ($70/20/10$) and Property-Based Testing into `skills/testing-mastery/SKILL.md`.

### Phase 4: Code Review Standards, Taxonomies & Workflows
- [x] 4.1 Ingest Google Engineering Practices 3-Tier severity taxonomy (P1/P2/P3) into `skills/code-review/SKILL.md`.
- [x] 4.2 Ingest PR Fast-Path algebra ($N_{\text{lines}} \le 200$) into `skills/code-review-lite/SKILL.md`.
- [x] 4.3 Ingest Multi-Round Review FSM and consensus gates into `skills/code-review-workflow/SKILL.md`.

### Phase 5: Validation, Batch Audit & Ledger Recalculation
- [x] 5.1 Execute `scripts/batch_skill_auditor.py` over Batch 3 skills.
- [x] 5.2 Verify all 9 skills achieve Grade B+ / A / S (Target Catalog Average > 85.0).
- [x] 5.3 Synchronize `docs/audit/skills/SKILL_AUDIT_LEDGER.md`.
- [x] 5.4 Run full test suite and pages build.
