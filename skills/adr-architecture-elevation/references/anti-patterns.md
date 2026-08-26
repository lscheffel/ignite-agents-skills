# Architectural Anti-Patterns — Detection Catalog

## Purpose

Reference catalog of common architectural anti-patterns to actively detect during Phase 3 (Architecture Challenge). Each anti-pattern includes detection signals, consequences, and preferred alternatives.

---

## Structural Anti-Patterns

### 1. Distributed Monolith
**Signals**:
- Services share database or schema
- Synchronous call chains > 2 hops for single operation
- Shared libraries with business logic deployed everywhere
- Deploying one service requires deploying others
- Distributed transactions (saga) for basic operations

**Consequences**: Worst of both worlds — operational complexity of microservices without autonomy benefits

**Alternative**: True bounded contexts with async communication; shared-nothing architecture

---

### 2. God Service / Mega-Service
**Signals**:
- Single service owns > 30% of domain entities
- Service has > 10 database tables
- Team cannot work independently on different features
- Long-lived feature branches; merge conflicts constant
- Cognitive load exceeds team capacity

**Consequences**: Bottleneck for changes; scaling requires scaling everything; single point of failure

**Alternative**: Decompose by bounded context; apply Single Responsibility at service level

---

### 3. Anemic Domain Model
**Signals**:
- Entities are data bags (getters/setters only)
- Business logic in "service" layer (Transaction Script)
- Domain rules scattered across controllers, services, validators
- No encapsulation of invariants
- DTOs mirror entities 1:1

**Consequences**: Logic duplication; invariant violations; difficult to test; procedural not object-oriented

**Alternative**: Rich domain models; entities enforce invariants; domain services for cross-entity logic

---

### 4. Shared Database Integration
**Signals**:
- Multiple services read/write same tables
- Schema changes require coordinated deployments
- "Just add a column" breaks other services
- Reporting queries join across service tables
- No schema ownership

**Consequences**: Implicit coupling; deployment coordination; schema evolution paralysis

**Alternative**: Database per service; API-only integration; CDC for read models; data mesh principles

---

### 5. Chatty Communication
**Signals**:
- Single user request triggers > 5 service calls
- Latency dominated by network hops
- N+1 query patterns across services
- No API aggregation / BFF layer

**Consequences**: High latency; cascade failures; difficult debugging; poor user experience

**Alternative**: API Gateway/BFF; GraphQL federation; composite APIs; materialized views

---

## Data & Consistency Anti-Patterns

### 6. Distributed Transactions (2PC) in Business Flow
**Signals**:
- XA transactions across services
- Saga orchestrators with > 5 steps for simple flows
- Compensating transactions as complex as forward
- Long-running transactions holding locks

**Consequences**: Low availability; lock contention; complexity explosion; operational nightmares

**Alternative**: Eventual consistency; outbox pattern; choreography over orchestration; idempotency

---

### 7. Event Sourcing Without Need
**Signals**:
- Event store for simple CRUD domain
- No temporal query requirements
- No audit/regulatory requirement
- Projections rebuilt on every deploy
- Team unfamiliar with event modeling

**Consequences**: Unnecessary complexity; steep learning curve; projection rebuild pain; over-engineering

**Alternative**: State-based persistence with audit log; event sourcing only where temporal queries needed

---

### 8. CQRS Without Justification
**Signals**:
- Separate read/write models for simple domain
- Same data, different shape — could be views
- Synchronization complexity between models
- No performance or scalability driver

**Consequences**: Double the models; eventual consistency confusion; sync bugs; team cognitive load

**Alternative**: Start with single model; add read replicas/views; CQRS only when read/write patterns diverge significantly

---

### 9. Cache-Aside Without Invalidation Strategy
**Signals**:
- TTL-only expiration
- Stale reads accepted without documentation
- No cache stampede protection
- Cache keys embed business logic

**Consequences**: Silent data inconsistency; thundering herd; debugging nightmare

**Alternative**: Write-through / read-through; explicit invalidation on write; versioned keys; single-flight

---

### 10. Premature Materialization
**Signals**:
- Pre-computed aggregates for queries that run < 1/sec
- Multiple materialized views for same data
- Refresh lag causes user-visible inconsistency
- Complex refresh logic (incremental, partial, full)

**Consequences**: Write amplification; consistency lag; operational complexity; YAGNI

**Alternative**: Query optimization first; materialize only when proven necessary; real-time views where possible

---

## Communication & Contract Anti-Patterns

