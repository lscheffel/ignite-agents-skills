---
name: adr-architecture-elevation
version: 1.0.0
description: Independent Architecture Adversarial Review, Design Space Exploration and Decision Set Amplification. Reconstructs problems from first principles, challenges ADR Decision Sets (ADR/BP/PI/TODO), explores architectural alternatives, conducts comparative matrix evaluation, amplifies winning solutions and produces hardened, certified Decision Sets.
domain: domain-stack
triggers:
  - adr-architecture-elevation
  - elevate-adr
  - challenge-architecture
  - adversarial-architecture-review
  - elevar-adr
  - desafio-arquitetural
  - revisao-arquitetural-adversarial
  - decision-set-amplification
tags:
  - architecture
  - adr
  - adversarial-review
  - design-space
  - decision-set
  - amplification
  - governance
  - sota
related_skills:
  - adr-generator
  - adr-archive
  - architecture-review
  - systematic-debugging
  - implementation
  - governance
metadata:
  author: Antigravity Architecture / SOTA
  provenance: internal
  last_audited: "2026-08-26"
---

# ADR Architecture Elevation — Independent Architecture Challenger (SOTA Edition)

## Purpose

Transform an ADR Decision Set from "functional" to "industrial-grade" through an 8-phase independent architecture challenge process. This skill does not merely validate — it reconstructs, challenges, explores alternatives, compares, amplifies, reconciles, and re-audits to certify the solution is the best reasonable approach given constraints.

---

## When to Use

### Use when:
- An agent has produced an ADR Decision Set (ADR + Blueprint + Plan + TODO) and you need independent architectural challenge
- The stakes are high enough to justify a second architectural intelligence (production systems, core infrastructure, irreversible decisions)
- You suspect the solution may be locally correct but globally suboptimal
- You need to prove whether a materially better alternative exists before committing to implementation
- You want to elevate a "working" architecture to "SOTA execution-grade" through systematic amplification

### Do not use when:
- Creating initial ADR scaffolding from scratch (use `adr-generator`)
- Simple code style or linting checks (use `clean-code` or `code-review-lite`)
- Archiving already completed and executed ADRs (use `adr-archive`)

---

## Decision Tree

```mermaid
graph TD
    A[ADR Decision Set Submitted] --> B[Phase 1: Independent Problem Model]
    B --> C[Phase 2: Existing Decision Set Audit]
    C --> D[Phase 3: Architecture Challenge & Alternatives]
    D --> E[Phase 4: Comparative Architecture Evaluation Matrix]
    E --> F{Phase 6: Decision}
    F -->|KEEP| G[Certify Original Solution]
    F -->|KEEP + AMPLIFY| H[Phase 5: Amplification Register]
    F -->|MODIFY| H
    F -->|REPLACE| H
    H --> I[Phase 7: Hardened Decision Set]
    I --> J[Phase 8: Re-Audit & Certification Gate]
```

---

## The 8-Phase Pipeline

### Phase 1 — Independent Problem Model (Reconstruction)

**Mandatory first step.** Do not read the existing ADR as truth. Extract and build your own problem representation:

```text
Problem Statement
Goals (primary, secondary, tertiary)
Constraints (hard, soft, regulatory, budget, timeline)
Invariants (must always hold)
Non-goals (explicitly out of scope)
Actors (human, system, external)
Inputs (data, events, triggers)
Outputs (deliverables, side effects, state changes)
State (persistent, ephemeral, distributed)
Dependencies (upstream, downstream, lateral)
Failure Conditions (what constitutes failure)
Operational Requirements (SLOs, SLAs, observability, recovery)
```

Output: `Phase1_Independent_Problem_Model.md`

### Phase 2 — Existing Decision Set Audit

Compare the existing Decision Set against your independent problem model:

```text
For each artifact (ADR, BP, PI, TODO):
  - Correctness: Does it solve the stated problem?
  - Completeness: Are all problem dimensions addressed?
  - Coherence: Do artifacts agree with each other?
  - Implementability: Can this be built as specified?
  - Robustness: Does it handle failure conditions?
  - Traceability: Can every decision trace to a goal/constraint?
```

Output: `Phase2_Audit_Report.md` with findings categorized as CRITICAL / MAJOR / MINOR / OBSERVATION

