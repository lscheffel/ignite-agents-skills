# Output Templates — Phase Document Structures

## Purpose

Standardized templates for each phase output document. Ensures consistency, completeness, and traceability across the 8-phase pipeline.

---

## Phase 1: Independent Problem Model

```markdown
# Phase 1 — Independent Problem Model

## Problem Statement
[One paragraph: what problem is actually being solved?]

## Goals
### Primary (Must Achieve)
- [Goal 1 with measurable success criterion]
- [Goal 2 with measurable success criterion]

### Secondary (Should Achieve)
- [Goal 3 with measurable success criterion]

### Tertiary (Nice to Have)
- [Goal 4 with measurable success criterion]

## Constraints
### Hard (Non-Negotiable)
- [Constraint 1: regulatory, budget, timeline, technical]

### Soft (Negotiable with Trade-off)
- [Constraint 2: preference, optimization target]

## Invariants (Must Always Hold)
- [Invariant 1: e.g., "No data loss under any failure mode"]
- [Invariant 2: e.g., "All mutations are idempotent"]

## Non-Goals (Explicitly Out of Scope)
- [Non-goal 1 with rationale]
- [Non-goal 2 with rationale]

## Actors
| Actor | Type | Responsibilities | Interactions |
|-------|------|------------------|--------------|
| [Name] | Human/System/External | [What they do] | [With whom] |

## Inputs
| Input | Source | Format | Frequency | SLA |
|-------|--------|--------|-----------|-----|
| [Name] | [Source] | [Format] | [Freq] | [SLA] |

## Outputs
| Output | Consumer | Format | Frequency | SLA |
|--------|----------|--------|-----------|-----|
| [Name] | [Consumer] | [Format] | [Freq] | [SLA] |

## State
| State Entity | Persistence | Consistency | Access Pattern |
|--------------|-------------|-------------|----------------|
| [Name] | [Persistent/Ephemeral/Distributed] | [Strong/Eventual] | [Read/Write/Both] |

## Dependencies
### Upstream
- [Dependency 1: what we consume, SLA, failure mode]

### Downstream
- [Dependency 2: what consumes us, SLA, failure mode]

### Lateral
- [Dependency 3: peer systems, integration pattern]

## Failure Conditions
| Condition | Detection | Impact | Recovery |
|-----------|-----------|--------|----------|
| [What fails] | [How detected] | [User/System impact] | [Recovery procedure] |

## Operational Requirements
| Requirement | Target | Measurement |
|-------------|--------|-------------|
| Availability | [e.g., 99.9%] | [How measured] |
| Latency (p99) | [e.g., < 200ms] | [How measured] |
| Throughput | [e.g., 10k req/s] | [How measured] |
| Durability | [e.g., 11 9s] | [How measured] |
| Observability | [Specific requirements] | [How verified] |
| Recovery (RTO/RPO) | [e.g., RTO<5min, RPO=0] | [How verified] |
```

---

## Phase 2: Audit Report

```markdown
# Phase 2 — Existing Decision Set Audit Report

## Input Artifacts Audited
- ADR: [path/version]
- BP: [path/version]
- PI: [path/version]
- TODO: [path/version]

## Audit Methodology
[Brief description of comparison approach]

## Findings Summary
| Severity | Count |
|----------|-------|
| CRITICAL | [N] |
| MAJOR | [N] |
| MINOR | [N] |
| OBSERVATION | [N] |

## Detailed Findings

### CRITICAL Findings
#### FINDING-001: [Title]
**Dimension**: [Problem model dimension affected]
**Artifact**: [ADR/BP/PI/TODO section]
**Description**: [What is wrong/missing]
**Evidence**: [Specific reference to artifact text]
**Impact**: [Consequence if unaddressed]
**Recommendation**: [Specific fix]

### MAJOR Findings
#### FINDING-002: [Title]
[Same structure as CRITICAL]

### MINOR Findings
#### FINDING-003: [Title]
[Same structure]

### OBSERVATIONS
#### OBS-001: [Title]
[Same structure; lower priority]

## Traceability Matrix
| Problem Model Element | ADR Coverage | BP Coverage | PI Coverage | TODO Coverage | Gap? |
|----------------------|--------------|-------------|-------------|---------------|------|
| Goal 1 | ✅/❌/⚠️ | ✅/❌/⚠️ | ✅/❌/⚠️ | ✅/❌/⚠️ | [Yes/No] |
| Constraint 1 | ... | ... | ... | ... | ... |
| Invariant 1 | ... | ... | ... | ... | ... |
| Failure Condition 1 | ... | ... | ... | ... | ... |

## Overall Assessment
[Summary: Does the decision set adequately address the problem model?]
```

