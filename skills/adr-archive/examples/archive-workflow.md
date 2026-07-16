# Example: ADR Archive Workflow

> Exemplo completo de uso da skill `adr-archive` para arquivar ADR-007

---

## Cenário

ADR-007 (AGENTS.md Generator) foi implementada com:
- `docs/adr/ADR-007.md` — ADR principal
- `docs/adr/ADR-007-BP.md` — Blueprint
- `docs/adr/ADR-007-TODO.md` — TODO 100% completo
- `docs/adr/ADR-007-PI.md` — Implementation Plan (Tier 2)
- `docs/adr/ADR-007-ER.md` — Execution Report na raiz

---

## Passo 1: Auditoria (Zero Tokens)

```bash
cd /home/loupan/projetosVS/ignite-agents-skills
python3 skills/adr-archive/scripts/audit.py .
```

**Output esperado:**
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

## Passo 2: Ler Relatório

```bash
cat docs/reports/adr-archive-report-20260715.md
```

**Trecho do relatório:**
```markdown
## Flags de Ação
| Flag | ADR | Descrição | Ação Requerida |
|------|-----|-----------|----------------|
| READY_TO_ARCHIVE | ADR-007 | ADR-007-ER.md exists, TODO complete | python3 audit.py . --archive ADR-007 |
| READY_TO_ARCHIVE | ADR-008 | ADR-008-ER.md exists, TODO complete | python3 audit.py . --archive ADR-008 |
```

---

## Passo 3: Arquivar

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

## Passo 4: Verificar

```bash
ls -la docs/adr/
# Deve mostrar apenas ERs + ADRs ativas (se houver)

ls -la docs/adr/archive/
# Deve mostrar ADR-007*, ADR-008*

cat docs/adr/INDEX.md
# Seção "Archived ADRs" deve incluir ADR-007 e ADR-008
```

---

## Passo 5: Deploy gh-pages (Governança)

```bash
git checkout gh-pages
git merge master
git push origin gh-pages
git checkout master
```

---

*Exemplo: `skills/adr-archive/examples/archive-workflow.md`*