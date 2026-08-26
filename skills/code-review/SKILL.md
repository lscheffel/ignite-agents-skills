---
name: code-review
version: 5.0.0
description: Unified code review engine supporting fast iterative review (mode: lite) and rigorous multi-agent consensus verification (mode: full).
domain: engineering-quality
triggers:
- code-review
- code-review-lite
- review_code
- task_completion
- feature_completion
- pre_commit
- pre_merge
- release_candidate
- production_deployment
tags:
- code-review
- governance
- security
- autonomous-agents
- fast-feedback
- audit
- compliance
metadata:
  author: Antigravity Refactored Architecture
  provenance: internal
  last_audited: '2026-08-24'
---

# Unified Code Review Engine (v5.0.0)

This unified engine operates in two interchangeable modes of intensity:

```
                                  UNIFIED CODE REVIEW ENGINE
                                                │
                       ┌────────────────────────┴────────────────────────┐
                       ▼                                                 ▼
             [ MODE: LITE (Default) ]                           [ MODE: FULL (Audit) ]
        - Fast Feedback (30-90s)                        - Multi-Agent Pipeline
        - Logical Regression Checks                 - SBOM and Supply-Chain Security
        - Immediate Security Sanity Checks              - Consensus Voting (Council)
        - Vibe-coding and Iterative PRs                  - Audit Trail and Immutability
```

## Mode Selection

| Mode | Typical Triggers | Average Time | Scope of Verification |
|---|---|:---:|---|
| **`mode: lite`** *(Default)* | "review this diff", "fast code review", "check if I broke something", iterative commits, vibe-coding. | ~30-90s | Logical regressions, immediate security (OWASP Top 10), linting, testing, and alignment with the plan. |
| **`mode: full`** | "formal architecture review", "critical pre-merge", "release candidate", multi-agent audit. | ~3-10 min | Formal verification of SBOM, supply-chain security, multi-agent council deliberation, consensus, and audit trail. |

---

# Runtime Principles

1. Zero Trust
2. Least Privilege
3. Defense in Depth
4. Immutable Audit Trail
5. Human Override
6. Multi-Agent Consensus (in Full Mode)
7. No Raw Untrusted Context
8. Fail Closed

---

## Operational Flow: Lite Mode (Fast Guardrail)

When executed in `mode: lite`:
1. **Delta Analysis:** Inspect only recent `git diff` modifications.
2. **Sanity Check:** Verify if implicit assumptions were broken and if automated tests cover the change.
3. **Security Sanity:** Verify SQL injection, hardcoded credentials, XSS, and input validation.
4. **Rapid Verdict:** Return immediately with a list of improvements and approval/blocking in direct format.

---

## Operational Flow: Full Mode (Multi-Agent Protocol)

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
- approved version
- cryptographic hash verification
- signature validation
- approved trust level

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
- raw git diff
- shell output
- stack traces
- environment variables
- secrets
- credentials
- configuration files

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
- Abstract Syntax Tree (AST)
- Semantic Graph
- Code Property Graph
- Dependency Graph

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
- complexity
- maintainability
- coupling
- modularity

### Security Reviewer

Responsibilities:
- OWASP Top 10
- secrets
- injection
- authentication
- authorization
- supply-chain risk

### Quality Reviewer

Responsibilities:
- readability
- duplication
- testing
- conventions

### Performance Reviewer

Responsibilities:
- complexity analysis
- scalability
- memory consumption
- hot paths

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
- critical vulnerability
- secret exposure
- authentication failure
- undefined behavior
- missing audit

Automatic escalation:
- consensus score < 0.75
- conflicting findings
- reviewer timeout

Automatic approval:
- consensus score ≥ 0.90
- no blocking findings

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
- MAJOR → Runtime changes
- MINOR → New reviewers or capabilities
- PATCH → Policy updates

## Change Requirements

Every change requires:
- ADR
- Security Review
- Architecture Approval
- Migration Guide

## Deprecation Policy
- minimum support period: 24 months
- migration window: 12 months

---

# Validation Suite

Mandatory scenarios:
- prompt injection
- dependency poisoning
- tool compromise
- reviewer compromise
- secret leakage
- consensus split
- audit corruption

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