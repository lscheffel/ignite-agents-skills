# ADR-033 Blueprint: Backend, Data, Cloud & Security Domain SOTA

> **Companion Artifact to:** [ADR-033.md](./ADR-033.md)  
> **Type:** Technical Architecture Blueprint (Tier II)  
> **Status:** APPROVED  

---

## 1. Mathematical Models & Protocol Contracts

### 1.1 B-Tree Index Selectivity & Cardinality (`database-architecture`)

Index efficacy is measured by **Index Selectivity ($S_{\text{idx}}$)**:

$$S_{\text{idx}} = \frac{D_{\text{distinct}}}{N_{\text{total}}} \in (0, 1]$$

**Index Gating Rule:**
- If $S_{\text{idx}} \ge 0.15$ ($15\%$ distinct values): B-Tree index is highly effective.
- If $S_{\text{idx}} < 0.05$: B-Tree index causes index bloat; use Partial Index or Bitmap Index instead.

---

### 1.2 Capacity Planning & Latency: Little's Law (`performance-optimization`)

The average number of concurrent requests ($L$) in a stable system is governed by **Little's Law**:

$$L = \lambda \cdot W$$

Where:
- $\lambda$ is the arrival throughput (requests per second).
- $W$ is the mean latency / response time (seconds).

#### Amdahl's Law for Parallel Speedup:
$$S_{\text{latency}}(s) = \frac{1}{(1 - p) + \frac{p}{s}}$$

Where $p$ is the fraction of code parallelizable, and $s$ is the number of parallel workers.

---

### 1.3 RFC 7807 Problem Details Error Contract (`api-design`)

All RESTful HTTP error responses must adhere to RFC 7807 (`application/problem+json`):

```json
{
  "type": "https://api.example.com/errors/resource-not-found",
  "title": "Resource Not Found",
  "status": 404,
  "detail": "The skill 'unknown-skill' could not be found in the catalog.",
  "instance": "/skills/unknown-skill",
  "code": "SKILL_NOT_FOUND",
  "timestamp": "2026-08-26T23:45:00Z"
}
```

---

### 1.4 STRIDE Threat Modeling Matrix (`security-review`)

Security reviews map vulnerabilities against the **STRIDE Model**:

| Threat | Security Property | Mitigation Strategy |
|:---|:---|:---|
| **S**poofing | Authenticity | Mutual TLS, JWT with asymmetric RS256, secure cookies (`HttpOnly; Secure; SameSite=Strict`). |
| **T**ampering | Integrity | HMAC signatures, TLS in-transit encryption, database parameterization. |
| **R**epudiation | Non-repudiation | Immutable append-only audit logs, cryptographic commit attestation. |
| **I**nformation Disclosure | Confidentiality | Secrets management (Vault/KMS), TLS 1.3, PII masking, least privilege RBAC. |
| **D**enial of Service | Availability | Token Bucket rate limiting, Circuit Breaker FSM, request timeouts. |
| **E**levation of Privilege | Authorization | Strict RBAC/ABAC, object-level access control (BOLA/IDOR prevention). |
