---
id: ADR-{{id}}-TODO
type: todo
title: "Execution - {{title}}"
created: {{date}}
updated: {{date}}
adr_ref: ADR-{{id}}
---

# ADR-{{id}}-TODO: Execution - {{title}}

> Reference: [ADR-{{id}}](./ADR-{{id}}.md) | Status: ⬜ PENDING

> **Elastic Structure:** The Phases and Steps below are an example skeleton, not a mandatory count. Use as many Phases as the real scope of the decision requires – a small decision may have a single Phase with two or three tasks; a large decision may have several. Do not create tasks just to fill the structure (see anti-pattern "TODO with Fabricated Phases").

## Legend

- ✅ Completed
- ⬜ Pending
- 🔄 In Progress
- ❌ Blocked
- ⏸️ Paused

**Priority:** 🔴 High | 🟡 Medium | 🟢 Low

---

## Phase {{phase_1_letter}}: {{phase_1_title}}

### {{phase_1_letter}}1: {{phase_1_subtitle}}

| # | Task | Status | Priority | Dependencies | Estimation |
|---|--------|--------|------------|--------------|------------|
| {{phase_1_letter}}1.1 | {{task_1}} | ⬜ | 🔴 | — | {{time_1}} |
| {{phase_1_letter}}1.2 | {{task_2}} | ⬜ | 🔴 | {{phase_1_letter}}1.1 | {{time_2}} |

**Checkpoint {{phase_1_letter}}1:**
- [ ] {{checkpoint_1}}

<!--
Repeat the block "### {{phase_1_letter}}N: {{subtitle}}" for each additional sub-group of tasks within this Phase, and repeat the entire section "## Phase {{letra}}" for each additional Phase that the real scope requires. Each Phase ends with a General Checkpoint:

**General Checkpoint for Phase {{phase_1_letter}}:**
- [ ] {{checkpoint_general}}
-->

---

## General Summary

| Phase | Tasks | Estimated Hours | Status |
|------|---------|------------|--------|
| Phase {{phase_1_letter}}: {{phase_1_title}} | {{count_1}} | ~{{hours_1}} | ⬜ |
| **Total** | **{{total}}** | **~{{total_hours}}** | |

<!-- Add a line for each real Phase. -->

---

## Dependencies between Phases

> Only include this diagram if there are more than one Phase with real dependencies between them. For a single-Phase TODO, omit this section.

```
Phase {{phase_1_letter}} ({{phase_1_title}})
  │
  └─── {{phase_1_letter}}1: {{phase_1_short}} ─────┐
                                                     │
Phase {{phase_2_letter}} ({{phase_2_title}}) ◄───────┘
```

---

*Document generated on {{date}}. Reference: ADR-{{id}}.*