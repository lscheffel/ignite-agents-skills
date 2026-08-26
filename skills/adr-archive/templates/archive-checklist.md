# ADR Archive Checklist Template

> Checklist for validation before archiving ADR

---

## Prerequisites for Archiving

### Primary ADR
- [ ] Status is "Implemented" or "Accepted"
- [ ] ADR has an archiving date
- [ ] References to BP, TODO, PI (if applicable) are up-to-date

### Blueprint (BP)
- [ ] BP exists: `ADR-XXX-BP.md`
- [ ] All phases are marked as completed
- [ ] Acceptance criteria are met

### TODO
- [ ] TODO exists: `ADR-XXX-TODO.md`
- [ ] **Zero pending tasks** (`[ ]` → all `[x]`)
- [ ] All validation commands pass

### Implementation Plan (PI) — if Tier 2/3
- [ ] PI exists: `ADR-XXX-PI.md`
- [ ] Microscopic tasks are all completed
- [ ] TDD tests are passing

### Execution Report (ER)
- [ ] ER exists in the root: `docs/adr/ADR-XXX-ER.md`
- [ ] ER documents: what was done, tests, metrics, lessons
- [ ] ER is linked in the primary ADR

---

## Execution Validation

- [ ] `./scripts/archive-adrs.sh --dry-run` shows ADR as "Ready to Archive"
- [ ] No `ARCHIVED_MISTAKE_RETURN` flag for this ADR
- [ ] Work branch merged into master
- [ ] SemVer tag created (if feature is complete)

---

## Archiving Command

```bash
python3 audit.py . --archive ADR-XXX
# OR
./scripts/archive-adrs.sh
```

---

## Post-Archiving

- [ ] `docs/adr/INDEX.md` updated (moved to "Archived ADRs")
- [ ] ADR + BP + TODO + PI moved to `docs/adr/archive/`
- [ ] ER remains in `docs/adr/` (root)
- [ ] gh-pages deploy synchronized

---

## Exceptions (Do Not Archive)

- [ ] ADR with status "Proposed" or "In Progress"
- [ ] ADR with TODO containing `[ ]` (pending tasks)
- [ ] ADR without ER in the root (create ER first)
- [ ] ADR marking active technical debt (keep visible)

---

*Template: `skills/adr-archive/templates/archive-checklist.md`*