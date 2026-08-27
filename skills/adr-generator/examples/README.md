# ADR Generator Reference Examples Catalog

This directory provides canonical, battle-tested reference implementations demonstrating how to structure, challenge, and govern Architectural Decision Records (ADRs) using the **MADR v3.0** standard.

---

## 1. Catalog of Reference Examples

1. **`adr-generator-example.md`:** 
   - Complete end-to-end scenario demonstrating how an AI coding agent processes technical trade-offs.
   - Evaluates competing architectural alternatives (e.g. SQLite WAL vs Kafka).
   - Synthesizes a hardened Decision Set: ADR, Blueprint (BP), Implementation Plan (PI), and Completion Checklist (TODO).

2. **`adr-blueprint-sample.md`:** 
   - Sample Architectural Blueprint (BP) incorporating C4 component diagrams and Mermaid state machines.
   - Decoupled interface boundary definitions and typed data contracts.

3. **`adr-implementation-plan-sample.md`:** 
   - Sample Phased Implementation Plan (PI) with quantitative milestones and dependency ordering.
   - Granular verification gates for deterministic completion.

---

## 2. Best Practices & Decision Governance
- Every ADR must explicitly articulate **Negative Consequences** and trade-offs alongside positive drivers.
- All Decision Sets must maintain 1-to-1 traceability with implementation tasks in `TODO.md`.
- Upon successful implementation, use `adr-archive` to certify the decision with an Evidence Record (`ER.md`).
- Never merge an unverified architectural change without a corresponding ADR when structural trade-offs exist.