---

## Phase 3: Architecture Challenge

```markdown
# Phase 3 — Architecture Challenge

## Current Architecture Summary
[1-2 paragraph summary of the existing ADR/BP approach]

## Independent Problem Model Reference
[Link to Phase 1 output; key constraints/invariants that drive challenge]

## Alternative Architectures Explored

### Alternative A: [Name]
**Type**: [Architectural / Implementation / Generalization / Simplification / Anticipation]
**Core Idea**: [One-sentence essence]
**Key Differences from Current**:
- [Difference 1]
- [Difference 2]
**Rationale**: [Why this alternative exists]
**Complexity Assessment**: [Higher/Lower/Same + justification]
**Risk Assessment**: [New risks introduced]

### Alternative B: [Name]
[Same structure]

### Alternative C: [Name] (if applicable)
[Same structure]

## Alternatives Considered but Rejected

### Rejected: [Name]
**Reason**: [Why rejected — not viable, too complex, doesn't solve problem, etc.]

## Anti-Patterns Detected in Current Architecture
| Anti-Pattern | Evidence | Consequence | Remediation Effort |
|--------------|----------|-------------|-------------------|
| [Name] | [Specific evidence] | [If unaddressed] | [Low/Medium/High] |

## Generalization Opportunities
| Opportunity | Current Specificity | Generalized Form | Value | Decision (NOW/LATER/DO NOT DO) |
|-------------|---------------------|------------------|-------|-------------------------------|
| [Description] | [Current] | [Generalized] | [Why valuable] | [Decision] |

## Simplification Opportunities
| Opportunity | Current Complexity | Simplified Form | Trade-off | Decision |
|-------------|-------------------|-----------------|-----------|----------|
| [Description] | [Current] | [Simpler] | [What lost] | [Decision] |

## Anticipation Opportunities
| Future Need | Current Gap | Pre-emptive Design | Cost Now | Value Later | Decision |
|-------------|-------------|-------------------|----------|-------------|----------|
| [Description] | [Gap] | [What to add] | [Cost] | [Value] | [Decision] |
```

---

## Phase 4: Comparative Evaluation

```markdown
# Phase 4 — Comparative Architecture Evaluation

## Evaluation Context
**Problem**: [Reference Phase 1]
**Alternatives Evaluated**: [Current A, Alternative B, Alternative C...]
**Weighting Scheme**: [Default or custom with justification]

## Scoring Matrix

| Criterion | Weight | Current (A) | Alt B | Alt C | Winner |
|-----------|--------|-------------|-------|-------|--------|
| Correctness | [%] | [Score]/5 | [Score]/5 | [Score]/5 | [A/B/C] |
| Complexity | [%] | [Score]/5 | [Score]/5 | [Score]/5 | [A/B/C] |
| Robustness | [%] | [Score]/5 | [Score]/5 | [Score]/5 | [A/B/C] |
| Testability | [%] | [Score]/5 | [Score]/5 | [Score]/5 | [A/B/C] |
| Operability | [%] | [Score]/5 | [Score]/5 | [Score]/5 | [A/B/C] |
| Performance | [%] | [Score]/5 | [Score]/5 | [Score]/5 | [A/B/C] |
| Security | [%] | [Score]/5 | [Score]/5 | [Score]/5 | [A/B/C] |
| Maintainability | [%] | [Score]/5 | [Score]/5 | [Score]/5 | [A/B/C] |
| Cost | [%] | [Score]/5 | [Score]/5 | [Score]/5 | [A/B/C] |
| Reversibility | [%] | [Score]/5 | [Score]/5 | [Score]/5 | [A/B/C] |
| Operational Complexity | [%] | [Score]/5 | [Score]/5 | [Score]/5 | [A/B/C] |
| **WEIGHTED TOTAL** | **100%** | **[Score]** | **[Score]** | **[Score]** | **[Winner]** |

## Evidence for Scores

### Current (A)
**Correctness**: [Evidence for score]
**Complexity**: [Evidence for score]
[... all criteria ...]

### Alternative B
[Same structure]

### Alternative C
[Same structure]

## Veto Check
- Any criterion scored 1 (Critical)? [Yes/No]
- If yes: [Which criterion, which alternative, implication]

## Sensitivity Analysis
[How do results change with ±10% weight variations?]

## Recommendation
**Recommended Architecture**: [A/B/C]
**Justification**: [Evidence-based rationale referencing matrix]
**Confidence**: [High/Medium/Low with reasoning]
**Conditions**: [Any conditions on recommendation]
```

