# Comparative Evaluation Criteria — Detailed Rubrics

## Purpose

Provide precise, evidence-based scoring criteria for the Phase 4 Comparative Architecture Evaluation Matrix. Each criterion must be scored with specific evidence, not intuition.

---

## Scoring Scale

| Score | Label | Meaning |
|-------|-------|---------|
| 5 | Exceptional | Best-in-class; sets new standard for this criterion |
| 4 | Strong | Clearly above average; material advantage |
| 3 | Adequate | Meets requirements; no significant gaps |
| 2 | Weak | Notable gaps; requires remediation |
| 1 | Critical | Fails requirement; blocking issue |

---

## Criterion Definitions & Evidence Requirements

### 1. Correctness
**Definition**: Does the architecture correctly solve the stated problem under all specified conditions?

**Evidence Required**:
- Traceability from each problem goal to architectural decision
- Coverage of all failure conditions identified in Phase 1
- Handling of all invariants under concurrency/failure
- Formal or semi-formal verification of critical paths

**Scoring Guide**:
- 5: Proven correct for all problem dimensions; formal verification on critical paths
- 4: Correct for all stated goals; comprehensive failure condition coverage
- 3: Correct for primary goals; minor gaps in edge cases
- 2: Gaps in secondary goals or failure conditions
- 1: Does not solve core problem or violates invariants

---

### 2. Complexity (Code + Operations)
**Definition**: Total cognitive and operational burden to build, deploy, operate, and maintain.

**Evidence Required**:
- Component count and interaction complexity
- Lines of code / service count / configuration surface area
- Operational procedures required (runbooks, playbooks)
- Onboarding time for new team member
- Cyclomatic complexity of critical paths

**Scoring Guide**:
- 5: Radical simplicity; single-digit services; self-documenting
- 4: Low complexity; clear boundaries; minimal operational burden
- 3: Moderate complexity; manageable with good tooling
- 2: High complexity; requires dedicated platform team
- 3: Extreme complexity; brittle; high cognitive load

---

### 3. Robustness
**Definition**: Ability to continue operating correctly under adverse conditions.

**Evidence Required**:
- Failure mode analysis (FMEA) coverage
- Graceful degradation behaviors defined
- Circuit breakers, retries, timeouts, bulkheads implemented
- Data consistency guarantees under partition
- Recovery time objectives (RTO) and recovery point objectives (RPO) met

**Scoring Guide**:
- 5: Antifragile; improves under stress; self-healing
- 4: Comprehensive failure handling; automatic recovery; no data loss
- 3: Handles common failures; manual intervention for rare cases
- 2: Fragile; cascading failures likely; data loss possible
- 1: Single points of failure; no recovery strategy

---

### 4. Testability
**Definition**: Ease and completeness of verifying correctness at all levels.

**Evidence Required**:
- Unit test coverage % (target: >90% on business logic)
- Integration test strategy and coverage
- Contract testing between services
- Chaos engineering / fault injection capability
- Deterministic reproducibility of production issues
- Test execution time (CI pipeline duration)

**Scoring Guide**:
- 5: Fully testable at all levels; fast deterministic tests; chaos-ready
- 4: Strong testability; good coverage; reasonable CI time
- 3: Adequate unit/integration; gaps in contract/E2E
- 2: Difficult to test; slow flaky tests; gaps in critical paths
- 1: Effectively untestable; no automation strategy

---

### 5. Operability
**Definition**: Ease of operating, monitoring, debugging, and evolving in production.

**Evidence Required**:
- Observability: metrics, logs, traces coverage (RED/USE methods)
- Alerting strategy: actionable alerts, low noise
- Debugging: correlation IDs, distributed tracing, live introspection
- Deployment: zero-downtime, rollback < 5 min, feature flags
- Capacity planning: autoscaling, cost visibility
- Runbook completeness for top 10 scenarios

**Scoring Guide**:
- 5: Self-operating; predictive; zero-touch for routine ops
- 4: Excellent observability; fast debugging; safe deployments
- 3: Basic observability; manual debugging; standard deployments
- 2: Poor visibility; risky deployments; reactive firefighting
- 1: Blind in production; deployments cause incidents

---

### 6. Performance
**Definition**: Meets latency, throughput, and resource efficiency targets.

**Evidence Required**:
- Latency percentiles (p50, p95, p99) under load
- Throughput capacity with headroom
- Resource utilization efficiency (CPU, memory, network, disk)
- Scaling behavior (horizontal/vertical)
- Cost per transaction/request

