---
name: implementation
version: 2.2.1
description:
  Executes previously planned changes in a governed and incremental manner, closing the SDLC cycle based on Agent Skills.
domain: domain-stack
triggers:
  - implementation
  - execute-changes
  - implement-feature
  - apply-plan
  - implementar-mudancas
  - executar-codigo
  - desenvolver-feature
  - fechar-ciclo-sdlc
tags:
  - implementation
  - execution
  - artifact-driven
  - sdlc
  - governance
  - tech-debt
related_skills:
  - adr-generator
  - adr-archive
  - agent-planning-execution
  - testing-mastery
  - git-workflow
  - technical-documentation
metadata:
  author: Antigravity Refactored Architecture
  provenance: internal
  last_audited: "2026-08-26"
---

# Implementation

Executes previously planned changes in a governed and incremental manner, closing the SDLC cycle based on Agent Skills.

## ⚠️ Token Optimization (Skip Consolidated & Frozen ADRs)

When you need to sweep ADRs from the repository to get context, **FIRST** read `docs/adr/ADR-INDEX.md` or perform a `grep` on the frontmatter of ADRs. You are **PROHIBITED** from reading the complete content (via `view_file` or `cat`) of any file with the tag `implementation_status: CONSOLIDATED` or `implementation_status: FROZEN` (or located in the `docs/adr/frozen/` directory). Apply the 'SKIP' summary to these files. Frozen ADRs (`FROZEN`) are approved for the future but are out of active scope and should not be implemented or reconciled until explicit user thawing.

## When to Use

### Use when:

- There is an approved ADR (status "Accepted") that needs to be implemented
- There is a Blueprint and TODO associated with the ADR
- Standardized and reproducible execution is required between different agents
- Complete traceability is required during implementation
- Execution Report is required at the end

### Do not use when:

- There is no ADR yet (use `adr-generator` first)
- Only code planning tasks without ADR are required (use `agent-planning-execution`)
- The change is trivial (< 1 file, < 30 minutes) and does not justify governance
- Only a single commit without intermediate validation is required

### Related Skills:

- `adr-generator` — generates ADRs that this skill consumes
- `adr-archive` — audits, archives, generates the Evidence Record (ER.md), and synchronizes technical debt
- `agent-planning-execution` — manages task decomposition and execution planning
- `testing-mastery` — executes tests during continuous validation
- `git-workflow` — manages commits and worktrees
- `technical-documentation` — updates documentation during implementation

## Decision Tree

```mermaid
graph TD
    A[Change requested] -->|Is there an ADR?| B{ADR found}
    B -->|No| C[Use adr-generator first]
    B -->|Yes| D{Is there a Blueprint?}
    D -->|No| E[Use adr-generator for Blueprint]
    D -->|Yes| F{Is there a TODO?}
    F -->|No| G[Use adr-generator for TODO]
    F -->|Yes| H{Execution Contract passes? (including depends_on)}
    H -->|No| I[Correct artifacts/dependencies before continuing]
    H -->|Yes| J[Start Execution Loop]
    J --> K[Select task via DAG]
    K --> L[Execute change]
    L --> M[Validate: build + lint + test]
    M -->|Found out-of-scope debt?| TD[Register via audit.py --register-debt]
    TD --> M
    M -->|Failed| N[Correct and re-validate]
    M -->|Passed| O[Update documentation]
    O --> P[Update TODO]
    P --> Q{More tasks?}
    Q -->|Yes| K
    Q -->|No| R[audit.py --archive ADR-XXX: Auto-generate ER.md and archive]
```

## Key Concepts

### Execution Contract

A mandatory contract that validates whether all necessary artifacts are present and consistent before any change.

**Contract fields:**

- ADR: path, status, decision
- Inter-ADR dependencies (`depends_on`): confirms that all prerequisite ADRs have a consolidated ER.md
- Blueprint: path, listed tasks
- TODO: path, tasks with states
- PI (Implementation Plan): path, granular steps (TDD) **[Optional/Recommended]**
- Branch: name, clean state
- Workspace: no uncommitted changes
- Affected files: extracted from PI
- Acceptance criteria: extracted from TODO and PI
- Rollback criteria: defined in the Blueprint

**Auto-Repair Rule:** If the Triad (ADR, BP, TODO) or PI is missing, malformed, or diverges from the standard templates, the skill should not abort. The agent should invoke the `adr-generator` skill in **Retroactive Governance** mode to generate or refactor missing artifacts before starting execution.

