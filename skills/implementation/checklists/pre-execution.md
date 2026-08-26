# Pre-Execution Checklist

> Execute this checklist before initiating any governed implementation.

---

## 1. Artifact Validation

- [ ] ADR exists and is in `docs/adr/ADR-XXX.md`
- [ ] ADR contains a filled "Decision" section
- [ ] ADR contains a filled "Context" section
- [ ] ADR contains a filled "Consequences" section
- [ ] Blueprint exists in `docs/adr/ADR-XXX-BP.md`
- [ ] Blueprint contains documented tasks with dependencies
- [ ] Blueprint contains time estimates
- [ ] TODO exists in `docs/adr/ADR-XXX-TODO.md`
- [ ] TODO contains tasks with states (pending/in progress/completed)
- [ ] TODO contains dependencies between tasks
- [ ] TODO contains defined priorities

---

## 2. Coherence Validation

- [ ] Tasks from the Blueprint exist in the TODO
- [ ] Dependencies in the TODO are consistent with the Blueprint
- [ ] Estimates in the TODO are consistent with the Blueprint
- [ ] No task is duplicated between the Blueprint and TODO
- [ ] ADR is aligned with the scope of the Blueprint

---

## 3. Environment Validation

- [ ] Current branch is not main/master (or a PR is open)
- [ ] Workspace is clean (no uncommitted changes)
- [ ] Branch is up-to-date with remote
- [ ] No pending merge conflicts
- [ ] Working directory is correct

---

## 4. Affected File Validation

- [ ] All files listed in the Blueprint exist
- [ ] Files are accessible (correct permissions)
- [ ] No files are locked by another process
- [ ] Backup was considered (if applicable)

---

## 5. Criteria Validation

- [ ] Acceptance criteria are defined in the TODO
- [ ] Rollback criteria are defined in the Blueprint
- [ ] Relevant tests were identified
- [ ] Validation commands were documented

---

## 6. External Dependency Validation

- [ ] Related skills are available in the registry
- [ ] Build dependencies are installed
- [ ] Lint/test tools are configured
- [ ] CI/CD is functional (if applicable)

---

## 7. Execution Contract Generation

- [ ] Execution Contract was generated from the template
- [ ] All mandatory fields were filled
- [ ] Contract was validated by the agent
- [ ] Next step was defined

---

## 8. Change Plan Construction

- [ ] DAG was constructed from the TODO
- [ ] DAG is free of cycles
- [ ] Execution order was defined (topological sort)
- [ ] Parallelizable tasks were identified
- [ ] Total estimate was calculated

---

## Approval

| Field | Value |
|-------|-------|
| Checklist complete | ✅/❌ |
| Contract approved | ✅/❌ |
| Plan approved | ✅/❌ |
| Implementation authorized | ✅/❌ |