**Scoring Guide**:
- 5: Exceeds targets with 10x headroom; optimal resource use
- 4: Meets all targets with comfortable headroom
- 3: Meets targets; limited headroom; some inefficiency
- 2: Misses targets under load; significant inefficiency
- 1: Cannot meet targets; architecture fundamentally limited

---

### 7. Security
**Definition**: Resistance to threats; compliance with security requirements.

**Evidence Required**:
- Threat model (STRIDE/PASTA) coverage
- Authentication/authorization architecture
- Data encryption (at rest, in transit, in use)
- Supply chain security (SBOM, dependency scanning)
- Secrets management
- Audit logging completeness
- Compliance mapping (SOC2, GDPR, etc.)

**Scoring Guide**:
- 5: Zero-trust by default; continuous verification; compliance automated
- 4: Strong security posture; defense in depth; good threat model
- 3: Baseline security; some gaps in threat coverage
- 2: Significant vulnerabilities; weak threat model
- 1: Critical security flaws; non-compliant

---

### 8. Maintainability
**Definition**: Ease of modifying, extending, and refactoring over time.

**Evidence Required**:
- Module coupling/cohesion metrics
- API stability and versioning strategy
- Technical debt index (SonarQube or equivalent)
- Refactoring safety (test coverage on changed code)
- Architecture decision record freshness
- Dependency freshness (no abandoned libraries)

**Scoring Guide**:
- 5: Designed for change; pluggable; debt near zero
- 4: Low coupling; clear boundaries; manageable debt
- 3: Moderate coupling; some debt; refactoring possible
- 2: High coupling; significant debt; risky changes
- 1: Big ball of mud; changes break unrelated features

---

### 9. Cost (Build + Run)
**Definition**: Total cost of ownership — development, infrastructure, operations.

**Evidence Required**:
- Development effort estimate (person-weeks)
- Infrastructure cost model (cloud pricing calculator)
- Operational staffing requirements
- Licensing costs
- Opportunity cost of complexity

**Scoring Guide**:
- 5: Minimal cost; serverless/managed; high leverage
- 4: Reasonable cost; good ROI; efficient resource use
- 3: Expected cost for problem class; some waste
- 2: High cost; over-provisioned; poor ROI
- 1: Prohibitive cost; architecture unsustainable

---

### 10. Reversibility
**Definition**: Ability to change course or rollback architectural decisions.

**Evidence Required**:
- Data migration strategy (forward/backward compatibility)
- API versioning and deprecation policy
- Feature flag coverage for new paths
- Strangler Fig / Branch by Abstraction readiness
- Contract test reversibility

**Scoring Guide**:
- 5: Fully reversible at all layers; zero-downtime migration
- 4: Reversible with planned migration; low risk
- 3: Partially reversible; some one-way doors
- 2: Significant irreversible decisions; high migration cost
- 1: Architecture locks in; cannot pivot

---

### 11. Operational Complexity
**Definition**: Distinct from code complexity — the day-to-day operational burden.

**Evidence Required**:
- Number of moving parts requiring human attention
- Specialized expertise required (e.g., Kafka tuning, K8s expertise)
- Incident frequency and MTTR
- On-call burden
- Compliance/audit overhead

**Scoring Guide**:
- 5: Runs itself; no specialized ops skills needed
- 4: Standard ops skills sufficient; low incident rate
- 3: Some specialized skills; manageable on-call
- 2: Requires dedicated specialists; frequent incidents
- 1: Requires heroics; unsustainable operational model

---

## Matrix Completion Rules

1. **Every cell must have evidence** — No scoring without specific evidence reference
2. **Weighting** — Apply problem-specific weights (document in Phase 4 output)
3. **Tie-breaking** — When tied, prefer lower complexity / higher reversibility
4. **Veto** — Any criterion scored 1 (Critical) triggers automatic REPLACE recommendation unless mitigated
5. **Documentation** — Record score rationale in Phase 4 output for auditability

---

## Weighting Guidance

Default weights (adjust per problem context):

| Criterion | Default Weight | High-Stakes Adjustment |
|-----------|----------------|------------------------|
| Correctness | 25% | 30% |
| Robustness | 20% | 25% |
| Operability | 15% | 15% |
| Security | 10% | 15% |
| Testability | 10% | 5% |
| Maintainability | 8% | 5% |
| Performance | 5% | 3% |
| Cost | 4% | 2% |
| Reversibility | 2% | 0% |
| Complexity | 1% | 0% |

*Note: Complexity and Reversibility are inverse weights — lower is better*