### Phase 3 — Architecture Challenge (Adversarial Review)

Assume the existing architecture may be locally correct but globally suboptimal. Actively search for:

**A. Architectural Alternatives** (at least 2, max 5):
- Does an approach exist that reduces complexity/coupling/cost?
- Does an approach exist that improves reliability/testability/extensibility?
- Does an approach exist that eliminates a dependency or failure surface?
- Is the current approach over-engineered for the actual problem?

**B. Implementation Alternatives** (same architecture, better execution):
- Substantially better patterns, libraries, or techniques?

**C. Generalization Opportunities**:
- Is the design excessively specific? Can it solve a broader class?

**D. Simplification Opportunities**:
- Can the problem be solved more simply without loss of capability?

**E. Anticipation Opportunities**:
- Predictable future needs that should inform current boundaries?

**Constraint**: Alternatives must earn their complexity. Use the Comparative Evaluation Matrix (Phase 4).

Output: `Phase3_Architecture_Challenge.md` documenting each alternative with rationale.

### Phase 4 — Comparative Architecture Evaluation

Evaluate Original (A) vs Alternatives (B, C...) against the matrix:

| Criterion | Current (A) | Alt B | Alt C | Winner |
|---|:---:|:---:|:---:|:---:|
| Correctness | | | | |
| Complexity (code/ops) | | | | |
| Robustness | | | | |
| Testability | | | | |
| Operability | | | | |
| Performance | | | | |
| Security | | | | |
| Maintainability | | | | |
| Cost (build/run) | | | | |
| Reversibility | | | | |
| Operational Complexity | | | | |

**Rule**: Do not recommend an alternative merely because it is different. The alternative must demonstrate material gain on multiple criteria without unjustified complexity.

Output: `Phase4_Comparative_Evaluation.md` with scored matrix and recommendation.

### Phase 5 — Amplification Register

Amplification ≠ Expansion. Amplification means increasing architectural quality, robustness, capability, or future leverage **without unjustified complexity or scope expansion**.

Seek five amplification types:

1. **Completeness Amplification**: Add necessary requirements not explicitly stated; close gaps between problem model and solution.
2. **Robustness Amplification**: Add protection against failures, concurrency, corruption, intermediate states, retries, restarts, stampedes, cascading failures.
3. **Capability Amplification**: Discover capabilities that significantly improve outcome without altering core.
4. **Architectural Amplification**: Improve boundaries, abstractions, contracts, decoupling, extensibility.
5. **Operational Amplification**: Add observability, diagnostics, rollout/rollback, metrics, health checks, recovery procedures.
6. **Opportunity Discovery**: Classify collateral capabilities as NOW / LATER / DO NOT DO.

Output: `Phase5_Amplification_Register.md` with specific, actionable amplifications.

### Phase 6 — Decision

One of:
- **KEEP** — No material improvement demonstrated.
- **KEEP + AMPLIFY** — Original stands, apply amplifications.
- **MODIFY** — Original architecture, significant changes from amplification.
- **REPLACE** — Alternative architecture demonstrably superior.

Output: `Phase6_Decision.md` with justification.

### Phase 7 — Hardened Decision Set

Produce the final, amplified artifacts:
- `ADR-HARDENED.md` — Updated ADR with all amplifications integrated
- `BP-HARDENED.md` — Updated Blueprint with implementation-grade detail
- `PI-HARDENED.md` — Updated Plan with amplification tasks
- `TODO-HARDENED.md` — Updated TODO with execution-ready items

### Phase 8 — Re-Audit

Audit your own hardened decision set against the independent problem model (Phase 1). Verify:
- All amplifications are integrated and consistent
- No new gaps introduced
- Complexity remains justified
- Traceability maintained end-to-end

Output: `Phase8_Reaudit_Report.md` — Certification or required fixes.

---

## Anti-Patterns & Pitfalls

