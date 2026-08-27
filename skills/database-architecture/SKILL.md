---
name: database-architecture
version: 2.0.0
description: Unified database modeling, schema design, migrations, and performance optimization.
related_skills:
  - cap
  - implementation
  - technical-documentation
domain: architecture-systems
triggers:
  - database-architecture
  - database-design
  - sql-modeling
  - schema-migrations
  - arquitetura-de-banco
  - modelagem-de-dados
  - migracao-de-schema
  - performance-db
tags:
- database-architecture
- schema-design
- sql
- migrations
- performance
- data-modeling
metadata:
  author: Antigravity Refactored Architecture
  provenance: internal
  last_audited: '2026-08-24'
---

# Database Architecture & Schema Design (v2.0.0)

## When to Use

### Use when:
- Designing relational or NoSQL database schemas, entities, and relationships
- Optimizing indexing strategies ($S_{\text{idx}} \ge 0.15$), query performance, and connection pools
- Planning zero-downtime database migrations via the Expand-Contract pattern

### Do not use when:
- In-memory data structures or simple JSON file storage without database engine

> 💡 **Lazy Loading of References:** This document contains contracts, decision-making heuristics, and central modeling rules. To consult complete DDL templates, partitioning scripts, and an exhaustive catalog of anti-patterns, execute `view_file` on [`references/patterns-and-migrations.md`](./references/patterns-and-migrations.md).

---

## 1. Decision Tree for Modeling & Storage



```mermaid
graph TD
    A[Data Modeling] -->|Relational?| B{Access Type}
    A -->|Non-Relational| N[Document / Key-Value / Graph]
    B -->|Structured & Transactional| C[Normalized SQL Schema 3NF]
    B -->|High Read Frequency| D[Strategic Denormalization / Views]
    C --> E{Indexing Strategy}
    D --> E
    E --> F[Predicate Analysis for WHERE & JOINs]
    F --> G[Composite / Partial Indexes]
    G --> H[Migrated Versions UP/DOWN]
    H --> I[CI/CD Validation & Rollback]
```



---

## 2. Modeling Invariants & Normalization

1. **Required Primary Keys:** Every table MUST contain an immutable primary key (`UUID` or `BIGINT IDENTITY`).
2. **Referential Integrity:** Foreign keys MUST explicitly define `ON DELETE RESTRICT` or `ON DELETE CASCADE`.
3. **Strict Typing & Constraints:**
   - Currency / Monetary Values: `BIGINT` (cents) or `NUMERIC(15,2)`. Never `FLOAT`.
   - Dates: `TIMESTAMPTZ` (always with UTC time zone).
   - Validations: `CHECK constraints` for enums and finite domains.
4. **Normalization vs Denormalization:**
   - Write Path (Transactional): Normalize to 3NF/BCNF to eliminate write anomalies.
   - Read Path (Analytics/Dashboards): Strategically denormalize with Materialized Views or Redis cache.

---

## 3. Indexing Strategy & Query Optimization

| Query Type | Indexing Strategy | Example SQL |
|---|---|---|
| Filter with high selectivity | Simple B-Tree Index | `CREATE INDEX idx_users_email ON users(email);` |
| Filter with multiple columns | Composite Index (Order: equality $\rightarrow$ range) | `CREATE INDEX idx_orders_user_date ON orders(user_id, created_at);` |
| Specific status / Boolean | Partial Index | `CREATE INDEX idx_orders_pending ON orders(user_id) WHERE status = 'pending';` |
| Read without accessing heap | Covering Index (`INCLUDE`) | `CREATE INDEX idx_users_lookup ON users(email) INCLUDE (name, is_active);` |

---

## 4. Migration Governance (Zero Downtime)

1. **Atomicity & Reversibility:** Every migration MUST be strictly reversible with `UP` and `DOWN` scripts.
2. **Expand / Contract Pattern:** Never remove or rename columns in production in a single deploy; use 3-step migration (Add $\rightarrow$ Backfill $\rightarrow$ Deprecate).
3. **Automated Validation:** Execute dry-run and migration tests in CI/CD before deployment.

---

## 5. Extended References

To consult detailed DDL scripts, partitioning examples, and an exhaustive catalog of anti-patterns:
- 👉 [references/patterns-and-migrations.md](./references/patterns-and-migrations.md)
| Anti-Pattern | Severity | Negative Impact | Canonical Mitigation |
| :--- | :---: | :--- | :--- |
| **Early Execution without Context** | 🔴 Critical | Context hallucination and destructive refactoring | Enable the `cap` skill to acquire minimal evidence before editing. |
| **Omission of Validation Checklists** | 🟡 Medium | Delivery of artifacts with syntactic inconsistencies | Rigorously execute the checklist step by step before handoff. |
| **Lack of Decision Documentation** | 🟢 Low | Loss of technical traceability and architectural drift | Record relevant trade-offs via the `adr-generator` skill. |- **Restricted Environment / Read-Only:** If the filesystem or sandbox is locked against writing, report the lock with immediate evidence and generate the patch in markdown diff.- [ ] All prerequisites and target files were inspected before the modification.A task associated with the `database-architecture` skill can only be declared complete when:
1. All operational checklist checks have been met.
2. The result has been validated deterministically through execution evidence.
3. There are no outstanding structural issues, placeholders, or unresolved errors.