### 11. Integration Database / Shared Schema
**Signals**: (See #4 Shared Database Integration)

### 12. Consumer-Driven Contract Absence
**Signals**:
- Provider changes break consumers silently
- No contract tests in CI
- Versioning only in URL (/v1/, /v2/)
- Breaking changes deployed without migration period

**Consequences**: Fear of change; integration hell; consumer distrust; shadow APIs

**Alternative**: Consumer-driven contract testing (Pact); explicit versioning; deprecation policy; parallel run

---

### 13. RPC-Over-HTTP (Not REST, Not GraphQL, Not gRPC)
**Signals**:
- HTTP POST for everything
- Verbs in URL (/getUser, /updateOrder)
- No standard status codes
- Custom error formats
- No caching, no HATEOAS

**Consequences**: No tooling support; no caching; fragile; not interoperable

**Alternative**: Choose one: REST (resource-oriented), GraphQL (query flexibility), gRPC (performance/contracts)

---

### 14. Synchronous Communication for Async Work
**Signals**:
- HTTP call with 30s+ timeout
- Polling for completion
- Client holds connection during background work
- No webhook/callback mechanism

**Consequences**: Resource exhaustion; timeout cascades; poor UX; unnatural coupling

**Alternative**: Async APIs with 202 Accepted + webhook/callback; polling only as fallback; SSE/WebSocket for progress

---

## Operational Anti-Patterns

### 15. Pet Services (Not Cattle)
**Signals**:
- Manual deployment steps
- Named servers (not ephemeral)
- SSH access required for debugging
- Unique snowflake configurations
- No automated recovery

**Consequences**: High MTTR; scaling manual; knowledge silos; bus factor = 1

**Alternative**: Immutable infrastructure; GitOps; declarative config; self-healing; chaos engineering

---

### 16. Observability Theater
**Signals**:
- Logs exist but unstructured
- Metrics exist but no alerts
- Traces sampled at 1%
- Dashboards show "green" during incidents
- No correlation between logs/metrics/traces

**Consequences**: Blind during incidents; MTTD high; root cause guesswork

**Alternative**: Structured JSON logs; RED/USE metrics; 100% trace sampling for errors; correlated IDs; SLO-based alerting

---

### 17. Alert Fatigue / Paging on Symptoms
**Signals**:
- > 5 pages/week per engineer
- Alerts on CPU, memory, disk (causes)
- No runbooks linked to alerts
- Auto-resolving alerts still page
- "Watch" alerts that never fire

**Consequences**: Burnout; ignored alerts; real incidents missed; normalization of deviance

**Alternative**: Symptom-based alerting (SLO burn rate); runbook per alert; auto-remediation; alert review cadence

---

### 18. Configuration as Code Without Validation
**Signals**:
- Config in Git but no schema validation
- Typos in prod config cause outages
- No config drift detection
- Secrets in config files
- Environment-specific config duplication

**Consequences**: Config-induced outages; security exposure; drift; deployment anxiety

**Alternative**: Config schema validation (CUE, JsonSchema); GitOps with drift detection; secret management (Vault, SealedSecrets); templating with validation

---

### 19. Manual Runbooks
**Signals**:
- Runbooks in Confluence/Notion
- Steps require human judgment at every step
- No automation for common remediation
- Runbook last updated > 6 months ago
- New hires cannot execute runbooks

**Consequences**: High MTTR; inconsistent execution; knowledge loss; training burden

**Alternative**: Executable runbooks (Jupyter, RunWhen, custom); one-click remediation; automated diagnosis; runbook testing in CI

---

## Security Anti-Patterns

### 20. Perimeter-Only Security
**Signals**:
- VPN/firewall as primary defense
- Internal services trust each other implicitly
- No mTLS between services
- No zero-trust network policies

**Consequences**: Lateral movement trivial; breach blast radius = entire network

**Alternative**: Zero-trust; mTLS everywhere; service mesh; network policies; identity-based auth

---

### 21. Secrets in Code / Config
**Signals**:
- API keys in .env files committed
- Database passwords in Helm values
- JWT secrets in Docker images
- No secret rotation

**Consequences**: Credential leakage; compliance violations; rotation impossible

**Alternative**: Secret managers (Vault, AWS Secrets Manager, GCP Secret Manager); external secrets operator; rotation automation

---

### 22. Authorization as Afterthought
**Signals**:
- AuthZ checks only at API gateway
- No field-level or row-level security
- "Admin" role bypasses all checks
- No audit trail for authorization decisions

**Consequences**: Data leakage; privilege escalation; audit failures

**Alternative**: Zero-trust authZ; policy-as-code (OPA/Cedar); field/row-level; decision logging

---

## Process Anti-Patterns

### 23. Architecture by Committee
**Signals**:
- Every decision requires 5+ approvals
- ADRs take months to approve
- Lowest common denominator decisions
- No clear decision ownership

**Consequences**: Decision paralysis; mediocre architecture; frustration; shadow architecture

**Alternative**: Clear decision owners (RACI); lightweight ADR process; disagree and commit; time-boxed reviews

---

### 24. Architecture Astronautics
**Signals**:
- Kubernetes for 3-service system
- Event sourcing for CRUD app
- Service mesh for 2 services
- "Future-proofing" drives current complexity
- No proven need for scale

**Consequences**: Wasted resources; cognitive overload; delayed delivery; YAGNI violations

**Alternative**: Start simple; evolve with evidence; complexity budget; justify every abstraction

---

### 25. Not Invented Here (NIH) Syndrome
**Signals**:
- Custom orchestrator instead of Temporal/Camunda
- Custom cache instead of Redis
- Custom auth instead of Keycloak/Auth0
- Custom metrics instead of Prometheus
- "Our use case is unique"

**Consequences**: Maintenance burden; security gaps; hiring difficulty; reinventing bugs

**Alternative**: Default to boring technology; build vs buy framework; contribute upstream; customize only differentiating logic

---

## Detection Checklist for Phase 3

During Architecture Challenge, systematically check:

```
[ ] Distributed Monolith?
[ ] God Service?
[ ] Anemic Domain Model?
[ ] Shared Database?
[ ] Chatty Communication?
[ ] Distributed Transactions?
[ ] Unnecessary Event Sourcing?
[ ] Unjustified CQRS?
[ ] Cache Without Invalidation?
[ ] Premature Materialization?
[ ] Missing Consumer-Driven Contracts?
[ ] RPC-Over-HTTP?
[ ] Sync for Async Work?
[ ] Pet Services?
[ ] Observability Theater?
[ ] Alert Fatigue?
[ ] Config Without Validation?
[ ] Manual Runbooks?
[ ] Perimeter-Only Security?
[ ] Secrets in Code?
[ ] AuthZ Afterthought?
[ ] Architecture by Committee?
[ ] Architecture Astronautics?
[ ] NIH Syndrome?
```

Each detected anti-pattern becomes a finding in Phase 3 output with:
- Pattern name
- Evidence in current architecture
- Consequence if unaddressed
- Recommended alternative
- Effort to remediate