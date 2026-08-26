---
id: ADR-{{id}}-BP
type: bp
title: "Blueprint — {{title}}"
created: {{date}}
updated: {{date}}
adr_ref: ADR-{{id}}
---

# Blueprint — ADR-{{id}}: {{title}}

> Reference: [ADR-{{id}}](./ADR-{{id}}.md)

---

## 1. Overview

### Objective
{{objective}}

### Success Metrics

| Metric | Before | After | Status |
|---------|-------|--------|--------|
| {{metric_1}} | {{before_1}} | {{after_1}} | ⬜ |
| {{metric_2}} | {{before_2}} | {{after_2}} | ⬜ |

---

## 2. Affected Artifact Structure

List the actual files that will be created or modified — not a generic structure. This will be the scope map that the TODO and PI will detail.

```text
{{artifacts_structure}}
```

---

## 3. Key Concepts of the Solution

> Add as many concepts as the reader needs to understand the decision without referring back to the original ADR. Do not force a fixed number — a simple decision may not need any, while a complex one may need several.

### 3.1 {{concept_1_title}}

{{concept_1_description}}

**Configuration / Example:**
```
{{concept_1_config}}
```

<!-- Repeat "3.N {{concept_n_title}}" for each additional relevant concept. -->

---

## 4. Implementation Workflows

> Add as many workflows as the actual scope requires. A simple Blueprint may have only one.

### Workflow 1: {{workflow_1_name}}

**Objective:** {{workflow_1_objective}}

**Steps:**
{{workflow_1_steps}}

**Checkpoint:** {{workflow_1_checkpoint}}

<!-- Repeat "Workflow N" for each additional workflow required. -->

---

## 5. Specific Anti-patterns of this Decision

> Particular implementation risks specific to THIS decision — do not repeat generic anti-patterns already covered by the SKILL.md of the adr-generator.

### Critical

#### {{anti_pattern_1_title}}
**What is it:** {{anti_pattern_1_what}}
**Why it's bad:** {{anti_pattern_1_why}}
**How to avoid:** {{anti_pattern_1_how}}

### Medium

#### {{anti_pattern_2_title}}
**What is it:** {{anti_pattern_2_what}}
**Why it's bad:** {{anti_pattern_2_why}}
**How to avoid:** {{anti_pattern_2_how}}

<!-- Omit the entire section if the decision does not have specific risks beyond the generic ones. -->

---

## 6. Checklists

### Pre-Deploy Checklist

- [ ] {{checklist_pre_1}}
- [ ] {{checklist_pre_2}}

### Post-Deploy Checklist

- [ ] {{checklist_post_1}}
- [ ] {{checklist_post_2}}

---

## 7. Edge Cases

### {{edge_case_1_title}}
**Situation:** {{edge_case_1_situation}}
**Solution:** {{edge_case_1_solution}}
**Exception:** {{edge_case_1_exception}}

<!-- Repeat for each relevant edge case. Omit if none exist. -->

---

## 8. Related Skills

> Only list skills that this Blueprint actually invokes or depends on — not a generic list of skills from the catalog.

| Skill | Relation to this Blueprint |
|-------|------------------------------|
| `{{skill_1}}` | {{skill_1_relation}} |

---

## 9. Risks and Mitigations

| Risk | Impact | Probability | Mitigation |
|-------|---------|---------------|-----------|
| {{risk_1}} | {{impact_1}} | {{likelihood_1}} | {{mitigation_1}} |

---

## 10. References

- {{reference_1}}

---

*Document generated on {{date}}. Reference: ADR-{{id}}.*