| Severity | Anti-Pattern | Description & Remediation |
|---|---|---|
| 🔴 **CRITICAL** | **Rubber-Stamping / Confirmation Bias** | Accepting the input ADR's assumptions without independent first-principles problem reconstruction. **Remedy**: Always complete Phase 1 before deep analysis. |
| 🔴 **CRITICAL** | **Scope Creep as Amplification** | Adding heavy infrastructure, microservices, or unwanted third-party dependencies disguised as "improvements". **Remedy**: Enforce that every amplification must earn its complexity in Phase 4. |
| 🟡 **ALARM** | **Novelty Bias** | Recommending an alternative simply because it uses newer or more fashionable technology without measurable trade-off gains. |
| 🟢 **GENTLE** | **Dismissing KEEP Outcomes** | Believing an evaluation is only valuable if it proposes massive rewrites. Certifying a truly sound architecture with minor hardening is an optimal result. |

---

## Checklists & Verification Gates

### Pre-Challenge Checklist
- [ ] ADR Decision Set (ADR, BP, PI, TODO) present and accessible
- [ ] Problem domain, constraints, and runtime environment identified
- [ ] Independent Problem Model (Phase 1) completed without reading ADR implementation details

### Post-Challenge Quality Gate
- [ ] At least 2 architectural alternatives rigorously compared in Phase 4 matrix
- [ ] Amplifications mapped to specific robustness, operational, or architectural gaps
- [ ] Final Decision Set (`ADR-HARDENED`, `BP-HARDENED`, `PI-HARDENED`, `TODO-HARDENED`) internally consistent
- [ ] Phase 8 Re-audit certified with zero CRITICAL findings

---

## Output Structure

```text
architecture-elevation-report/
├── Phase1_Independent_Problem_Model.md
├── Phase2_Audit_Report.md
├── Phase3_Architecture_Challenge.md
├── Phase4_Comparative_Evaluation.md
├── Phase5_Amplification_Register.md
├── Phase6_Decision.md
├── Phase7_Hardened_Decision_Set/
│   ├── ADR-HARDENED.md
│   ├── BP-HARDENED.md
│   ├── PI-HARDENED.md
│   └── TODO-HARDENED.md
├── Phase8_Reaudit_Report.md
└── EXECUTIVE_SUMMARY.md
```

---

## Reference Files & Scripts

- [`references/evaluation-criteria.md`](./references/evaluation-criteria.md) — Detailed rubrics for the Comparative Evaluation Matrix
- [`references/amplification-patterns.md`](./references/amplification-patterns.md) — Catalog of common amplification patterns by type
- [`references/anti-patterns.md`](./references/anti-patterns.md) — Common architectural anti-patterns to detect during challenge
- [`references/output-templates.md`](./references/output-templates.md) — Templates for each phase output document
- [`scripts/run_elevation.py`](./scripts/run_elevation.py) — Orchestrates the 8-phase pipeline and produces final package
- [`scripts/comparative_matrix.py`](./scripts/comparative_matrix.py) — Helper for Phase 4 matrix scoring and visualization
- [`scripts/reconstruct_problem.py`](./scripts/reconstruct_problem.py) — Guided problem reconstruction questionnaire

## Edge Cases & Failure Modes

- **Restricted / Read-Only Environment:** If the filesystem or sandbox is write-locked, report the constraint immediately with evidence and generate changes as a markdown diff patch.
- **Specification Conflict:** If contradictions emerge between user intent and the SSOT (`AGENTS.md`), halt and present trade-off options.
- **Context Exhaustion / Timeout:** For massive tasks, decompose into atomic sub-batches utilizing `subagent-driven-development`.



## Completion Gate

The task associated with the skill `adr-architecture-elevation` can only be declared complete when:
1. All checks in the operational verification checklist have been satisfied.
2. The deliverable has been deterministically validated through execution evidence.
3. No structural debt, unresolved placeholders, or unhandled errors remain.



## Architectural Reversibility Algebra & Blast Radius Index (SOTA)

Every architecture decision evaluated under this skill must be quantified using the **Blast Radius Index ($BR$)**:

$$BR = (N_{\text{dependents}} \times 1.5) + (R_{\text{data}} \times 2.0) + (H_{\text{rollback}} \times 0.5)$$

### Reversibility Scoring Rubric:
- **$N_{\text{dependents}}$**: Number of downstream modules, packages, or services consuming this interface directly.
- **$R_{\text{data}}$ (Data Migration Risk)**:
  - `0`: Stateless or ephemeral cache change.
  - `1`: Additive non-breaking schema evolution.
  - `2`: State migration required with dual-write phase.
  - `3`: Destructive database rewrite / irreversible event schema change.