---

## Phase 5: Amplification Register

```markdown
# Phase 5 — Amplification Register

## Amplification Candidates

### Completeness Amplifications
| ID | Gap/Opportunity | Amplification | Type | Effort | Value | Decision |
|----|-----------------|---------------|------|--------|-------|----------|
| CA-001 | [Reference to Phase 2 finding] | [Specific amplification] | [Pattern from catalog] | [S/M/L] | [High/Med/Low] | [NOW/LATER/DO NOT DO] |

### Robustness Amplifications
| ID | Gap/Opportunity | Amplification | Type | Effort | Value | Decision |
|----|-----------------|---------------|------|--------|-------|----------|
| RA-001 | [Reference] | [Specific] | [Pattern] | [S/M/L] | [H/M/L] | [NOW/LATER/DO NOT DO] |

### Capability Amplifications
| ID | Gap/Opportunity | Amplification | Type | Effort | Value | Decision |
|----|-----------------|---------------|------|--------|-------|----------|
| KA-001 | [Reference] | [Specific] | [Pattern] | [S/M/L] | [H/M/L] | [NOW/LATER/DO NOT DO] |

### Architectural Amplifications
| ID | Gap/Opportunity | Amplification | Type | Effort | Value | Decision |
|----|-----------------|---------------|------|--------|-------|----------|
| AA-001 | [Reference] | [Specific] | [Pattern] | [S/M/L] | [H/M/L] | [NOW/LATER/DO NOT DO] |

### Operational Amplifications
| ID | Gap/Opportunity | Amplification | Type | Effort | Value | Decision |
|----|-----------------|---------------|------|--------|-------|----------|
| OA-001 | [Reference] | [Specific] | [Pattern] | [S/M/L] | [H/M/L] | [NOW/LATER/DO NOT DO] |

### Opportunity Discoveries
| ID | Discovery | Platform/Product/Protocol/Compute | Decision | Rationale |
|----|-----------|-----------------------------------|----------|-----------|
| OD-001 | [Description] | [Category] | [NOW/LATER/DO NOT DO] | [Why] |

## NOW Amplifications Summary (Integrated into Hardened Set)
| ID | Amplification | Affected Artifacts | Integration Notes |
|----|---------------|-------------------|-------------------|
| CA-001 | [Description] | [ADR/BP/PI/TODO sections] | [How to integrate] |

## Complexity Budget Check
**Original Complexity Score**: [From Phase 4]
**Amplification Complexity Delta**: [Estimated]
**Resulting Complexity**: [Must not exceed threshold without exceptional justification]
```

---

## Phase 6: Decision

