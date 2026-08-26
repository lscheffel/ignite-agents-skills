# Execution Contract

> Mandatory contract that validates the presence of all necessary artifacts before execution.

---

## Identification

| Field | Value |
|-------|-------|
| ADR | {{adr_path}} |
| Blueprint | {{blueprint_path}} |
| TODO | {{todo_path}} |
| Generation Date | {{date}} |
| Responsible Agent | {{agent_name}} |

---

## Artifacts

| Artifact | Path | Status | Coherent |
|----------|------|--------|----------|
| ADR | {{adr_path}} | {{adr_status}} | {{adr_coherent}} |
| Blueprint | {{blueprint_path}} | {{bp_exists}} | {{bp_coherent}} |
| TODO | {{todo_path}} | {{todo_exists}} | {{todo_coherent}} |

### Coherence Validation

- [ ] ADR contains filled "Decision" section
- [ ] Blueprint contains documented tasks
- [ ] TODO contains tasks with states
- [ ] Blueprint tasks exist in TODO
- [ ] TODO dependencies are consistent with Blueprint

---

## Environment

| Field | Value |
|-------|-------|
| Current Branch | {{branch_name}} |
| Clean Workspace | {{workspace_clean}} |
| Commit HEAD | {{head_commit}} |
| Working Directory | {{working_dir}} |

### Environment Validation

- [ ] Branch is not main/master (or PR is open)
- [ ] No uncommitted changes (git status clean)
- [ ] All impacted files exist in workspace
- [ ] Branch is up-to-date with remote (no divergence)

---

## Affected Files

| File | Type of Change | Related Skill |
|---------|-----------------|-------------------|
{{#each affected_files}}
| {{path}} | {{change_type}} | {{related_skill}} |
{{/each}}

---

## Acceptance Criteria

| # | Criterion | Verifiable |
|---|----------|-------------|
{{#each acceptance_criteria}}
| {{number}} | {{criterion}} | {{verifiable}} |
{{/each}}

---

## Rollback Criteria

| # | Criterion | Trigger Criterion |
|---|----------|---------------------|
{{#each rollback_criteria}}
| {{number}} | {{criterion}} | {{trigger}} |
{{/each}}

---

## Final Validation

- [ ] All mandatory fields are filled
- [ ] All artifacts exist and are coherent
- [ ] Environment is clean and ready for execution
- [ ] Acceptance criteria are defined and verifiable
- [ ] Rollback criteria are defined
- [ ] Contract approved by executing agent

---

## Signature

| Field | Value |
|-------|-------|
| Contract validated on | {{validation_date}} |
| Status | {{contract_status}} |
| Next Step | {{next_step}} |