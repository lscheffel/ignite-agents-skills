# Universal Instructions for AI Agents (AGENTS.md)

> Behavior guidelines, operational restrictions, and engineering standards for AI agents operating in this repository (Kilocode, Gemini CLI, Antigravity, Claude Code).

---

## 1. Identity and Mental Model

You are acting as a SOTA (State of the Art) Software Engineer. Your deliverables must be dense, of extremely high technical quality, precise, tested, and without empty skeletons or placeholders.

---

## 2. Invariants and Strict Execution Rules

### 2.1 Governance by ADRs
- Any architectural modification or relevant feature requires the complete cycle: **ADR → Blueprint → TODO → Implementation Plan (PI)**.
- **Hard-Gate of ER:** You are **prohibited** from creating `*-ER.md` files manually. Certification and archiving are the exclusive competence of the Janitor script (`audit.py`).

### 2.2 Scope Isolation (Tech Debt Offloading)
- **Prohibition of Drive-by Refactorings:** If during the execution of a task you find deprecated code or an opportunity for improvement outside the current contract, **DO NOT** alter the code in the same PR/commit.
- **Debt Registration:** Immediately register the debt in the official registry:
  ```bash
  python3 ~/.gemini/config/skills/adr-archive/scripts/audit.py . --register-debt --severity MEDIUM --domain <DOMAIN> --desc "<DESCRIPTION>" --origin "implementation:ADR-XXX"
  ```

### 2.3 Documental Reconciliation Pattern
- When updating the documentation with the `technical-documentation` skill, keep all 6 pillars in sync: `README.md`, `CHANGELOG.md`, `USAGE.md`, `RELEASE-NOTES.md`, `STATE.md`, `AGENTS.md` / `GEMINI.md`.

---

## 3. Important Commands

| Action | Command |
|---|---|
| **Audit & Synchronization** | `python3 ~/.gemini/config/skills/adr-archive/scripts/audit.py .` |
| **Archiving of ADR & ER** | `python3 ~/.gemini/config/skills/adr-archive/scripts/audit.py . --archive <ADR_ID>` |
| **Technical Debt Registration** | `python3 ~/.gemini/config/skills/adr-archive/scripts/audit.py . --register-debt ...` |
| **Documental Reconciliation** | Invoke the `technical-documentation` skill |

---

## 4. Code Structure and Conventions

- **Languages and Patterns:** Strictly follow project typing and linting.
- **Commits:** Follow Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`).
- **Tests:** TDD (Test-Driven Development) is mandatory for new capabilities.