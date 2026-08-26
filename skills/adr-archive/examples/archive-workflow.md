# Example: ADR Archive Workflow

> Complete usage example of the `adr-archive` skill for archiving ADR-007

---

## Scenario

ADR-007 (AGENTS.md Generator) was implemented with:
- `docs/adr/ADR-007.md` — Main ADR
- `docs/adr/ADR-007-BP.md` — Blueprint
- `docs/adr/ADR-007-TODO.md` — 100% complete TODO
- `docs/adr/ADR-007-PI.md` — Implementation Plan (Tier 2)
- `docs/adr/ADR-007-ER.md` — Execution Report in the root

---

## Step 1: Audit (Zero Tokens)

```bash
cd /home/loupan/projetosVS/ignite-agents-skills
python3 skills/adr-archive/scripts/audit.py .
```

**Expected Output:**
```
🔍 ADR Archive Audit — 2026-07-15
=====================================

📊 Stats:
  Total ADRs: 15
  Active (root): 0
  Archived: 15

🚩 Flags Found:
  [READY_TO_ARCHIVE] ADR-007 — ADR-007-ER.md exists, TODO complete
  [READY_TO_ARCHIVE] ADR-008 — ADR-008-ER.md exists, TODO complete

📝 Report: docs/reports/adr-archive-report-20260715.md
```

---

## Step 2: Read Report

```bash
cat docs/reports/adr-archive-report-20260715.md
```

**Report Excerpt:**
```markdown
## Action Flags
| Flag | ADR | Description | Required Action |
|------|-----|-------------|-----------------|
| READY_TO_ARCHIVE | ADR-007 | ADR-007-ER.md exists, TODO complete | python3 audit.py . --archive ADR-007 |
| READY_TO_ARCHIVE | ADR-008 | ADR-008-ER.md exists, TODO complete | python3 audit.py . --archive ADR-008 |
```

---

## Step 3: Archive

```bash
python3 skills/adr-archive/scripts/audit.py . --archive ADR-007
python3 skills/adr-archive/scripts/audit.py . --archive ADR-008
```

**Output:**
```
✅ ADR-007 archived successfully
   Moved: ADR-007.md, ADR-007-BP.md, ADR-007-TODO.md, ADR-007-PI.md → archive/
   Kept: ADR-007-ER.md in root
   Updated: docs/adr/INDEX.md

✅ ADR-008 archived successfully
   Moved: ADR-008.md, ADR-008-BP.md, ADR-008-TODO.md, ADR-008-PI.md → archive/
   Kept: ADR-008-ER.md in root
   Updated: docs/adr/INDEX.md
```

---

## Step 4: Verify

```bash
ls -la docs/adr/
# Should show only ERs + active ADRs (if any)

ls -la docs/adr/archive/
# Should show ADR-007*, ADR-008*

cat docs/adr/INDEX.md
# "Archived ADRs" section should include ADR-007 and ADR-008
```

---

## Step 5: Deploy gh-pages (Governance)

```bash
git checkout gh-pages
git merge master
git push origin gh-pages
git checkout master
```

---

*Example: `skills/adr-archive/examples/archive-workflow.md`*