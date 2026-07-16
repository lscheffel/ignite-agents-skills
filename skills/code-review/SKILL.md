---

name: code-review
description: >
Autonomous multi-agent code review runtime protocol with deterministic execution,
semantic code analysis, consensus voting, immutable audit trails, supply-chain
security verification and fail-closed governance enforcement.

version: 4.0.0
maturity: autonomous-runtime
classification: critical-governance-component

owner: Architecture Governance Board

tags:

* code-review
* governance
* security
* autonomous-agents
* supply-chain
* audit
* compliance

triggers:

* task_completion
* feature_completion
* pre_commit
* pre_merge
* release_candidate
* production_deployment

required_before_merge: true
audit_required: true
consensus_required: true
minimum_reviewers: 3

capabilities:

* semantic_analysis
* dependency_scanning
* security_review
* architecture_review
* performance_review
* audit_generation
* consensus_evaluation

dependencies:
external_tools:
- syft
- gitleaks
- pip-audit
- npm-audit
- cargo-audit
- grype

integrations:

* planning
* acceptance-testing
* security-review
* self-learning
* verification-before-completion

## skill_type: RIGID

# Code Review v4.0

## Mission

Guarantee that no code reaches production without:

* specification compliance
* architectural compliance
* security compliance
* operational compliance
* supply-chain compliance
* audit traceability

---

# Runtime Principles

1. Zero Trust
2. Least Privilege
3. Defense in Depth
4. Immutable Audit Trail
5. Human Override
6. Multi-Agent Consensus
7. No Raw Untrusted Context
8. Fail Closed

---

# Runtime State Machine

```text
INITIALIZED
    ↓
DEPENDENCY_VERIFICATION
    ↓
INPUT_SANITIZATION
    ↓
SEMANTIC_EXTRACTION
    ↓
REVIEW_DISPATCH
    ↓
CONSENSUS_EVALUATION
    ↓
AUDIT_PERSISTENCE
    ↓
MERGE_APPROVED
```

Terminal states:

```text
MERGE_BLOCKED
ESCALATED
FAILED
```

---

# Phase 0 — Dependency Verification

## Generate SBOM

```bash
syft . -o json > sbom.json
```

## Dependency Security Scanning

Python:

```bash
pip-audit
```

Node:

```bash
npm audit --audit-level high
```

Rust:

```bash
cargo audit
```

Containers:

```bash
grype .
```

## Approved Tool Verification

Every executable dependency MUST satisfy:

* approved version
* cryptographic hash verification
* signature validation
* approved trust level

Failure result:

```text
BLOCK_EXECUTION
```

---

# Phase 1 — Input Sanitization

## Objective

Transform untrusted inputs into trusted semantic artifacts.

## Security Gateway Pipeline

```text
RAW INPUT
    ↓
Tokenizer
    ↓
Parser
    ↓
Metadata Extractor
    ↓
Normalizer
    ↓
Schema Validator
    ↓
Policy Validator
    ↓
Serializer
    ↓
TRUSTED ARTIFACT
```

## Forbidden Inputs

Never expose directly to reviewer agents:

* raw git diff
* shell output
* stack traces
* environment variables
* secrets
* credentials
* configuration files

## Secret Detection

Execute:

```bash
gitleaks detect
detect-secrets scan
trufflehog git .
```

Detection result:

```text
BLOCK_MERGE
ESCALATE_SECURITY
```

---

# Phase 2 — Semantic Extraction

## Allowed Artifacts

* AST
* Semantic Graph
* Code Property Graph
* Dependency Graph

## Forbidden Artifact

```text
RAW_DIFF
```

## Semantic Change Schema

```json
{
  "change_id": "uuid",
  "change_type": "function_added",
  "module": "auth.py",
  "symbol": "validate_token",
  "dependencies_added": ["jwt"],
  "security_impact": true,
  "behavior_change": true,
  "breaking_change": false,
  "risk_score": 0.82
}
```

---

# Phase 3 — Review Dispatch

## Reviewer Swarm

### Architecture Reviewer

Responsibilities:

* complexity
* maintainability
* coupling
* modularity

### Security Reviewer

Responsibilities:

* OWASP Top 10
* secrets
* injection
* authentication
* authorization
* supply-chain risk

### Quality Reviewer

Responsibilities:

* readability
* duplication
* testing
* conventions

### Performance Reviewer

Responsibilities:

* complexity analysis
* scalability
* memory consumption
* hot paths

---

# Agent Runtime Contract

Example:

```yaml
agent_id: security-reviewer

timeout_seconds: 300
max_tokens: 25000
retries: 2

resources:
  cpu_limit: 1
  memory_limit_mb: 1024

permissions:
  filesystem:
    mode: readonly

  network:
    enabled: false

  shell:
    whitelist:
      - pip-audit
      - pytest
```

---

# Phase 4 — Consensus Evaluation

## Voting Weights

| Reviewer     | Weight |
| ------------ | ------ |
| Security     | 0.35   |
| Architecture | 0.25   |
| Quality      | 0.20   |
| Performance  | 0.20   |

## Decision Rules

Automatic rejection:

* critical vulnerability
* secret exposure
* authentication failure
* undefined behavior
* missing audit

Automatic escalation:

* consensus score < 0.75
* conflicting findings
* reviewer timeout

Automatic approval:

* consensus score ≥ 0.90
* no blocking findings

---

# Phase 5 — Immutable Audit

## Audit Artifact

```json
{
  "review_id": "uuid",
  "trace_id": "uuid",
  "timestamp": "iso8601",
  "semantic_diff_hash": "sha256",
  "reviewers": [],
  "votes": [],
  "consensus_score": 0.0,
  "decision": "approve",
  "signature": "ed25519"
}
```

## Protection

Encryption:

```text
AES256-GCM
```

Integrity:

```text
SHA256
Ed25519
```

Access:

```text
RBAC_REQUIRED
```

---

# Failure Matrix

| Failure                   | Action              |
| ------------------------- | ------------------- |
| Dependency scan timeout   | Block merge         |
| Semantic parser failure   | Escalate            |
| Reviewer timeout          | Retry then escalate |
| Consensus failure         | Escalate            |
| Audit persistence failure | Block merge         |

---

# Governance Lifecycle

## Versioning

* MAJOR → Runtime changes
* MINOR → New reviewers or capabilities
* PATCH → Policy updates

## Change Requirements

Every change requires:

* ADR
* Security Review
* Architecture Approval
* Migration Guide

## Deprecation Policy

* minimum support period: 24 months
* migration window: 12 months

---

# Validation Suite

Mandatory scenarios:

* prompt injection
* dependency poisoning
* tool compromise
* reviewer compromise
* secret leakage
* consensus split
* audit corruption

---

# Iron Law

```text
NO MERGE WITHOUT REVIEW
NO REVIEW WITHOUT CONSENSUS
NO CONSENSUS WITHOUT AUDIT
NO AUDIT WITHOUT TRACEABILITY
NO EXCEPTIONS
```

---

# Final Rule

If uncertainty exists:

```text
FAIL_CLOSED
BLOCK_MERGE
ESCALATE
```