### Artifact Resolution

The process of automatic discovery and correlation of involved documents.

**Algorithm:**

1. Search for `ADR-XXX.md` in the `docs/adr/` directory
2. Derive paths: `ADR-XXX-BP.md`, `ADR-XXX-TODO.md`, `ADR-XXX-PI.md`
3. Verify existence of each artifact (PI is optional, but generates legacy execution if absent)
4. Extract `depends_on` and `related_skills` from the frontmatter
5. Map affected files from the PI
6. Return consolidated **Artifact Map**

### Execution Loop

The incremental execution model. The loop attempts to consume the PI (Implementation Plan) in granular steps (TDD). If the PI does not exist, the loop operates in **Legacy** mode, consuming directly the macro tasks from the TODO:

1. **Read** the detailed plan in `ADR-XXX-PI.md` (or the `ADR-XXX-TODO.md` in Legacy mode)
2. **Select** task (via DAG, respecting dependencies)
3. **Execute** the change in the code following the exact steps (TDD in the PI or macro-scope in the TODO)
4. **Validate** (build, lint, typecheck, tests)
5. **Update** affected documentation
6. **Mark** task as completed in the PI and reflect progress in the TODO
7. **Re-evaluate** dependencies (next tasks can start)

**Rules:**

- Maximum 1 task "In progress" at a time
- Task only starts if all dependencies are "Completed"
- If validation fails, task goes to "Blocked" until correction
- Big Bang is strictly prohibited
- **Scope Isolation & Tech Debt Offloading:** It is strictly forbidden to perform peripheral refactoring or alter files outside the scope of the current ADR/TODO/PI. Any opportunity for improvement, indirect coupling, or legacy code found during execution **MUST** be registered via the Janitor's CLI:
  ```bash
  python3 ~/.gemini/config/skills/adr-archive/scripts/audit.py . --register-debt --severity MEDIUM --domain <DOMAIN> --desc "<DESCRIPTION>" --origin "implementation:ADR-XXX"
  ```

### Change Lifecycle

The formal model of a change's lifecycle:

```
ADR → Blueprint → TODO → PI → Execution Contract (Inter-ADR Validation) → Artifact Resolution
  → Incremental Implementation → Validation (Scope Isolation & Debt Offloading)
  → Documentation Update → Algorithmic Evidence Record & Archival (audit.py)
```

## Workflow

### Workflow 1: Artifact Resolution

**Objective:** Discover and correlate all involved artifacts.

1. Identify the reference ADR (by name or context)
2. Derive paths: `ADR-XXX-BP.md`, `ADR-XXX-TODO.md`, `ADR-XXX-PI.md`
3. Verify existence of each artifact
4. Read frontmatter of the ADR to extract status, decision, and `depends_on`
5. Read Blueprint to extract macro phases
6. Read TODO to extract macro states
7. Read PI to extract granular tasks and code
8. Map `related_skills` from the frontmatter
9. Extract affected files from the PI
10. Return **Artifact Map** consolidated
11. **Checkpoint:** All artifacts exist and are consistent

### Workflow 2: Execution Contract

**Objective:** Validate that implementation can start safely.

1. Load Artifact Map (Workflow 1)
2. **Inter-ADR Validation (`depends_on`):** Verify if all ADRs listed in `depends_on` have their respective consolidated ER.md in `docs/adr/` or `docs/adr/archive/`. If any dependency is pending, **STOP** and report blockage.
3. Validate if ADR, BP, and TODO exist and are consistent.
4. If artifacts or templates are missing or outdated, **pause validation and initiate Auto-Repair:**
   - Invoke the `adr-generator` skill to apply retroactive governance (Retroactive Governance).
5. Verify if PI exists (Optional, but changes the workflow to Zen-Mode or Legacy).
6. Validate if PI (if exists) contains TDD steps or if TODO (if Legacy) contains tasks.
7. Validate branch (not main/master without PR)
8. Validate workspace clean (no uncommitted changes)
9. Validate affected files exist
10. Extract acceptance criteria from TODO and PI
11. Extract rollback criteria from Blueprint
12. Generate `execution-contract.md` filled
13. **Checkpoint:** Contract signed (all fields valid and dependencies satisfied)

### Workflow 3: Dependency Analysis & Execution Plan

**Objective:** Build DAG and execution plan.