## Domain SOTA & Industry Engineering Standards

- **Relational Normalization:** Edgar F. Codd's Normal Forms (1NF, 2NF, 3NF, Boyce-Codd BCNF) and pragmatic de-normalization.
- **ACID Transaction Isolation Levels:** ANSI/ISO SQL-92 (Read Uncommitted, Read Committed, Repeatable Read, Serializable) and MVCC internals.
- **Index Engineering:** B-Tree, Hash, GIN, GiST, and BRIN index mechanics with selectivity math.
- **Zero-Downtime Schema Migrations:** Expand-Contract (Parallel Run) Pattern for zero lock contention.

### B-Tree Index Selectivity Formula:

$$S_{\text{idx}} = \frac{D_{\text{distinct}}}{N_{\text{total}}} \in (0, 1]$$

| Metric / Threshold | Recommendation |
|:---|:---|
| **$S_{\text{idx}} \ge 0.15$ ($15\%+$ distinct)** | Create standard B-Tree index. |
| **$0.01 \le S_{\text{idx}} < 0.15$** | Evaluate Composite or Partial / Filtered Index (`WHERE active = true`). |
| **$S_{\text{idx}} < 0.01$ ($<1\%$ distinct / Boolean)** | Do NOT index with B-Tree; use Bitmap or evaluate table scan efficiency. |

### Expand-Contract Migration Lifecycle:
1. **Phase 1 (Expand):** Add new column/table as nullable. Deploy code writing to BOTH old and new locations.
2. **Phase 2 (Backfill):** Run asynchronous batch backfill script in small chunks ($N_{\text{chunk}} = 1000$).
3. **Phase 3 (Switch):** Deploy code reading exclusively from new location.
4. **Phase 4 (Contract):** Remove old column/table safely after 30-day soak period.

### Exhaustive Heuristic Decision Rules:
- **Rule of Thumb 1 (Zero-Trust Architectural Boundaries):** Treat all external inputs, third-party payloads, and cross-module boundaries with strict zero-trust schema validation.
- **Rule of Thumb 2 (Fail-Fast & Deterministic Errors):** Reject invalid states immediately with typed, actionable error contracts rather than cascading silent failures.
- **Rule of Thumb 3 (Idempotency & AST Preservation):** State mutations and code transformations must maintain semantic idempotency across repeated executions.
- **Rule of Thumb 4 (Benchmark & Telemetry Alignment):** Measure critical execution latency ($P_{95}$) and memory overhead with structured telemetry and baseline benchmarks.
- **Rule of Thumb 5 (Event-Driven & Circuit Breaker Decoupling):** Isolate asynchronous operations behind circuit breakers and resilient retry mechanisms to prevent cascading failure.
- **Rule of Thumb 6 (Contract-First DDD Modeling):** Define clear domain aggregates, value objects, and typed interface contracts before implementing concrete logic.
- **Rule of Thumb 7 (RAG & Semantic Retrieval Precision):** Optimize context retrieval with hybrid lexical-vector search and reciprocal rank fusion to eliminate hallucinated routing.
- **Rule of Thumb 8 (OWASP & Supply Chain Verification):** Verify dependencies and data flows against OWASP Top 10 and SLSA Level 3 supply chain security standards.
- **Rule of Thumb 9 (Verification Gate Invariant):** Never declare completion without automated test execution evidence and zero compiler/linter warnings.
## Edge Cases & Failure Modes

- **Edge Case 1 (Table-Locking DDL Migrations):** Mandate `ADD COLUMN ... NULL` without table locks on production tables exceeding 1M rows.
- **Edge Case 2 (N+1 Query Explosion):** Detect un-eager-loaded relationships in ORM access paths using telemetry profilers.
- **Edge Case 3 (Missing Composite Index Ordering):** Order multi-column composite index keys by highest cardinality first (`(tenant_id, status, created_at)`).

## Completion Gate & Verification
Before declaring database architecture change complete:
- [ ] Schema normalized to 3NF/BCNF (or documented de-normalization rationale)
- [ ] Index selectivity calculated and verified with `EXPLAIN ANALYZE`
- [ ] Idempotent migration with reversible rollback vector verified