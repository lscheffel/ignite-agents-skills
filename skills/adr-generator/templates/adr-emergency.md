---
id: ADR-{{id}}
type: adr
title: "{{title}}"
created: {{date}}
updated: {{date}}
implementation_status: IN_PROGRESS
tier: X
follow_up_deadline: {{follow_up_date}}
# ADR Emergency Template
---

# ADR-{{id}}: {{title}}

> Tier X — ADR Flash (Hotfix Post-Event). Reserved for P0 incidents where the
> code has already been or is being written before there is time to document.
> **Follow-up mandatory:** promote this ADR to a complete Triad (ADR + BP +
> TODO) via Phase 4 (Auto-Repair) by `{{follow_up_date}}`. Until then, treat
> as governance debt of high priority 🔴.

## Status
Accepted (emergency) — pending promotion to Triad

## Data
{{date}}

## Context

### Diagnosis

| Capacity | Status | Evidence |
|------------|--------|----------|
| {{capability}} | ❌ | {{evidence}} |

### Consequences of the Gap

- {{consequence_1}}
- {{consequence_2}}

## Decision

{{decision}}

### Immediate Implementation

```
{{implementation_steps}}
```

## Consequences

### Positive
- {{positive_1}}

### Negative
- {{negative_1}}

### Risks
- **Risk**: {{risk}}
  - **Mitigation**: {{mitigation}}

## References
- {{reference}}
- Follow-up (Phase 4 Auto-Repair): (pending until {{follow_up_date}})