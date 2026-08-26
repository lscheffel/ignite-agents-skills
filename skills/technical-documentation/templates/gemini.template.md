# Gemini CLI & Antigravity Rules (GEMINI.md)

> Contextual Directives, Preferences, and Universal Rules for Executions in the Gemini CLI and Google Antigravity Ecosystem.

---

## 1. Primary Operational Rules

- **Agent Behavior:** Deep reasoning, methodical execution, and continuous verification before concluding any task.
- **Response Format:** Concise, direct, with clickable links in markdown format (`[file.ext](file:///absolute/path)`).
- **No Placeholders:** All code, documentation, and scripts must be provided in their entirety, without cuts.

---

## 2. Governance Patterns and Skills

- **Creating ADRs:** Use the `adr-generator` skill.
- **Incremental Implementation:** Use the `implementation` skill.
- **Governance Janitor:** Use the `adr-archive` and `audit.py` skills.
- **Document Reconciliation:** Use the `technical-documentation` skill to audit and synchronize `README.md`, `CHANGELOG.md`, `USAGE.md`, `RELEASE-NOTES.md`, `STATE.md`, and `AGENTS.md`/`GEMINI.md`.

---

## 3. Token Economy Guidelines

- Do not read consolidated files (`CONSOLIDADA` or `docs/adr/archive/`) unless explicitly requested.
- Prioritize querying structured indices (`ADR-INDEX.md`, `tech-debt-registry.json`).