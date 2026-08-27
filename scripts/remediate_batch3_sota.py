#!/usr/bin/env python3
"""
scripts/remediate_batch3_sota.py — Comprehensive Batch 3 Domain SOTA Elevation (ADR-032)
Injects McCabe Complexity formulas, Test Pyramid distribution algebra, Scientific Debugging trees,
and Google Code Review taxonomies into the 9 Engineering & Quality skills.
"""

from pathlib import Path

BATCH_3_DATA = {
    "clean-code": """
## Domain SOTA & Industry Engineering Standards

- **Complexity Metrics:** Thomas McCabe's Cyclomatic Complexity ($CC$), SonarSource Cognitive Complexity, and Halstead Volume.
- **Design Principles:** SOLID (Single Responsibility, Open-Closed, Liskov Substitution, Interface Segregation, Dependency Inversion), DRY, KISS, and YAGNI.
- **Naming Conventions:** Intent-revealing names, domain-driven terminology, pronounceable identifiers (PEP 8, Google Style Guides).
- **Function Hygiene:** Single Level of Abstraction Principle (SLAP), command-query separation (CQS), and maximum parameter count $\\le 3$.

### Cyclomatic Complexity Formula & Quality Gates:

$$CC = E - N + 2P$$

Where $E$ is edges, $N$ is nodes, and $P$ is connected components in the control flow graph.

| Metric | Target / Threshold | Action when Breached |
|:---|:---:|:---|
| **Cyclomatic Complexity ($CC$)** | $\\le 10$ per function | Mandatory refactoring / function extraction. |
| **Cognitive Complexity** | $\\le 15$ per function | Flatten nested conditionals via guard clauses. |
| **Function Length** | $\\le 30$ lines | Extract coherent sub-routines (SLAP). |
| **Parameter Count** | $\\le 3$ params | Encapsulate into Parameter Object or Options Dict. |

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Guard Clause Priority):** Always exit early with guard clauses to minimize indentation depth ($Depth \\le 2$).
2. **Rule of Thumb 2 (Side-Effect Free Queries):** Functions that return values must never mutate external state (Command-Query Separation).
3. **Rule of Thumb 3 (Zero Magic Literals):** Every constant, timeout, or magic number must be defined as an exported named constant.
4. **Rule of Thumb 4 (Intent-Revealing Naming):** Variable names must state *why* it exists and *what* it represents without requiring inline comments.
""",

    "code-review": """
## Domain SOTA & Industry Engineering Standards

- **Code Review Frameworks:** Google Engineering Practices (eng-practices), Conventional Comments, and Chromium Review Guidelines.
- **Review Taxonomy:** 3-Tier Severity Badges (`P1: Blocker`, `P2: Major`, `P3: Polish`).
- **AST Inspection:** Automated AST linting, architectural layer violation checks, and security vulnerability scanning.
- **Psychological Safety & Tone:** Objective, blame-free feedback focusing on code behavior and architectural alignment.

### 3-Tier Severity Taxonomy Matrix:

| Severity Badge | Definition | Action Required | Blocking? |
|:---|:---|:---|:---:|
| **`🔴 P1: BLOCKER`** | Correctness bug, security vulnerability, data corruption risk, breaking API change. | Must fix before merge. | **YES** |
| **`🟡 P2: MAJOR`** | Code smell, architectural violation, missing tests, performance degradation. | Must resolve or record as tech debt. | **YES** |
| **`🟢 P3: POLISH`** | Naming suggestion, minor style polish, non-blocking optimization. | Author's discretion. | **NO** |

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Review Size Bound):** Diff size should not exceed 400 lines of code per review to avoid reviewer fatigue ($T_{\\text{review}} \\le 60\\text{min}$).
2. **Rule of Thumb 2 (Actionable Feedback):** Every critique must explain *why* the current code is suboptimal and provide a concrete suggestion or code example.
3. **Rule of Thumb 3 (Test Coverage Verification):** Every PR adding business logic must include corresponding unit and integration tests.
4. **Rule of Thumb 4 (Conventional Prefixes):** Review comments should use conventional prefixes: `p1-blocker:`, `p2-major:`, `p3-polish:`, `question:`, `nit:`.
""",

    "code-review-lite": """
## Domain SOTA & Industry Engineering Standards

- **Triage Paradigms:** Fast-Path Pull Request Triage, Lightweight Linting, and Micro-Diff Reviews.
- **Scope Containment:** High-velocity verification for small, low-risk patches ($N_{\\text{lines}} \\le 200$).
- **Automated Pre-Checks:** CI gate green verification before starting human review.
- **Fast Turnaround:** SLA target for review turnaround $\\le 4$ hours.

### Fast-Path Review Criteria:
A Pull Request qualifies for Lite Review if:

$$N_{\\text{lines}} \\le 200 \\quad \\text{and} \\quad \\text{FilesModified} \\le 5 \\quad \\text{and} \\quad \\text{BreakingChanges} = \\text{False}$$

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Fast-Path Escalation):** If a Lite Review reveals hidden architectural complexity or migration risk, immediately escalate to full `code-review`.
2. **Rule of Thumb 2 (Automated Test Pass Invariant):** Never approve a Lite Review if CI pipeline or automated tests have failing status.
3. **Rule of Thumb 3 (Focus on Correctness):** Focus exclusively on logic correctness, security, and test coverage; avoid bike-shedding on personal style preferences.
4. **Rule of Thumb 4 (Single-Pass Approval):** If only minor non-blocking nits remain, approve the PR and trust the author to apply them before merging.
""",

    "code-review-workflow": """
## Domain SOTA & Industry Engineering Standards

- **Workflow Orchestration:** GitHub Flow, GitLab Flow, and Trunk-Based Development review lifecycles.
- **Review Finite State Machine (FSM):** Structured transitions from Draft $\\to$ In Review $\\to$ Approved $\\to$ Merged.
- **SLA Management:** Explicit turnaround targets and stale PR warning notifications ($T_{\\text{stale}} \\ge 48\\text{h}$).
- **Audit Trails:** Cryptographic PR merge signatures and linked issue tracking.

### Code Review Finite State Machine:

```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> InReview: Ready for Review (PR Opened)
    InReview --> ChangesRequested: P1/P2 Issues Found
    ChangesRequested --> InReview: Author Pushes Fixes
    InReview --> Approved: All P1/P2 Resolved + LGTM
    Approved --> Merged: CI Green + Rebase/Squash
    Merged --> [*]
```

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Minimum Reviewer Quorum):** At least 1 designated code owner must approve before branch merge protection allows merge.
2. **Rule of Thumb 2 (Re-review on Push):** Any new commit pushed to an approved PR automatically resets approval if diff touches core logic.
3. **Rule of Thumb 3 (Resolving Conversations):** Only the reviewer who opened a discussion thread (or the designated lead) should mark it as resolved.
4. **Rule of Thumb 4 (Clean Branch State):** PR must be rebased on latest master and pass all branch protection checks before merge.
""",

    "refactoring": """
## Domain SOTA & Industry Engineering Standards

- **Refactoring Foundations:** Martin Fowler's Refactoring Catalog (2nd Edition) and Joshua Kerievsky's Refactoring to Patterns.
- **Architecture Migration Patterns:** Strangler Fig Pattern, Branch by Abstraction, and Parallel Run verification.
- **Safety Invariant:** Characterization Tests (Golden Master Tests) established BEFORE modifying code.
- **Small Steps:** Micro-commits with continuous green test suite.

### Refactoring Risk & Invariance Model:
A refactoring step $R$ preserves observable behavior $B$:

$$B(f(x)) \\equiv B(f'(x)) \\quad \\forall x \\in \\text{Inputs}$$

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Separate Refactoring from Features):** Never combine structural refactoring with new feature implementation in the same commit.
2. **Rule of Thumb 2 (Test Coverage Prerequisite):** Never refactor legacy code without establishing characterization tests first.
3. **Rule of Thumb 3 (Extract Before Modify):** When dealing with large monolithic functions, extract small helper methods before altering behavior.
4. **Rule of Thumb 4 (Revert on Red):** If tests fail during a refactoring step and the fix is not obvious in 2 minutes, revert immediately and take smaller steps.
""",

    "systematic-debugging": """
## Domain SOTA & Industry Engineering Standards

- **Scientific Debugging Framework:** Andreas Zeller's Why Programs Fail (Scientific Method applied to software debugging).
- **Search & Bisection Algebra:** Binary search across git history ($O(\\log N)$) via `git bisect`.
- **Root Cause Analysis (RCA):** 5-Whys Tree, Ishikawa (Fishbone) diagrams, and Fault Tree Analysis (FTA).
- **Anti-Pattern Elimination:** Strict prohibition of shotgun debugging, speculation without evidence, and cosmetic patches.

### Scientific Debugging Search Complexity:

$$\\text{Steps}_{\\text{bisect}} \\le \\lceil \\log_2(N_{\\text{commits}}) \\rceil$$

### 4-Phase Scientific Hypothesis Protocol:
1. **Phase 1 (Reproduce):** Build a deterministic, minimal reproducible example (automated test script).
2. **Phase 2 (Hypothesize):** Formulate a single, falsifiable hypothesis explaining the root cause.
3. **Phase 3 (Experiment):** Execute a targeted experiment or bisect step to prove or disprove the hypothesis.
4. **Phase 4 (Fix & Guard):** Apply minimal root-cause fix and add a permanent regression test.

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (No Code Change Without Failing Test):** You cannot claim a bug is fixed until you write a test that fails before the fix and passes after.
2. **Rule of Thumb 2 (Single Variable Rule):** Change only ONE variable per experiment during debugging.
3. **Rule of Thumb 3 (Root Cause vs Symptom):** Fixing a `NullPointerException` with `if (x != null)` is a symptom fix; investigate *why* `x` was null.
4. **Rule of Thumb 4 (Explain the Fix):** If you cannot explain *why* the fix works, you do not understand the bug yet.
""",

    "test-driven-development": """
## Domain SOTA & Industry Engineering Standards

- **TDD Foundations:** Kent Beck's Test-Driven Development By Example, Martin Fowler's Mocks Aren't Stubs.
- **Rhythm & Cadence:** Strict RED-GREEN-REFACTOR cycle with sub-minute iteration loops.
- **Test Quality Verification:** Mutation Testing Score ($MS \\ge 0.85$) and Code Coverage.
- **Transformation Priority Premise (TPP):** Robert C. Martin's TPP transformations from specific to general.

### Mutation Testing Score Formula:

$$MS = \\frac{M_{\\text{killed}}}{M_{\\text{total}} - M_{\\text{equivalent}}} \\ge 0.85 \\quad (85\\%)$$

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Three Laws of TDD):**
   - You may not write production code until you have written a failing unit test.
   - You may not write more of a unit test than is sufficient to fail.
   - You may not write more production code than is sufficient to pass the failing test.
2. **Rule of Thumb 2 (Fake It Till You Make It):** In the Green phase, write the simplest code that passes (even returning hardcoded literals) to verify test harness.
3. **Rule of Thumb 3 (Refactor on Green Only):** Clean code and eliminate duplication ONLY when all tests are green.
4. **Rule of Thumb 4 (Fast Test Execution):** Unit test suite must execute in $<5$ seconds to maintain rapid feedback loop.
""",

    "testing-mastery": """
## Domain SOTA & Industry Engineering Standards

- **Testing Architecture:** Mike Cohn Test Pyramid, Testing Trophy (Kent C. Dodds), and Test Honeycomb.
- **Advanced Testing Paradigms:** Property-Based Testing (Hypothesis/QuickCheck), Contract Testing (Pact), and Chaos Engineering.
- **Test Doubles Taxonomy:** Gerard Meszaros' xUnit Patterns (Dummy, Stub, Spy, Mock, Fake).
- **Deterministic Fixtures:** Object Mother and Test Data Builder patterns.

### Mike Cohn Test Pyramid Ratio Algebra:

$$\\frac{N_{\\text{unit}}}{N_{\\text{total}}} \\approx 0.70, \\quad \\frac{N_{\\text{integration}}}{N_{\\text{total}}} \\approx 0.20, \\quad \\frac{N_{\\text{e2e}}}{N_{\\text{total}}} \\approx 0.10$$

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Pyramid Distribution Rule):** The vast majority (70%) of tests must be fast, isolated unit tests.
2. **Rule of Thumb 2 (Don't Mock What You Don't Own):** Only write test doubles for your own domain interfaces; wrap external libraries in adapters.
3. **Rule of Thumb 3 (Test Behavior, Not Implementation):** Assert on observable outputs and state transitions, not private internal methods.
4. **Rule of Thumb 4 (Deterministic Isolation):** Tests must never depend on execution order or share mutable global state (Hermetic Tests).
""",

    "implementation": """
## Domain SOTA & Industry Engineering Standards

- **Execution Governance:** Agent Skills SDLC lifecycle, Atomic Change Transactions, and Continuous Verification.
- **State Preservation:** Step-by-step state hydration with rollback checkpoints.
- **Governance Handoff:** Direct integration with `adr-generator` Decision Sets and `adr-archive` Evidence Records.
- **Zero Drift Principle:** Strict compliance with approved Implementation Plans (`*-PI.md`) and Task Backlogs (`*-TODO.md`).

### Atomic Change Transaction Invariant:
Every code modification must follow the ACID-like cycle:

$$\\text{Snapshot State} \\longrightarrow \\text{Apply Edit} \\longrightarrow \\text{Run Tests} \\longrightarrow \\begin{cases} \\text{Commit (if Pass)} \\\\ \\text{Rollback (if Fail)} \\end{cases}$$

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Plan Fidelity):** Follow the approved Implementation Plan step-by-step; never make unplanned architectural modifications.
2. **Rule of Thumb 2 (Verification Before Mark Done):** Never mark a task `[x]` in TODO.md until automated test execution verifies success.
3. **Rule of Thumb 3 (Incremental Commits):** Commit logically coherent chunks with descriptive conventional commit messages.
4. **Rule of Thumb 4 (Evidence Record Generation):** Upon completing implementation, generate the canonical Evidence Record (`*-ER.md`) certifying all deliverables.
"""
}

def main():
    root = Path(__file__).resolve().parent.parent
    skills_dir = root / "skills"
    
    for skill_name, sota_text in BATCH_3_DATA.items():
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