```markdown
# Phase 6 — Decision

## Decision
**Outcome**: [KEEP / KEEP + AMPLIFY / MODIFY / REPLACE]

## Justification
[Evidence-based rationale referencing Phase 2, 3, 4, 5]

## If KEEP + AMPLIFY
**Amplifications Applied**: [List of NOW amplifications from Phase 5]
**Complexity Impact**: [Assessment]

## If MODIFY
**Architectural Changes**: [Specific modifications to current architecture]
**Amplifications Applied**: [List]
**Rationale for Modification vs Replacement**: [Why not replace entirely]

## If REPLACE
**Replacement Architecture**: [Reference to winning alternative from Phase 4]
**Migration Strategy**: [High-level: Strangler Fig / Big Bang / Parallel Run]
**Risk Mitigation**: [Key risks and mitigations]

## Conditions / Caveats
- [Condition 1]
- [Condition 2]

## Sign-off
**Challenger Agent**: [Model/Instance]
**Date**: [Timestamp]
**Phase 1 Problem Model Hash**: [For traceability]
```

---

## Phase 7: Hardened Decision Set

### ADR-HARDENED.md Template
```markdown
---
adr_id: [ID]
title: [Title]
status: [Proposed/Accepted/Superseded]
date: [YYYY-MM-DD]
decision_set_version: [HARDENED-v1]
phase1_problem_model_hash: [Hash]
---

# [Title]

## Context
[Enhanced with Phase 1 problem model elements; all amplifications integrated]

## Decision
[Clear, unambiguous decision statement]

## Consequences
### Positive
- [Consequence 1]
- [Consequence 2]

### Negative
- [Consequence 1 with mitigation]
- [Consequence 2 with mitigation]

### Neutral / Risks
- [Risk 1 with monitoring/mitigation]

## Amplifications Integrated
| Amplification ID | Description | Section Affected |
|------------------|-------------|------------------|
| CA-001 | [Description] | [Section] |
| RA-001 | [Description] | [Section] |

## Compliance & Traceability
| Problem Model Element | Addressed In | Status |
|----------------------|--------------|--------|
| Goal 1 | [Section] | ✅/⚠️ |
| Invariant 1 | [Section] | ✅/⚠️ |
| Failure Condition 1 | [Section] | ✅/⚠️ |
```

### BP-HARDENED.md Template
```markdown
# Blueprint — HARDENED

## Architecture Overview
[High-level diagram description + component list]

## Component Specifications
### Component: [Name]
**Responsibility**: [Single sentence]
**Interfaces**: [APIs, events, contracts]
**Dependencies**: [Upstream/downstream]
**Data Model**: [Entities, schema ref]
**NFRs**: [Latency, availability, etc.]
**Failure Modes**: [How it fails, detection, recovery]
**Observability**: [Metrics, logs, traces]
**Security**: [AuthZ, encryption, audit]

## Data Architecture
[Schemas, migrations, ownership, flows]

## Infrastructure
[Deployment topology, scaling, networking]

## Cross-Cutting Concerns
[Logging, tracing, config, secrets, feature flags]

## Amplifications Integrated
[Reference Phase 5 NOW items with implementation details]
```

### PI-HARDENED.md Template
```markdown
# Plan — HARDENED

## Phases
### Phase 1: Foundation [Duration]
- [Task 1] — [Owner] — [Dependencies] — [Acceptance Criteria]
- [Task 2] — ...

### Phase 2: Core Implementation [Duration]
...

### Phase 3: Amplification Integration [Duration]
- [Amplification CA-001 implementation]
- [Amplification RA-001 implementation]
...

### Phase 4: Operational Readiness [Duration]
- [Observability implementation]
- [Runbook creation]
- [Load testing]
- [Chaos engineering]
- [DR drill]

### Phase 5: Rollout [Duration]
- [Canary plan]
- [Progressive rollout]
- [Rollback criteria]

## Milestones
| Milestone | Target Date | Criteria |
|-----------|-------------|----------|
| M1: Foundation Complete | [Date] | [Criteria] |
| M2: Core Feature Complete | [Date] | [Criteria] |
| M3: Amplifications Integrated | [Date] | [Criteria] |
| M4: Operational Ready | [Date] | [Criteria] |
| M5: Production Rollout | [Date] | [Criteria] |

## Risk Register
| Risk | Likelihood | Impact | Mitigation | Owner |
|------|------------|--------|------------|-------|
| [Risk] | [H/M/L] | [H/M/L] | [Mitigation] | [Owner] |
```