1. Read PI and extract all micro-tasks
2. Read dependencies of each task in the PI
3. Construct directed acyclic graph (DAG)
4. Detect cycles (if any, report error and interrupt)
5. Topological sort for execution order
6. Identify parallelizable tasks (no dependency between them)
7. Generate `change-plan.md` with DAG and order
8. Estimate total time from TODO estimates
9. **Checkpoint:** Valid DAG, no cycles, order defined

### Workflow 4: Incremental Execution

**Objective:** Execute tasks one by one with validation.

For each task in the DAG order (derived from PI or TODO, if Legacy):

1. Verify that all dependencies are "Completed"
2. Mark task as "In progress" (in PI and TODO simultaneously if Zen-Mode, or only in TODO if Legacy)
3. Generate `task-progress.md` for the task
4. Read exact steps (TDD in PI) or infer implementation (TODO in Legacy)
5. Execute changes in the code exactly as prescribed or inferred
6. Execute continuous validation (Workflow 5)
7. **Scope Isolation:** If during execution peripheral refactoring or files outside the scope are detected:
   - Register the incidental debt via CLI:
     `python3 ~/.gemini/config/skills/adr-archive/scripts/audit.py . --register-debt --severity MEDIUM --domain <DOMAIN> --desc "<DESCRIPTION>" --origin "implementation:ADR-XXX"`
   - **DO NOT** alter peripheral code in the current task.
8. If validation passes:
   - Update affected documentation
   - Mark task as "Completed" in PI and update TODO
   - Update `task-progress.md`
9. If validation fails:
   - Analyze root cause
   - Correct
   - Re-execute validation
   - If not corrected in 3 attempts: mark "Blocked"
10. Re-evaluate dependencies (next tasks can start)
11. **Checkpoint:** Task completed, TODO updated

### Workflow 5: Continuous Validation

**Objective:** Validate project state after each change.

**Validation sequence (when applicable):**

1. **Build**: `npm run build` / `cargo build` / equivalent
2. **Lint**: `npm run lint` / `cargo clippy` / equivalent
3. **Typecheck**: `npm run typecheck` / `cargo check` / equivalent
4. **Unit tests**: `npm run test` / `cargo test` / equivalent
5. **Integration tests**: if present
6. **Architectural validation**: verify consistency with ADR
7. **Document validation**: verify that docs are updated

**Rule:** If any step fails, the task cannot be marked as "Completed".

### Workflow 6: Documentation Synchronization

**Objective:** Ensure documentation is synchronized with code.

After each completed task:

1. Verify if the change impacts existing ADRs
2. If so, update the ADR with new information
3. Verify if the Blueprint needs adjustments
4. If so, update the Blueprint
5. Verify if README needs updating
6. If so, update README
7. Verify if new debts were discharged in the registry via `--register-debt`
8. Verify if `related_skills` of other skills need adjustments
9. **Checkpoint:** No divergent documentation from code

### Workflow 7: Progress Tracking

**Objective:** Maintain TODO synchronized throughout implementation.

**Allowed states:**

| State          | Description                     | Transitions               |
| --------------- | ----------------------------- | ------------------------ |
| ⬜ Pending     | Task not initiated           | → In progress           |
| 🔄 In progress | Task in execution            | → Completed, Blocked   |
| ✅ Completed   | Task finalized with success | —                        |
| ❌ Blocked     | Task impeded                 | → In progress, Pending |
| ⏸️ Paused      | Task voluntarily delayed    | → Pending               |

**Rules:**

- Maximum 1 task "In progress" at a time
- "Completed" only after successful validation
- "Blocked" requires justification
- State must be updated in TODO immediately

### Workflow 8: Final Audit & Handoff (GATEKEEPER RESTRICTED)

**Objective:** Invoke the auditor to close the cycle and generate the Execution Report algorithmically.

<HARD-GATE>
**ABSOLUTE PROHIBITION ON GENERATING `ER.md` FILES MANUALLY.**
You (agent) are **STRICLY PROHIBITED** from creating, editing, or mocking any files that end in `*-ER.md`. The generation of the complete, consistent, and structured Evidence Record is the **EXCLUSIVE** responsibility of the algorithmic gatekeeper (`audit.py` / `adr-archive`).
</HARD-GATE>

**Final Step (Mandatory):**

