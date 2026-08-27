# code-review-workflow Operational Checklist

## Phase 1: Pre-Execution Discovery & Constraints
- [ ] Inspect all target files, schemas, and specifications before modifying code.
- [ ] Verify that upstream and downstream dependencies in **Structured Code Review Process & Team Etiquette** are identified.
- [ ] Confirm that existing baseline test suites run and pass cleanly (`exit code 0`).
- [ ] Validate zero-trust boundaries, input parameters, and non-functional requirements.

---

## Phase 2: Domain-Specific Implementation Standards
- [ ] Apply canonical design patterns specific to **Structured Code Review Process & Team Etiquette**.
- [ ] Maintain strict type safety, explicit type annotations, and immutability where applicable.
- [ ] Implement deterministic error handling with structured, contextual exception types.
- [ ] Avoid any hidden mock values, stubbed returns, or unhandled promise/coroutine rejections.
- [ ] Ensure all log messages and telemetry events use structured formats.

---

## Phase 3: Invariant Protection & Edge Cases
- [ ] Handle null, empty, unexpected, or malformed input payloads safely.
- [ ] Validate concurrent access safety and race-condition freedom under load.
- [ ] Ensure resource cleanup (close database handles, sockets, file descriptors) in `finally` blocks.
- [ ] Verify idempotency on retried operations.

---

## Phase 4: Completion & Verification Gate
- [ ] Run full automated test suite with 100% pass rate.
- [ ] Execute linter and static analysis tools with zero warnings.
- [ ] Confirm documentation and code comments accurately reflect actual implementation.
- [ ] Record verification evidence in walkthrough or execution report.
