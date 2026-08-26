# Execution Report

> Final Report Produced at the End of Governed Implementation.

---

## Summary

| Field | Value |
|-------|-------|
| ADR Reference | {{adr_path}} |
| Start Date | {{start_date}} |
| End Date | {{end_date}} |
| Total Duration | {{total_duration}} |
| Total Tasks | {{total_tasks}} |
| Completed Tasks | {{completed_tasks}} |
| Deferred Tasks | {{deferred_tasks}} |
| Blocked Tasks | {{blocked_tasks}} |
| Completion Rate | {{completion_rate}} |

---

## Completed Tasks

| # | Task | Duration | Attempts | Validations |
|---|--------|---------|------------|------------|
{{#each completed}}
| {{number}} | {{task}} | {{duration}} | {{attempts}} | {{validations}} |
{{/each}}

---

## Deferred Tasks

| # | Task | Justification | Review Date |
|---|--------|---------------|--------------|
{{#each deferred}}
| {{number}} | {{task}} | {{reason}} | {{review_date}} |
{{/each}}

---

## Blocked Tasks

| # | Task | Blocker | Required Action |
|---|--------|------------|-----------------|
{{#each blocked}}
| {{number}} | {{task}} | {{blocker}} | {{required_action}} |
{{/each}}

---

## Executed Validations

| Validation | Result | Attempt | Notes |
|-----------|-----------|-----------|-------------|
| Build | {{build_result}} | {{build_attempt}} | {{build_notes}} |
| Lint | {{lint_result}} | {{lint_attempt}} | {{lint_notes}} |
| Typecheck | {{typecheck_result}} | {{typecheck_attempt}} | {{typecheck_notes}} |
| Unit Tests | {{unit_test_result}} | {{unit_test_attempt}} | {{unit_test_notes}} |
| Integration Tests | {{integration_test_result}} | {{integration_test_attempt}} | {{integration_test_notes}} |

---

## Implemented Changes

| File | Type | Task | Added Lines | Removed Lines |
|---------|------|--------|--------------------|--------------------|
{{#each changes}}
| {{file}} | {{type}} | {{task}} | {{added}} | {{removed}} |
{{/each}}

---

## Updated Documentation

| Document | Type of Update | Status |
|-----------|---------------------|--------|
{{#each docs_updated}}
| {{document}} | {{update_type}} | {{status}} |
{{/each}}

---

## Remaining Risks

| # | Risk | Impact | Probability | Recommended Mitigation |
|---|-------|---------|---------------|----------------------|
{{#each remaining_risks}}
| {{number}} | {{risk}} | {{impact}} | {{probability}} | {{mitigation}} |
{{/each}}

---

## Technical Debt Created

| # | Debt | Criticality | Justification |
|---|--------|-------------|---------------|
{{#each tech_debt}}
| {{number}} | {{debt}} | {{criticality}} | {{justification}} |
{{/each}}

---

## Future Recommendations

| # | Recommendation | Priority | Context |
|---|-------------|------------|----------|
{{#each recommendations}}
| {{number}} | {{recommendation}} | {{priority}} | {{context}} |
{{/each}}

---

## Implementation Metrics

| Metric | Value |
|---------|-------|
| Average Time per Task | {{avg_time_per_task}} |
| Number of Rollbacks | {{rollback_count}} |
| Number of Fixes During Execution | {{fix_count}} |
| Final Test Coverage | {{final_coverage}} |

---

## Conclusion

{{conclusion}}

---

## Signature

| Field | Value |
|-------|-------|
| Report Generated on | {{report_date}} |
| Implementation Considered | {{implementation_status}} |
| Next Steps | {{next_steps}} |