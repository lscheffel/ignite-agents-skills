# ADR-033 TODO: Operational Task Checklist

> **Companion Artifact to:** [ADR-033.md](./ADR-033.md) & [ADR-033-PI.md](./ADR-033-PI.md)  
> **Status:** ACTIVE  

---

## Task Backlog

- [x] `TASK-033-01`: Refactor `skills/database-architecture/SKILL.md` with B-Tree Index Selectivity math ($S_{\text{idx}} = D/N$), Relational Normalization (3NF/BCNF), and Expand-Contract migrations.
- [x] `TASK-033-02`: Refactor `skills/ddd/SKILL.md` with Aggregate Root transactional invariants (1 transaction per aggregate) and Domain Event envelopes.
- [x] `TASK-033-03`: Refactor `skills/api-design/SKILL.md` with RFC 7807 Problem Details and RFC 7231 Idempotency Key protocols.
- [x] `TASK-033-04`: Refactor `skills/deployment/SKILL.md` with Canary deployment routing algebra and zero-downtime database migration gates.
- [x] `TASK-033-05`: Refactor `skills/observability/SKILL.md` with OpenTelemetry GenAI span conventions, Google SRE Golden Signals, and RED/USE metrics.
- [x] `TASK-033-06`: Refactor `skills/performance-optimization/SKILL.md` with Little's Law ($L = \lambda W$) and Amdahl's Law speedup calculations.
- [x] `TASK-033-07`: Refactor `skills/security-review/SKILL.md` with STRIDE threat modeling algebra, OWASP Top 10 (2021) / API Top 10 (2023), and CVSS v3.1 rubrics.
- [x] `TASK-033-08`: Refactor `skills/php-laravel-ecosystem/SKILL.md` with modern Laravel 11/12 SOTA architecture (Pest v3, Pint, Octane concurrency safety).
- [x] `TASK-033-09`: Polish structural headings (`When to Use`, `Completion Gate`) across Batch 4 skills.
- [x] `TASK-033-10`: Re-audit Batch 4 skills and update `SKILL_AUDIT_LEDGER.md`.
- [x] `TASK-033-11`: Run full test suite (`python3 -m unittest discover -s scripts/tests`) and `pages/build.py`.
