# Rollback Report

> Report generated when an implementation requires partial or total reversal.

---

## Identification

| Field | Value |
|-------|-------|
| ADR reference | {{adr_path}} |
| Rollback date | {{rollback_date}} |
| Reason | {{reason}} |
| Scope | {{scope}} (partial/total) |

---

## Reason for Rollback

### Description

{{reason_description}}

### Classification

| Criterion | Value |
|----------|-------|
| Type | {{type}} (implementation error / incompatibility / changed requirement) |
| Severity | {{severity}} (critical / high / medium / low) |
| Impact | {{impact}} (blocks production / degrades functionality / cosmetic) |

---

## Tasks Reverted

| # | Task | Reverted Commits | Affected Files |
|---|--------|-------------------|-------------------|
{{#each reverted_tasks}}
| {{number}} | {{task}} | {{commits}} | {{files}} |
{{/each}}

---

## Reverted Commits

| Hash | Message | Original Date | Author |
|------|----------|---------------|-------|
{{#each reverted_commits}}
| {{hash}} | {{message}} | {{date}} | {{author}} |
{{/each}}

---

## Final State

| Field | Value |
|-------|-------|
| Branch | {{branch}} |
| Final commit | {{final_commit}} |
| Build | {{build_status}} |
| Lint | {{lint_status}} |
| Tests | {{test_status}} |
| Clean workspace | {{workspace_clean}} |

---

## Impact on Progress

| Task | Previous State | Current State |
|--------|-------------|---------------|
{{#each task_impact}}
| {{task}} | {{before}} | {{after}} |
{{/each}}

---

## Corrective Actions

| # | Action | Responsible | Deadline | Status |
|---|------|-------------|-------|--------|
{{#each corrective_actions}}
| {{number}} | {{action}} | {{owner}} | {{deadline}} | {{status}} |
{{/each}}

---

## Lessons Learned

| # | Lesson | Applicable to |
|---|-------|-------------|
{{#each lessons}}
| {{number}} | {{lesson}} | {{applicable_to}} |
{{/each}}

---

## Next Steps

1. {{next_step_1}}
2. {{next_step_2}}
3. {{next_step_3}}

---

## Rollback Validation

- [ ] All reverted commits confirmed
- [ ] Build passes after rollback
- [ ] Tests pass after rollback
- [ ] Workspace is clean
- [ ] Corrective actions documented
- [ ] Lessons learned recorded

---

## Signature

| Field | Value |
|-------|-------|
| Rollback executed on | {{execution_date}} |
| Rollback status | {{rollback_status}} |
| Implementation can proceed | {{can_proceed}} |