1. You must **physically touch** the `TODO.md` (or `*-PI.md`) file and mark completed tasks with `- [x]` or `✅`.
2. After finalizing all markings, **DO NOT** create the ER manually. Instead, execute the archival and generation algorithmically:
   ```bash
   python3 ~/.gemini/config/skills/adr-archive/scripts/audit.py . --archive ADR-XXX
   ```
   *The script will verify tasks, auto-generate the `ADR-XXX-ER.md` with all evidence, metrics, and tables in the root, and move the Triad of work to `docs/adr/archive/`.*

3. Read the terminal output and the generated report in `docs/reports/`. Present the final verdict and the consolidated Decision Set to the user.

## Anti-patterns

### 🔴 Critical

#### Drive-by Refactoring / Scope Violation

**What is it:** Performing changes and refactoring in peripheral files or modules not predicted in the ADR/TODO/PI contract.
**Why is it bad:** Causes hidden regressions, invalidates the execution DAG, hinders code review, and breaks SDLC traceability.
**How to avoid:** Apply the rule of *Tech Debt Offloading*: register the incidental debt via `audit.py . --register-debt` and continue focusing on the scope of the active ADR.

#### Execute without Validating Inter-ADR Dependencies

**What is it:** Starting the implementation of an ADR whose `depends_on` field lists ADRs not yet consolidated.
**Why is it bad:** Implements on non-existent or incomplete premises.
**How to avoid:** Respect the gate of Workflow 2 — all ADRs in `depends_on` must have a consolidated ER.md.

#### Mocking the Evidence Record (ER.md) Manually

**What is it:** The agent trying to write or edit files ending in `*-ER.md`.
**Why is it bad:** Violates the algorithmic gatekeeper and produces inconsistent certificates without machine validation.
**How to avoid:** Always delegate ER generation to `audit.py --archive ADR-XXX` or `audit.py --generate-er ADR-XXX`.

## Checklists

### Pre-execution Checklist

Location: `checklists/pre-execution.md`

Execute before starting any implementation. Validates artifacts, consistency, environment, inter-ADR dependencies, criteria, and dependencies.

### Post-execution Checklist

Location: `checklists/post-execution.md`

Execute after completing all implementation. Validates tasks, build, quality, tests, documentation, registry, git, risks, and handoff to `audit.py`.

## References

- [Skill adr-generator](../adr-generator/SKILL.md)
- [Skill adr-archive](../adr-archive/SKILL.md)
- [Skill agent-planning-execution](../agent-planning-execution/SKILL.md)
- [Skill technical-documentation](../technical-documentation/SKILL.md)
- [Skill testing-mastery](../testing-mastery/SKILL.md)
- [Skill git-workflow](../git-workflow/SKILL.md)

## Edge Cases & Failure Modes

- **Restricted / Read-Only Environment:** If the filesystem or sandbox is write-locked, report the constraint immediately with evidence and generate changes as a markdown diff patch.
- **Specification Conflict:** If contradictions emerge between user intent and the SSOT (`AGENTS.md`), halt and present trade-off options.
- **Context Exhaustion / Timeout:** For massive tasks, decompose into atomic sub-batches utilizing `subagent-driven-development`.



## Domain SOTA & Industry Engineering Standards

- **Execution Governance:** Agent Skills SDLC lifecycle, Atomic Change Transactions, and Continuous Verification.
- **State Preservation:** Step-by-step state hydration with rollback checkpoints.
- **Governance Handoff:** Direct integration with `adr-generator` Decision Sets and `adr-archive` Evidence Records.
- **Zero Drift Principle:** Strict compliance with approved Implementation Plans (`*-PI.md`) and Task Backlogs (`*-TODO.md`).

### Atomic Change Transaction Invariant:
Every code modification must follow the ACID-like cycle:

$$\text{Snapshot State} \longrightarrow \text{Apply Edit} \longrightarrow \text{Run Tests} \longrightarrow \begin{cases} \text{Commit (if Pass)} \\ \text{Rollback (if Fail)} \end{cases}$$

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
## Operational Verification Checklist

- [ ] All prerequisites and target files inspected before modification.
- [ ] Procedure strictly adheres to specialization rules and best practices.
- [ ] Security, typing, and architectural style guidelines preserved.
- [ ] Unit tests or validation commands executed successfully.
- [ ] Final deliverable verified against the completion gate.



## Completion Gate

The task associated with the skill `implementation` can only be declared complete when:
1. All checks in the operational verification checklist have been satisfied.
2. The deliverable has been deterministically validated through execution evidence.
3. No structural debt, unresolved placeholders, or unhandled errors remain.

