---
id: ADR-{{id}}
type: adr
title: "{{title}}"
created: {{date}}
updated: {{date}}
implementation_status: PENDING
depends_on: []
# ADR Template
---

# ADR-{{id}}: {{title}}

## Status
{{status}}

## Context

### Diagnosis

| Capacity | Status | Evidence |
|------------|--------|----------|
| {{capability_1}} | {{status_1}} | {{evidence_1}} |
| {{capability_2}} | {{status_2}} | {{evidence_2}} |

### Consequences of the Gap

- {{consequence_1}}
- {{consequence_2}}

## Decision

{{decision}}

### Solution Architecture

```
{{context_summary}} → {{action_summary}} → {{result_summary}}
```

### Implementation Details

**Trigger:** {{trigger}}

**Jobs:**
{{jobs}}

## Considered Alternatives

> A minimum of 2 alternatives — see anti-pattern "ADR without Alternatives". This applies even when the decision seems obvious in retrospect.

### Alternative A: {{alt_a_title}}
- **Pros**: {{alt_a_pros}}
- **Cons**: {{alt_a_cons}}

### Alternative B: {{alt_b_title}}
- **Pros**: {{alt_b_pros}}
- **Cons**: {{alt_b_cons}}

### Alternative C: {{alt_c_title}} (Chosen)
- **Pros**: {{alt_c_pros}}
- **Cons**: {{alt_c_cons}}

## Consequences

### Positive
- {{positive_1}}
- {{positive_2}}

### Negative
- {{negative_1}}
- {{negative_2}}

### Risks
- **Risk**: {{risk}}
  - **Mitigation**: {{mitigation}}

## References
- {{reference_1}}
- {{reference_2}}
- Evidence Record: (pending — see Phase 5 of the adr-generator)