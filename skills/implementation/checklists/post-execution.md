# Post-Implementation Checklist

> Execute this checklist after completing the entire governed implementation.

---

## 1. Task Validation

- [ ] All TODO tasks are marked as "Completed"
- [ ] No task is marked as "Blocked"
- [ ] No task is marked as "In Progress"
- [ ] "Deferred" tasks have documented justification

---

## 2. Build Validation

- [ ] Main build passes without errors
- [ ] Typecheck build passes without errors
- [ ] No new, unjustified warnings

---

## 3. Quality Validation

- [ ] Lint passes without errors
- [ ] Formatting is consistent
- [ ] No code smells were introduced
- [ ] **Isolated Scope:** No files or refactorings outside the contract were included

---

## 4. Test Validation

- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)
- [ ] Test coverage did not decrease
- [ ] New tests were added for new features

---

## 5. Documentation Validation

- [ ] ADR is updated with implementation status
- [ ] Blueprint is synchronized with implemented code
- [ ] TODO reflects real state (all tasks completed)
- [ ] README was updated (if applicable)
- [ ] CHANGELOG was updated (if applicable)
- [ ] `related_skills` were updated (if applicable)

---

## 6. Registry & Technical Debt Validation

- [ ] Incident technical debt discovered was registered in `docs/governance/tech-debt-registry.json`
- [ ] `skills/index.json` was updated (if new skill)
- [ ] `validate-index.sh` passes
- [ ] `validate-skill.sh` passes for new skill
- [ ] All paths in `index.json` are valid

---

## 7. Git Validation

- [ ] All commits follow Conventional Commits
- [ ] No secrets or credentials were committed
- [ ] Branch is clean and ready for PR
- [ ] Commit messages are descriptive

---

## 8. Risk Validation

- [ ] Remaining risks were documented
- [ ] Created/Discovered technical debt was registered in `tech-debt-registry.json`
- [ ] Future recommendations were registered

---

## 9. Execution Report

- [ ] Execution Report was generated from the template (or via gatekeeper algorithmic `audit.py`)
- [ ] All mandatory fields were filled
- [ ] Report includes lessons learned
- [ ] Report includes implementation metrics

---

## 10. Final Validation

- [ ] `validate-index.sh` passes for all skills
- [ ] `validate-skill.sh` passes for all skills
- [ ] No `related_skills` point to non-existent skill
- [ ] Workspace is clean

---

## Final Approval

| Field | Value |
|-------|-------|
| Checklist complete | ✅/❌ |
| Validations passed | ✅/❌ |
| Documentation synchronized | ✅/❌ |
| Technical debts registered | ✅/❌ |
| Implementation Report generated | ✅/❌ |
| Implementation considered complete | ✅/❌ |