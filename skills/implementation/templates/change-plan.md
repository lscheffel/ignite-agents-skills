# Change Plan

> Internal execution plan built from the analysis of dependencies of the TODO.

---

## Identification

| Field | Value |
|-------|-------|
| ADR | {{adr_path}} |
| Date of generation | {{date}} |
| Total tasks | {{total_tasks}} |
| Total estimate | {{total_estimate}} |

---

## Execution DAG

```mermaid
graph LR
{{#each dag_nodes}}
    {{id}}[{{label}}]{{#if edges}} --> {{target}}{{/if}}
{{/each}}
```

### Legend

| Color | Meaning |
|-------|---------|
| ⬜ | Pending |
| 🔄 | In progress |
| ✅ | Completed |
| ❌ | Blocked |

---

## Execution Order

| Phase | Tasks | Dependencies | Estimated Time |
|------|---------|--------------|----------------|
{{#each phases}}
| {{number}} | {{tasks}} | {{dependencies}} | {{estimate}} |
{{/each}}

---

## Detailed Tasks

| # | Task | Status | Dependencies | Priority | Estimate | Files |
|---|--------|--------|--------------|------------|------------|----------|
{{#each tasks}}
| {{number}} | {{name}} | {{status}} | {{deps}} | {{priority}} | {{estimate}} | {{files}} |
{{/each}}

---

## Parallelizable Tasks

| Phase | Tasks that can run in parallel |
|------|--------------------------------------|
{{#each parallel_tasks}}
| {{phase}} | {{tasks}} |
{{/each}}

---

## Checkpoints

| After Task | Verify | Criterion |
|-------------|-----------|----------|
{{#each checkpoints}}
| {{after_task}} | {{check}} | {{criterion}} |
{{/each}}

---

## Detailed Estimate

| Component | Estimated Time | Notes |
|------------|------------|-------|
| Infrastructure tasks | {{infra_estimate}} | Creating structure |
| Implementation tasks | {{impl_estimate}} | Main code |
| Validation tasks | {{validation_estimate}} | Tests and verification |
| Documentation tasks | {{docs_estimate}} | Updating docs |
| Buffer (20%) | {{buffer}} | Unforeseen events |
| **Total** | **{{total}}** | |

---

## Plan Risks

| # | Risk | Impact on Plan | Mitigation |
|---|-------|------------------|-----------|
{{#each plan_risks}}
| {{number}} | {{risk}} | {{impact}} | {{mitigation}} |
{{/each}}

---

## Plan Validation

- [ ] DAG constructed without cycles
- [ ] All tasks have defined dependencies
- [ ] Estimates sum to the expected total
- [ ] Parallelizable tasks are truly independent
- [ ] Checkpoints cover critical tasks
- [ ] Plan risks are documented