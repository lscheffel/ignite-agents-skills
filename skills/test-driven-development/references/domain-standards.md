# Domain Standards: Test-Driven Development (TDD) Red-Green-Refactor Cycle

## 1. Architectural Foundations & Principles
This document outlines the authoritative engineering standards, design heuristics, and cognitive patterns governing **test-driven-development** within the **Test-Driven Development (TDD) Red-Green-Refactor Cycle** ecosystem.

### Core Invariants
1. **Single Source of Truth (SSOT):** All decisions and data schemas must have an unambiguous, single authoritative source.
2. **Determinism:** Execution routines must produce identical, verifiable outcomes given identical inputs.
3. **Cognitive Ergonomics:** APIs, interfaces, and documentation must minimize cognitive friction for both human engineers and autonomous AI agents.

---

## 2. Key Standards & References
- **Focus Areas:** Red-Green-Refactor, unit tests, mock isolation, test doubles, coverage invariants
- **Clean Architecture:** Enforce strict separation between Domain, Application, Infrastructure, and Interface layers.
- **Fail-Fast Heuristic:** Validate input schemas and pre-conditions at the boundary before initiating state transitions.

---

## 3. Anti-Patterns to Avoid
| Anti-Pattern | Description | Remediation Strategy |
|:---|:---|:---|
| **Ghost Mocks / Stubs** | Creating shallow placeholders to bypass checks without real logic. | Implement complete, production-grade logic with verified test harnesses. |
| **Leaky Abstractions** | Exposing internal infrastructure types through domain interfaces. | Use Data Transfer Objects (DTOs) and domain-specific value objects. |
| **Shotgun Debugging** | Modifying random code lines without forming scientific hypotheses. | Follow the 4-phase systematic debugging framework with reproducible traces. |
| **Unbounded Retries** | Retrying failing operations without backoff or circuit breaking. | Use exponential backoff with jitter and hard timeout thresholds. |

---

## 4. Decision Heuristics Matrix
```
   [ Incoming Request / Problem in Test-Driven Development (TDD) Red-Green-Refactor Cycle ]
               │
               ▼
   Is the problem well-defined and constrained?
        ├── YES ──► Follow Canonical Template & Execute TDD Loop
        └── NO  ──► Trigger Structured Discovery & Invariant Analysis
```
