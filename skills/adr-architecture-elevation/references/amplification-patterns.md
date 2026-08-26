# Amplification Patterns Catalog

## Purpose

Reference catalog of common, proven amplification patterns organized by the five amplification types. Use during Phase 5 to identify applicable amplifications for the hardened decision set.

---

## 1. Completeness Amplification Patterns

### 1.1 Implicit Requirement Surfacing
**Pattern**: Requirements that stakeholders assume but never state explicitly.
**Detection**: Compare problem model (Phase 1) against decision set — gaps are implicit requirements.
**Amplification**: Add explicit requirements, acceptance criteria, and traceability.

### 1.2 Edge Case Enumeration
**Pattern**: Happy-path architecture that fails on boundaries.
**Detection**: For each input/output/state transition, ask: "What happens at min/max/null/empty/overflow?"
**Amplification**: Explicit handling for each edge case in contracts and implementation.

### 1.3 Non-Functional Requirement Completeness
**Pattern**: Missing NFRs (latency, availability, durability, consistency, auditability).
**Detection**: Check each quality attribute from ISO 25010 against architecture.
**Amplification**: Add specific, measurable NFR targets to ADR and BP.

### 1.4 Cross-Cutting Concern Coverage
**Pattern**: Logging, tracing, metrics, auth, rate limiting, idempotency scattered or missing.
**Detection**: Audit each component for standard cross-cutting concerns.
**Amplification**: Define unified cross-cutting concern implementation in BP.

### 1.5 Data Lifecycle Completeness
**Pattern**: Create/Read/Update covered; Delete/Archive/Purge/GDPR forgotten.
**Detection**: Trace every data entity through full lifecycle.
**Amplification**: Add retention, archival, deletion, and compliance procedures.

---

## 2. Robustness Amplification Patterns

### 2.1 Retry with Exponential Backoff + Jitter
**Pattern**: Transient failures cascade without proper retry strategy.
**Amplification**: Standard retry policy: `min(2^n * base + jitter, max)` with circuit breaker integration.

### 2.2 Circuit Breaker (State: Closed → Open → Half-Open)
**Pattern**: Cascading failures when downstream degrades.
**Amplification**: Per-dependency circuit breakers with configurable thresholds; emit metrics on state changes.

### 2.3 Bulkhead / Resource Isolation
**Pattern**: One misbehaving tenant/workload starves others.
**Amplification**: Thread pool / connection pool / memory isolation per tenant or critical path.

### 2.4 Idempotency Keys
**Pattern**: Retries cause duplicate side effects (payments, mutations).
**Amplification**: Require idempotency keys on all mutating operations; store key→result mapping with TTL.

### 2.5 Stampede Protection (Thundering Herd)
**Pattern**: Cache miss + high concurrency = DB overload.
**Amplification**: Single-flight / request coalescing; probabilistic early expiration; lease-based refresh.

### 2.6 Graceful Degradation Modes
**Pattern**: All-or-nothing failure.
**Amplification**: Define degraded modes per feature: read-only, stale data, reduced functionality, static fallback.

### 2.7 Data Integrity Guards
**Pattern**: Silent corruption propagates.
**Amplification**: Checksums on persisted data; schema validation on read; versioned schemas with migration.

### 2.8 Deterministic Key Generation
**Pattern**: Cache keys collide or become unpredictable.
**Amplification**: Canonical key format: `namespace:version:entity:id[:variant]` with deterministic serialization.

### 2.9 Concurrency Control
**Pattern**: Lost updates, dirty reads, write skew.
**Amplification**: Optimistic locking (version/timestamp) or pessimistic locking per access pattern; document choice.

### 2.10 Restart / Crash Recovery
**Pattern**: In-flight work lost; inconsistent state on restart.
**Amplification**: Checkpointing; write-ahead logs; transactional outbox pattern; idempotent replay.

---

## 3. Capability Amplification Patterns

### 3.1 Feature Flags / Toggle System
**Pattern**: Deploy ≠ Release; need progressive rollout.
**Amplification**: Built-in flag framework with targeting (user%, cohort, geography), kill switch, audit log.

### 3.2 Plugin / Extension Points
**Pattern**: Future customization needs anticipated.
**Amplification**: Define extension interfaces in BP; isolate extension runtime; sandbox untrusted extensions.

### 3.3 Multi-Tenancy Primitives
**Pattern**: Single-tenant now; multi-tenant later.
**Amplification**: Tenant context propagation; data isolation strategy; per-tenant config/limits; shared vs dedicated.

### 3.4 Audit Trail / Event Sourcing
**Pattern**: "What happened?" questions unanswerable.
**Amplification**: Immutable event log for all state changes; projections for read models; replay capability.

### 3.5 Dry-Run / Simulation Mode
**Pattern**: Fear of production changes.
**Amplification**: All mutating operations support `dry_run=true` returning predicted effects without side effects.

### 3.6 Batch / Streaming Duality
**Pattern**: Batch today; streaming tomorrow (or vice versa).
**Amplification**: Unified processing model; same logic runs in batch (scheduled) and streaming (event-driven).

---

## 4. Architectural Amplification Patterns

### 4.1 Explicit Module Boundaries
**Pattern**: Implicit coupling through shared DB, global state, circular imports.
**Amplification**: Define bounded contexts; explicit APIs; no cross-boundary data access; anti-corruption layers.

