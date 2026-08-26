---
name: adr-architecture-elevation
description: This skill implements an independent Architecture Adversarial Review + Design Space Exploration + Decision Set Amplification process. It acts as a second, independent architectural intelligence that reconstructs the problem from first principles, challenges the existing ADR Decision Set (ADR/BP/PI/TODO), explores alternative architectures, performs comparative evaluation, amplifies the winning solution with robustness/completeness/operational improvements, and produces a hardened, re-audited Decision Set. Use when an agent has produced an ADR Decision Set and you need to determine if it is locally optimal within the reasonable solution space — not merely "correct" but genuinely the best reasonable approach. Triggers: "audit this ADR", "challenge this architecture", "elevate this decision set", "architecture review", "adversarial review", "design space exploration", "decision set amplification", "SOTA architecture review".
---

# ADR Architecture Elevation — Independent Architecture Challenger

## Purpose

Transform an ADR Decision Set from "functional" to "industrial-grade" through an 8-phase independent architecture challenge process. This skill does not merely validate — it reconstructs, challenges, explores alternatives, compares, amplifies, reconciles, and re-audits to certify the solution is the best reasonable approach given constraints.

## Trigger Conditions

Invoke this skill when:
- An agent has produced an ADR Decision Set (ADR + Blueprint + Plan + TODO) and you need independent architectural challenge
- The stakes are high enough to justify a second architectural intelligence (production systems, core infrastructure, irreversible decisions)
- You suspect the solution may be locally correct but globally suboptimal
- You need to prove whether a materially better alternative exists before committing to implementation
- You want to elevate a "working" architecture to "SOTA execution-grade" through systematic amplification

## The 8-Phase Pipeline

### Phase 1 — Independent Problem Model (Reconstruction)

**Mandatory first step.** Do not read the existing ADR as truth. Extract and build your own problem representation:

```
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

```
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

Output: `Phase3_Architecture_Challenge.md` documenting each alternative with rationale

### Phase 4 — Comparative Architecture Evaluation

Evaluate Original (A) vs Alternatives (B, C...) against the matrix:

| Criterion | Current (A) | Alt B | Alt C | Winner |
|-----------|-------------|-------|-------|--------|
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

Output: `Phase4_Comparative_Evaluation.md` with scored matrix and recommendation

### Phase 5 — Amplification Register

Amplification ≠ Expansion. Amplification means increasing architectural quality, robustness, capability, or future leverage **without unjustified complexity or scope expansion**.

Seek five amplification types:

**1. Completeness Amplification**
- Add necessary requirements not explicitly stated
- Close gaps between problem model and solution

**2. Robustness Amplification**
- Add protection against: failures, concurrency, corruption, intermediate states, retries, restarts, stampede, cascading failures

**3. Capability Amplification**
- Discover capabilities that significantly improve outcome without altering core

**4. Architectural Amplification**
- Improve boundaries, abstractions, contracts, decoupling, extensibility

**5. Operational Amplification**
- Add observability, diagnostics, rollout/rollback, metrics, health checks, recovery procedures

**6. Opportunity Discovery** (bonus)
- What does this architecture build that could solve other problems?
- Classify: NOW / LATER / DO NOT DO

Output: `Phase5_Amplification_Register.md` with specific, actionable amplifications

### Phase 6 — Decision

One of:
- **KEEP** — No material improvement demonstrated
- **KEEP + AMPLIFY** — Original stands, apply amplifications
- **MODIFY** — Original architecture, significant changes from amplification
- **REPLACE** — Alternative architecture demonstrably superior

Output: `Phase6_Decision.md` with justification

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

Output: `Phase8_Reaudit_Report.md` — Certification or required fixes

## Output Structure

The skill produces a complete audit package:

```
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

## Execution Protocol

### Input Requirements

The skill expects as input:
1. The ADR Decision Set directory containing: `ADR.md`, `BP.md`, `PI.md`, `TODO.md`
2. Any supporting context (requirements docs, constraints, existing architecture docs)

### Agent Behavior Rules

1. **Never assume the input ADR is correct** — Treat it as a hypothesis to test
2. **Reconstruct independently first** — Phase 1 must complete before reading the ADR in detail
3. **Challenge aggressively, recommend conservatively** — Explore broadly, only adopt what earns its place
4. **Amplification is not expansion** — Do not add features, abstractions, or infrastructure merely because they could theoretically help
5. **Document the negative space** — Record alternatives considered and rejected with reasoning
6. **KEEP is a valid, honorable outcome** — If the original is genuinely optimal, certify it

### Quality Gates

Each phase must pass its quality gate before proceeding:

- **Phase 1 Gate**: Problem model covers all 11 dimensions with specificity
- **Phase 2 Gate**: Every finding mapped to problem model dimension
- **Phase 3 Gate**: At least 2 alternatives explored with architectural rationale
- **Phase 4 Gate**: Matrix complete with evidence-based scoring
- **Phase 5 Gate**: Each amplification traced to a specific gap or opportunity
- **Phase 6 Gate**: Decision justified by comparative evidence
- **Phase 7 Gate**: All artifacts internally consistent and traceable
- **Phase 8 Gate**: Re-audit passes with zero CRITICAL findings

## Reference Files

This skill includes supporting references in `references/`:

- `evaluation-criteria.md` — Detailed rubrics for the Comparative Evaluation Matrix
- `amplification-patterns.md` — Catalog of common amplification patterns by type
- `anti-patterns.md` — Common architectural anti-patterns to detect during challenge
- `output-templates.md` — Templates for each phase output document

## Scripts

- `scripts/run_elevation.py` — Orchestrates the 8-phase pipeline, manages state, produces final package
- `scripts/comparative_matrix.py` — Helper for Phase 4 matrix scoring and visualization
- `scripts/reconstruct_problem.py` — Guided problem reconstruction questionnaire

## Usage Example

```
User: "Audit and elevate this ADR Decision Set for the translation pipeline"
Agent: [Loads skill, reads input ADR/BP/PI/TODO, executes 8-phase pipeline]
Output: Complete architecture-elevation-report/ with hardened decision set
```

## Integration Notes

- This skill is designed for use by a second, independent agent instance (the "challenger")
- The challenger should have no prior context on the problem — fresh reconstruction is essential
- Works with any ADR format that follows the standard structure (Context, Decision, Consequences, Status)
- Compatible with the `adr-generator`, `adr-archive`, and `implementation` skills
- Output feeds directly into `implementation` skill for execution-grade delivery