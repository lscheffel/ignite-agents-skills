#!/usr/bin/env python3
"""
scripts/remediate_batch4_sota.py — Comprehensive Batch 4 Domain SOTA Elevation (ADR-033)
Injects B-Tree Index Math, RFC 7807 API contracts, STRIDE Threat Modeling, Little's Law,
and Laravel 11/12 architectures into the 8 Backend, Cloud & Security skills.
"""

from pathlib import Path

BATCH_4_DATA = {
    "database-architecture": """
## Domain SOTA & Industry Engineering Standards

- **Relational Normalization:** Edgar F. Codd's Normal Forms (1NF, 2NF, 3NF, Boyce-Codd BCNF) and pragmatic de-normalization.
- **ACID Transaction Isolation Levels:** ANSI/ISO SQL-92 (Read Uncommitted, Read Committed, Repeatable Read, Serializable) and MVCC internals.
- **Index Engineering:** B-Tree, Hash, GIN, GiST, and BRIN index mechanics with selectivity math.
- **Zero-Downtime Schema Migrations:** Expand-Contract (Parallel Run) Pattern for zero lock contention.

### B-Tree Index Selectivity Formula:

$$S_{\\text{idx}} = \\frac{D_{\\text{distinct}}}{N_{\\text{total}}} \\in (0, 1]$$

| Metric / Threshold | Recommendation |
|:---|:---|
| **$S_{\\text{idx}} \\ge 0.15$ ($15\\%+$ distinct)** | Create standard B-Tree index. |
| **$0.01 \\le S_{\\text{idx}} < 0.15$** | Evaluate Composite or Partial / Filtered Index (`WHERE active = true`). |
| **$S_{\\text{idx}} < 0.01$ ($<1\\%$ distinct / Boolean)** | Do NOT index with B-Tree; use Bitmap or evaluate table scan efficiency. |

### Expand-Contract Migration Lifecycle:
1. **Phase 1 (Expand):** Add new column/table as nullable. Deploy code writing to BOTH old and new locations.
2. **Phase 2 (Backfill):** Run asynchronous batch backfill script in small chunks ($N_{\\text{chunk}} = 1000$).
3. **Phase 3 (Switch):** Deploy code reading exclusively from new location.
4. **Phase 4 (Contract):** Remove old column/table safely after 30-day soak period.

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Zero Table Locks in Production):** Never execute blocking `ALTER TABLE ADD COLUMN NOT NULL DEFAULT ...` without PostgreSQL 11+ metadata-only optimizations or Expand-Contract pattern.
2. **Rule of Thumb 2 (Foreign Key Indexing):** Every foreign key column MUST be indexed to prevent full table scans during parent cascade deletes.
3. **Rule of Thumb 3 (Query Optimization SLA):** Any OLTP query taking $>50\\text{ms}$ must be analyzed with `EXPLAIN (ANALYZE, BUFFERS)` to eliminate Seq Scans on large tables.
4. **Rule of Thumb 4 (Idempotent Migrations):** Migration scripts must be deterministic and provide verifiable down/rollback vectors.
""",

    "api-design": """
## Domain SOTA & Industry Engineering Standards

- **RESTful API Architecture:** Richardson Maturity Model (Level 0 to Level 3 HATEOAS) and Fielding REST constraints.
- **Standardized Error Contracts:** RFC 7807 (Problem Details for HTTP APIs - `application/problem+json`).
- **Idempotency & Safety:** RFC 7231 / RFC 9110 HTTP semantics and IETF Idempotency-Key Header specification.
- **Pagination Standards:** Keyset / Cursor-Based Pagination vs Offset-Based ($O(1)$ vs $O(N)$ database scan).

### RFC 7807 Problem Details Error Schema:

```json
{
  "type": "https://api.example.com/errors/invalid-parameters",
  "title": "Invalid Request Parameters",
  "status": 422,
  "detail": "The 'query' field cannot be empty.",
  "instance": "/v1/search",
  "invalid_params": [
    {
      "name": "query",
      "reason": "Must be at least 3 characters long"
    }
  ]
}
```

### Cursor Pagination URL Contract:
`GET /v1/skills?limit=20&starting_after=skl_984fbc12`

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (RFC 7807 Mandate):** Never return ad-hoc error formats like `{ "error": "msg" }`; always return RFC 7807 compliant payloads with HTTP status matching payload status.
2. **Rule of Thumb 2 (Idempotency Key for Mutating Calls):** All financial, payment, or state-creating `POST` endpoints must support `Idempotency-Key` headers with a 24-hour cache TTL.
3. **Rule of Thumb 3 (Cursor Over Offset for Large Datasets):** For collections with $>10,000$ rows, offset pagination (`?page=100`) is prohibited; use keyset cursor pagination.
4. **Rule of Thumb 4 (Semantic HTTP Verbs):** `GET`, `HEAD`, `OPTIONS` must remain strictly safe and idempotent; `PUT` and `DELETE` must be idempotent; `POST` and `PATCH` are non-idempotent.
""",

    "ddd": """
## Domain SOTA & Industry Engineering Standards

- **Strategic DDD:** Bounded Contexts, Context Mapping (Shared Kernel, Customer-Supplier, Anti-Corruption Layer - ACL).
- **Tactical DDD:** Entities, Value Objects, Aggregates, Domain Services, Repositories, and Domain Events.
- **Transactional Invariant:** Exactly ONE Aggregate Root modified per database transaction (Eric Evans / Vaughn Vernon).
- **Event Messaging:** Outbox Pattern for guaranteed at-least-once domain event dispatch.

### Aggregate Root Transaction Invariant:
Modifying multiple aggregates in the same database transaction is an anti-pattern. Use Eventual Consistency:

$$\\text{Aggregate } A_1 \\xrightarrow{\\text{Mutate}} \\text{Emit DomainEvent } E_1 \\xrightarrow{\\text{Outbox Async}} \\text{Handler updates Aggregate } A_2$$

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Value Object Immutability):** Value Objects must be 100% immutable; equality is defined by structural attribute comparison, not identity ID.
2. **Rule of Thumb 2 (No Anemic Domain Models):** Business logic and invariants MUST reside inside Entity/Aggregate methods, not leaked into procedural Service classes.
3. **Rule of Thumb 3 (Transactional Boundary Rule):** If two entities must be updated transactionally with immediate consistency, they belong to the SAME Aggregate.
4. **Rule of Thumb 4 (Anti-Corruption Layer):** Never allow external third-party DTOs or models to leak into domain core; translate via an explicit ACL Adapter.
""",

    "deployment": """
## Domain SOTA & Industry Engineering Standards

- **Deployment Strategies:** Blue-Green Switching, Canary Deployments, Rolling Updates, and Shadow Deployment.
- **Cloud-Native Infrastructure:** Kubernetes Declarative Manifests, GitOps (ArgoCD/Flux), and Infrastructure-as-Code (Terraform/OpenTofu).
- **Automated Rollback Vectors:** Prometheus/Datadog metric-driven rollback thresholds.
- **Zero-Downtime Migrations:** Health checks (Liveness, Readiness, Startup probes) paired with pre-stop lifecycle hooks.

### Canary Deployment Gating Formula:
Canary traffic percentage $\\alpha_{\\text{canary}}$ scales progressively while error rates remain bounded:

$$\\text{ErrorRate}_{\\text{canary}} \\le \\text{ErrorRate}_{\\text{baseline}} + \\epsilon \\quad (\\epsilon = 0.005)$$

If $\\text{ErrorRate}_{\\text{canary}} > \\text{Threshold}$, trigger automated instant rollback ($T_{\\text{rollback}} \\le 30\\text{s}$).

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Readiness Probe Mandate):** Never send production traffic to a pod/container until its Readiness Probe explicitly returns HTTP 200.
2. **Rule of Thumb 2 (Immutable Artifacts):** Build container images and binary packages ONCE; propagate the exact same immutable SHA through Staging and Production.
3. **Rule of Thumb 3 (Database First Deployment):** Run database schema expansion BEFORE deploying application code; never deploy code that depends on unapplied migrations.
4. **Rule of Thumb 4 (Fast Rollback Capability):** Every production deploy must have an automated one-click or zero-click rollback vector.
""",

    "observability": """
## Domain SOTA & Industry Engineering Standards

- **OpenTelemetry Standard:** Distributed Tracing (Spans, Trace IDs, Context Propagation) and GenAI Semantic Conventions.
- **Google SRE Golden Signals:** Latency, Traffic, Errors, and Saturation.
- **Monitoring Frameworks:** RED Method (Rate, Errors, Duration) for services and USE Method (Utilization, Saturation, Errors) for infrastructure.
- **Structured Logging:** JSON log envelopes with unified trace/span correlation IDs (`trace_id`, `span_id`).

### The 4 Golden Signals Architecture:

| Signal | Metric Formulation | Alert Threshold / SLA |
|:---|:---|:---|
| **Latency** | $P_{95}$ and $P_{99}$ response duration | $P_{99} > 500\\text{ms}$ for $>2\\text{min}$. |
| **Traffic** | Requests Per Second (RPS) $\\lambda$ | Anomaly detection ($\pm 50\\%$ vs historical baseline). |
| **Errors** | Error rate ratio: $\\frac{N_{\\text{5xx}}}{N_{\\text{total}}}$ | Error rate $> 1.0\\%$ over 5-minute window. |
| **Saturation** | CPU/Memory/Pool utilization: $\\frac{U_{\\text{used}}}{U_{\\text{total}}}$ | Utilization $> 85\\%$ sustained for $>5\\text{min}$. |

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Context Propagation Invariant):** All outbound HTTP/gRPC requests and background jobs must inject OpenTelemetry `traceparent` headers.
2. **Rule of Thumb 2 (Zero Unstructured Logs):** Plain text `console.log` or `print()` statements are forbidden in production; all logs must be structured JSON.
3. **Rule of Thumb 3 (High-Cardinality Hygiene):** Never use UUIDs, email addresses, or raw user inputs as Prometheus metric labels (avoid cardinality explosion).
4. **Rule of Thumb 4 (Actionable Alerting):** Every PagerDuty/Slack alert must include a direct link to a Runbook with diagnosis steps.
""",

    "security-review": """
## Domain SOTA & Industry Engineering Standards

- **Threat Modeling:** STRIDE Framework (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege).
- **Vulnerability Standards:** OWASP Top 10 (2021), OWASP API Security Top 10 (2023), and CWE Top 25.
- **Severity Scoring:** Common Vulnerability Scoring System (CVSS v3.1).
- **Cryptographic Standards:** NIST SP 800-57, TLS 1.3, Argon2id for password hashing, and AES-256-GCM for data at rest.

### STRIDE Assessment Rubric:
Every new service, endpoint, or architecture change must be evaluated against all 6 STRIDE dimensions.

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Parameterized Queries Mandate):** String concatenation in SQL/NoSQL queries is strictly prohibited; all queries MUST use parameterized prepared statements.
2. **Rule of Thumb 2 (Zero Hardcoded Secrets):** API keys, passwords, and tokens must never be committed to git; enforce pre-commit secret scanners (Gitleaks/TruffleHog).
3. **Rule of Thumb 3 (Defense in Depth / Least Privilege):** API tokens and service accounts must be scoped with the minimal permissions required to execute their specific task.
4. **Rule of Thumb 4 (Secure-by-Default Headers):** All web responses must include HSTS, CSP (`Content-Security-Policy`), `X-Content-Type-Options: nosniff`, and `X-Frame-Options: DENY`.
""",

    "performance-optimization": """
## Domain SOTA & Industry Engineering Standards

- **Queuing & Capacity Laws:** Little's Law ($L = \\lambda W$) and Amdahl's Law for parallel scaling.
- **Web Vitals (CWV):** Largest Contentful Paint (LCP $\\le 2.5\\text{s}$), Interaction to Next Paint (INP $\\le 200\\text{ms}$), Cumulative Layout Shift (CLS $\\le 0.1$).
- **Connection Pool Sizing:** HikariCP connection pool formula: $\\text{PoolSize} = ((\\text{Cores} \\times 2) + \\text{DiskSpindles})$.
- **Memory & Cache Hierarchy:** Multi-tier caching (L1 In-Memory LRU $\\to$ L2 Redis Cluster $\\to$ L3 Persistent DB) with Cache-Aside pattern.

### Little's Law Capacity Sizing Formula:

$$L = \\lambda \\cdot W \\implies \\text{Concurrency} = \\text{Throughput (RPS)} \\times \\text{Latency (Seconds)}$$

*Example:* At 1,000 RPS with mean latency of $200\\text{ms}$ ($0.2\\text{s}$), the server must support $L = 1000 \\times 0.2 = 200$ concurrent active threads/connections.

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Eliminate N+1 Queries):** Never execute queries inside loops; use eager loading (`with()`, `include()`, `JOIN FETCH`) or batching (`DataLoader`).
2. **Rule of Thumb 2 (Cache Stampede Prevention):** High-traffic cache keys must implement Probabilistic Early Expiration (XFetch) or Mutex locking to prevent cache dogpiling.
3. **Rule of Thumb 3 (Measure Before Optimizing):** Never optimize based on intuition; always capture CPU/memory profiler snapshots (Flamegraphs / pprof) before and after changes.
4. **Rule of Thumb 4 (Payload Compression):** Enable Brotli/Gzip compression for all text-based HTTP responses ($>1\\text{KB}$).
""",

    "php-laravel-ecosystem": """
## Domain SOTA & Industry Engineering Standards

- **Modern Architecture:** Laravel 11/12 streamlined application structure, action-oriented controllers, and form request validation.
- **High-Performance Runtimes:** Laravel Octane (Swoole / RoadRunner) with strict state persistence and memory leak prevention.
- **Testing Architecture:** Pest v3 Testing Framework with architectural testing (`arch()->expect('App\\Models')->toOnlyBeUsedIn(...)`).
- **Code Standards:** Laravel Pint (PHP-CS-Fixer preset) and PHPStan / Larastan Level 8+ static analysis.

### Laravel Octane Concurrency Safety Invariant:
Octane keeps the application in memory across requests. Superglobals and singletons must never store request-specific state:

```php
// ❌ WRONG (Memory leak / Data bleed across users):
class OrderService {
    public static array $currentUserOrders = [];
}

// ✅ CORRECT (Scoped request lifecycle):
class OrderService {
    public function __construct(private readonly OrderRepository $orders) {}
}
```

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Strict Architectural Testing with Pest):** Use Pest Architecture Testing to enforce domain layering rules in CI.
2. **Rule of Thumb 2 (Typed Properties & Enums):** All model attributes, DTOs, and method signatures must use native PHP 8.3+ types and backed Enums.
3. **Rule of Thumb 3 (Queued Jobs for Heavy I/O):** Any operation involving emails, PDF generation, webhooks, or external APIs must be dispatched to Laravel Queue with exponential backoff.
4. **Rule of Thumb 4 (Static Analysis Level 8):** Larastan static analysis must pass at Level 8 with zero baseline ignores.
"""
}

def main():
    root = Path(__file__).resolve().parent.parent
    skills_dir = root / "skills"
    
    for skill_name, sota_text in BATCH_4_DATA.items():
        skill_file = skills_dir / skill_name / "SKILL.md"
        if not skill_file.exists():
            print(f"[!] Skill file not found: {skill_file}")
            continue
            
        content = skill_file.read_text(encoding="utf-8")
        if "## Domain SOTA & Industry Engineering Standards" in content:
            print(f"[*] Already has SOTA standards: {skill_name}")
            continue
            
        if "## Operational Verification Checklist" in content:
            parts = content.split("## Operational Verification Checklist", 1)
            new_content = parts[0] + sota_text.strip() + "\n\n## Operational Verification Checklist" + parts[1]
        elif "## Completion Gate" in content:
            parts = content.split("## Completion Gate", 1)
            new_content = parts[0] + sota_text.strip() + "\n\n## Completion Gate" + parts[1]
        else:
            new_content = content + "\n\n" + sota_text.strip()
            
        skill_file.write_text(new_content, encoding="utf-8")
        print(f"[✓] Elevated Domain SOTA for: {skill_name}")

if __name__ == "__main__":
    main()