### 4.2 Contract-First Development
**Pattern**: Implementation drives interface; breaking changes surprise consumers.
**Amplification**: OpenAPI/Protobuf contracts as source of truth; consumer-driven contract tests; breaking change detection in CI.

### 4.3 Dependency Inversion
**Pattern**: High-level modules depend on low-level details.
**Amplification**: Invert dependencies via interfaces; dependency injection; infrastructure at edges only.

### 4.4 Event-Driven Decoupling
**Pattern**: Synchronous call chains create temporal coupling.
**Amplification**: Domain events for cross-boundary communication; event bus/broker; eventual consistency by default.

### 4.5 CQRS (Command Query Responsibility Segregation)
**Pattern**: Single model serves conflicting read/write needs.
**Amplification**: Separate write model (commands, aggregates) from read models (projections, materialized views).

### 4.6 Strangler Fig / Branch by Abstraction
**Pattern**: Big-bang rewrite risk.
**Amplification**: Incremental migration pattern; facade/proxy; parallel run with comparison; gradual cutover.

### 4.7 Sidecar / Ambassador Pattern
**Pattern**: Cross-cutting concerns pollute business logic.
**Amplification**: Extract observability, security, resilience to sidecar; business logic stays pure.

---

## 5. Operational Amplification Patterns

### 5.1 Structured Logging (JSON + Correlation IDs)
**Pattern**: Unstructured logs unqueryable.
**Amplification**: Mandatory fields: timestamp, level, service, trace_id, span_id, user_id, operation; JSON format.

### 5.2 Distributed Tracing (W3C TraceContext)
**Pattern**: Request flow invisible across services.
**Amplification**: Automatic instrumentation; span attributes for business context; sampling strategy.

### 5.3 Metrics: RED + USE Methods
**Pattern**: Metrics exist but don't answer "is it healthy?"
**Amplification**: 
- RED: Rate, Errors, Duration per service/endpoint
- USE: Utilization, Saturation, Errors per resource (CPU, disk, network, queue)

### 5.4 Alerting: Symptom-Based, Not Cause-Based
**Pattern**: Alerts on CPU>80% (cause) not "request latency p99 > 2s" (symptom).
**Amplification**: Alert on user-visible symptoms; runbook-linked; auto-resolve; no paging for self-healing.

### 5.5 Health Checks: Liveness / Readiness / Startup
**Pattern**: Single /health endpoint; K8s kills starting pods.
**Amplification**: Three probes: liveness (deadlock), readiness (dependencies), startup (slow init); deep checks for readiness.

### 5.6 Runbook Automation
**Pattern**: Runbooks are wiki pages nobody reads during incidents.
**Amplification**: Executable runbooks (scripts/notebooks); auto-diagnosis; one-click remediation where safe.

### 5.7 Rollout Strategy: Canary → Progressive → Full
**Pattern**: Big-bang deployments cause incidents.
**Amplification**: Automated canary analysis (metrics comparison); progressive traffic shift; instant rollback.

### 5.8 Capacity Planning & Autoscaling
**Pattern**: Reactive scaling; OOM kills; cost surprises.
**Amplification**: Predictive scaling (time-series forecasting); load testing baselines; cost dashboards per feature.

### 5.9 Disaster Recovery Drills
**Pattern**: DR plan exists but never tested.
**Amplification**: Quarterly DR drills; RTO/RPO measurement; automated failover; chaos engineering integration.

### 5.10 Security Observability
**Pattern**: Security events invisible in standard monitoring.
**Amplification**: Auth failures, authorization denials, anomaly detection as first-class metrics; SIEM integration.

---

## 6. Opportunity Discovery Patterns (Bonus)

### 6.1 Platform Extraction
**Pattern**: Multiple teams building same infrastructure.
**Discovery**: "This translation pipeline's normalization engine could serve document processing, catalog migration, content validation."
**Decision Framework**:
- NOW: Extract if 2+ immediate consumers
- LATER: Document as platform candidate; build with extraction in mind
- DO NOT DO: If single use case for foreseeable future

### 6.2 Data Product Thinking
**Pattern**: Data produced as byproduct; could be product.
**Discovery**: "The translation quality metrics we collect could be a data product for ML training."
**Decision**: Same NOW/LATER/DO NOT DO framework.

### 6.3 Protocol Generalization
**Pattern**: Custom protocol solves general problem.
**Discovery**: "Our idempotency key protocol works for any async mutation."
**Decision**: Extract to library if reusable; document pattern if not.

### 6.4 Computational Reuse
**Pattern**: Heavy computation repeated across use cases.
**Discovery**: "The embedding generation in translation also serves search, classification, deduplication."
**Decision**: Shared service with clear SLOs; cache layer; quota management.

---

## Usage During Phase 5

1. **Systematic Scan**: For each amplification type, scan the decision set against relevant patterns
2. **Traceability**: Every amplification must trace to a specific gap (Phase 2) or opportunity (Phase 3)
3. **Justification**: Document why this amplification, why now, and what it costs
4. **Scope Control**: Apply NOW/LATER/DO NOT DO to every candidate; only NOW items go into hardened set
5. **Interaction Check**: Verify amplifications don't conflict (e.g., CQRS + Event Sourcing = natural pair; CQRS + simple CRUD = over-engineering)