- **$H_{\text{rollback}}$**: Estimated engineer-hours required to safely restore the prior system state.

```text
ELEVATION DECISION GATE:
- If BR < 3.0: Classified as Low Blast Radius (One-Way Door is NOT present). Fast-track elevation.
- If 3.0 <= BR < 7.0: Standard Architectural Decision. Requires 8-phase comparative evaluation matrix.
- If BR >= 7.0: CRITICAL Blast Radius (High Irreversibility). Mandatory Multi-Agent Adversarial Challenge (Red Team / Blue Team).
```

### Multi-Agent Red Team / Blue Team Adversarial Protocol
When $BR \ge 7.0$, spawn an isolated challenger agent:
1. **Blue Team Prompt:** *"Defend Decision Set against failure modes, performance regressions under 10x scale, and maintainability bounds."*
2. **Red Team Prompt:** *"Act as an adversarial principal architect. Find minimum 3 structural flaws, hidden couplings, or catastrophic rollback failure modes in this Decision Set."*

## Domain SOTA & Industry Engineering Standards

This skill adheres strictly to international architecture standards and software engineering best practices:
- **Architecture Evaluation Standard:** ISO/IEC/IEEE 42010 (Systems and software engineering — Architecture description).
- **Security & Threat Invariants:** Compliance with OWASP Top 10 API Security Risks and RFC 7519 / RFC 6749 identity federation protocols.
- **SOLID & Clean Architecture Adherence:** Explicit verification of Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, and Dependency Inversion.
- **Transactional & Event Semantics:** Formal enforcement of ACID guarantees for synchronous state transitions and Idempotency keys (RFC 7231) for asynchronous Event-Driven Architectures.
- **Domain-Driven Design (DDD):** Verification of Bounded Context boundaries, Aggregate roots, and anti-corruption layers.

### Exhaustive Heuristic Decision Rules:
- **Rule of Thumb 1 (Zero-Trust Architectural Boundaries):** Treat all external inputs, third-party payloads, and cross-module boundaries with strict zero-trust schema validation.
- **Rule of Thumb 2 (Fail-Fast & Deterministic Errors):** Reject invalid states immediately with typed, actionable error contracts rather than cascading silent failures.
- **Rule of Thumb 3 (Idempotency & AST Preservation):** State mutations and code transformations must maintain semantic idempotency across repeated executions.
- **Rule of Thumb 4 (Benchmark & Telemetry Alignment):** Measure critical execution latency ($P_{95}$) and memory overhead with structured telemetry and baseline benchmarks.
- **Rule of Thumb 5 (Event-Driven & Circuit Breaker Decoupling):** Isolate asynchronous operations behind circuit breakers and resilient retry mechanisms to prevent cascading failure.
- **Rule of Thumb 6 (Contract-First DDD Modeling):** Define clear domain aggregates, value objects, and typed interface contracts before implementing concrete logic.
- **Rule of Thumb 7 (RAG & Semantic Retrieval Precision):** Optimize context retrieval with hybrid lexical-vector search and reciprocal rank fusion to eliminate hallucinated routing.
- **Rule of Thumb 8 (OWASP & Supply Chain Verification):** Verify dependencies and data flows against OWASP Top 10 and SLSA Level 3 supply chain security standards.
- **Rule of Thumb 9 (Verification Gate Invariant):** Never declare completion without automated test execution evidence and zero compiler/linter warnings.

- **Rule of Thumb 1 (Reversibility Invariant):** If a decision cannot be reversed within $H_{\text{rollback}} \le 2$ hours without data loss, it is a One-Way Door and MUST undergo independent adversarial review.
- **Rule of Thumb 2 (Blast Radius Containment):** If $N_{\text{dependents}} \ge 3$, the interface must introduce an Anti-Corruption Layer (ACL) to shield legacy consumers.
- **Rule of Thumb 3 (State Migration Idempotency):** Every database migration script must be strictly idempotent and re-runnable with zero data drift.
- **Rule of Thumb 4 (Cognitive Budget Limit):** The architectural decision payload must maintain a Signal-to-Noise Ratio (SNR) $> 0.85$, removing speculative fluff.