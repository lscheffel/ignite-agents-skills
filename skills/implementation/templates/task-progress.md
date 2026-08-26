# Task Progress

> Individual task progress during governed execution.

---

## Identification

| Field | Value |
|-------|-------|
| Task | {{task_name}} |
| Number | {{task_number}} |
| TODO | {{todo_path}} |
| Start Date | {{start_date}} |

---

## State

| Field | Value |
|-------|-------|
| Current State | {{current_state}} |
| Start Date | {{start_date}} |
| End Date | {{end_date}} |
| Duration | {{duration}} |
| Attempts | {{attempts}} |

### State Transitions

| Date | From | To | Reason |
|------|------|----|--------|
{{#each transitions}}
| {{date}} | {{from}} | {{to}} | {{reason}} |
{{/each}}

---

## Task Description

{{task_description}}

---

## Dependencies

| # | Dependency | State | Can Start? |
|---|-------------|--------|---------------|
{{#each dependencies}}
| {{number}} | {{dependency}} | {{status}} | {{can_start}} |
{{/each}}

---

## Changes Made

| # | File | Type | Description | Lines |
|---|---------|------|-----------|--------|
{{#each changes}}
| {{number}} | {{file}} | {{type}} | {{description}} | {{lines}} |
{{/each}}

---

## Validations

| # | Validation | Result | Attempt | Timestamp | Notes |
|---|-----------|-----------|-----------|-----------|-------------|
{{#each validations}}
| {{number}} | {{validation}} | {{result}} | {{attempt}} | {{timestamp}} | {{notes}} |
{{/each}}

---

## Blockers

| # | Blocker | Identification Date | Resolution Date | Action |
|---|------------|-------------------|----------------|------|
{{#each blockers}}
| {{number}} | {{blocker}} | {{identified}} | {{resolved}} | {{action}} |
{{/each}}

---

## Acceptance Criteria

| # | Criterion | Met | Evidence |
|---|----------|----------|-----------|
{{#each acceptance_criteria}}
| {{number}} | {{criterion}} | {{met}} | {{evidence}} |
{{/each}}

---

## Notes

{{#each notes}}
- {{note}}
{{/each}}

---

## Summary

| Field | Value |
|-------|-------|
| Task Completed | {{completed}} |
| Validations Passed | {{validations_passed}} |
| Documentation Updated | {{docs_updated}} |
| Next Task | {{next_task}} |