### TODO-HARDENED.md Template
```markdown
# TODO — HARDENED (Execution-Ready)

## Format
- [ ] **Task ID**: [Unique ID] — [Description] — [Owner] — [Estimate] — [Dependencies] — [Acceptance Criteria] — [Phase]

## Phase 1: Foundation
- [ ] **TASK-001**: [Description] — [Owner] — [Estimate] — [Deps] — [AC] — Phase 1
- [ ] **TASK-002**: ...

## Phase 2: Core Implementation
...

## Phase 3: Amplification Integration
- [ ] **AMP-CA-001**: Implement [CA-001 description] — [Owner] — [Estimate] — [Deps] — [AC] — Phase 3
- [ ] **AMP-RA-001**: Implement [RA-001 description] — [Owner] — [Estimate] — [Deps] — [AC] — Phase 3
...

## Phase 4: Operational Readiness
...

## Phase 5: Rollout
...
```

---

## Phase 8: Re-Audit Report

```markdown
# Phase 8 — Re-Audit Report

## Hardened Decision Set Version
[Reference to Phase 7 artifacts]

## Re-Audit Methodology
[Same as Phase 2 but against hardened set]

## Findings Summary
| Severity | Count | Phase 2 Count | Delta |
|----------|-------|---------------|-------|
| CRITICAL | [N] | [N] | [+/-N] |
| MAJOR | [N] | [N] | [+/-N] |
| MINOR | [N] | [N] | [+/-N] |
| OBSERVATION | [N] | [N] | [+/-N] |

## Critical Findings (Must Fix Before Certification)
[If any CRITICAL — certification blocked]

## Major Findings (Should Fix)
[List with remediation]

## Regression Check
| Phase 2 Finding | Status in Hardened Set | Verified? |
|-----------------|------------------------|-----------|
| FINDING-001 | [Fixed/Partial/Not Fixed] | [Yes/No] |

## Amplification Verification
| Amplification ID | Integrated? | Consistent? | Testable? |
|------------------|-------------|-------------|-----------|
| CA-001 | [Yes/No] | [Yes/No] | [Yes/No] |

## Complexity Verification
**Original Complexity**: [Score]
**Hardened Complexity**: [Score]
**Delta**: [+/-]
**Within Budget?**: [Yes/No]

## Certification
**Status**: [CERTIFIED / CONDITIONAL / REJECTED]
**Conditions** (if CONDITIONAL): [List]
**Next Review**: [Date or trigger]

## Executive Summary
[1-paragraph summary for stakeholders]
```

---

## Executive Summary Template

```markdown
# Architecture Elevation — Executive Summary

## Decision Set
**Original**: [ADR ID / Title]
**Elevated**: [HARDENED version ID]
**Date**: [YYYY-MM-DD]

## Verdict
**Decision**: [KEEP / KEEP + AMPLIFY / MODIFY / REPLACE]
**Certification**: [CERTIFIED / CONDITIONAL / REJECTED]

## Key Findings
- [Finding 1: one sentence]
- [Finding 2: one sentence]
- [Finding 3: one sentence]

## Amplifications Applied
- [Amplification 1: one sentence value statement]
- [Amplification 2: one sentence value statement]

## Risk Reduction
| Risk | Before | After |
|------|--------|-------|
| [Risk 1] | [High/Med/Low] | [High/Med/Low] |
| [Risk 2] | [High/Med/Low] | [High/Med/Low] |

## Complexity Impact
**Original**: [Complexity score]
**Hardened**: [Complexity score]
**Delta**: [+/- with justification]

## Recommendation
[One paragraph: proceed with hardened set, or required actions before proceed]

## Artifacts Produced
- Phase 1-8 reports: [path]
- Hardened Decision Set: [path]
- This Summary: [path]
```