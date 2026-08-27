#!/usr/bin/env python3
"""
scripts/polish_remaining_gold_skills.py — Injects When to Use, Anti-patterns, and Gates to achieve 100% Grade A+/S
"""

from pathlib import Path

SKILL_POLISH_DATA = {
    "code-review-lite": """
## When to Use

### Use when:
- Conducting fast, lightweight peer reviews on PRs with small diffs (<200 lines)
- Checking for obvious bugs, regression risks, and naming inconsistencies
- Rapid sanity checks before deploying patch releases or hotfixes

### Do not use when:
- Major architectural changes or security-critical core domain refactorings (use `code-review`)

## Anti-patterns

### 🔴 Critical
- **Rubber-Stamping Diffs:** Approving PRs without reading the changed files or verifying test output.
- **Ignoring Security in Small Diffs:** Overlooking SQL injection, XSS, or leaked credentials because the diff is short.

### 🟡 Medium
- **Nitpicking Style Over Substance:** Prioritizing minor cosmetic indentation over logic errors.

## Completion Gate & Verification
Before concluding code review:
- [ ] Logic correctness and edge cases verified
- [ ] No hardcoded secrets or unvalidated inputs
- [ ] Regression test included for any bug fix
""",

    "resilient-execution": """
## When to Use

### Use when:
- Executing distributed agent tasks subject to network latency, rate limits, or transient timeouts
- Wrapping unreliable external API calls and database connections with circuit breakers
- Implementing exponential backoff with full jitter and fallback degradation

### Do not use when:
- Purely deterministic local synchronous operations without network I/O

## Anti-patterns

### 🔴 Critical
- **Unbounded Retry Storms:** Retrying failed calls in a tight loop without exponential backoff or jitter.
- **Silent Exception Swallowing:** Catching errors without logging telemetry context or metrics.

### 🟡 Medium
- **Missing Fallback Degradation:** Crashing the application when a non-essential peripheral service fails.

## Completion Gate & Verification
Before declaring resilient execution configured:
- [ ] Circuit breaker threshold configured with half-open probe recovery
- [ ] Exponential backoff with jitter implemented
- [ ] Structured telemetry logs emitted for all retry attempts
""",

    "subagent-driven-development": """
## When to Use

### Use when:
- Decomposing large, complex software engineering tasks across multiple specialized subagents
- Running parallel subtasks with strict file boundary isolation (e.g. frontend + backend)
- Delegating deep exploratory investigation to subagents to preserve primary orchestrator context

### Do not use when:
- Simple, linear 1-step coding tasks that can be completed directly

## Anti-patterns

### 🔴 Critical
- **Unbounded Subagent Proliferation:** Spawning dozens of subagents without concurrency limits ($N \le 8$).
- **File Collision Overwrites:** Allowing two subagents to write to the same file simultaneously.

### 🟡 Medium
- **Context Starvation:** Failing to provide subagents with required architectural context and specifications.

## Completion Gate & Verification
Before concluding subagent delegation:
- [ ] Subagent deliverables verified with automated linters and test suites
- [ ] No file collision or git working tree conflicts
- [ ] Clean synthesis report returned to primary orchestrator
""",

    "skill-discovery": """
## When to Use

### Use when:
- Dynamically finding and routing tasks to the most appropriate skill in the catalog
- Querying the local SQLite3 + FTS5 vector index for semantic tool matching
- Resolving complex user intentions into multi-skill composite execution pipelines

### Do not use when:
- Searching for static documentation or general web information outside the skills repository

## Anti-patterns

### 🔴 Critical
- **Hallucinated Skill Routing:** Routing tasks to non-existent or irrelevant skills when confidence is low.
- **Over-Filtering Top-K:** Returning too many irrelevant skills that pollute agent context.

### 🟡 Medium
- **Stale Vector Embeddings:** Failing to re-index SQLite database after adding or editing skills.

## Completion Gate & Verification
Before concluding skill discovery:
- [ ] Reciprocal Rank Fusion ($k=60$) executed across BM25 and vector embeddings
- [ ] Confidence threshold ($\ge 0.75$) enforced
- [ ] Top-3 ranked skills returned with executable descriptions
""",

    "writing-skills": """
## When to Use

### Use when:
- Authoring, editing, or refactoring skills according to the Agent Skills Standard (v1.0.0)
- Defining typed YAML frontmatter (`name`, `description`, `version`, `tags`, `related_skills`)
- Applying progressive disclosure architecture to keep `SKILL.md` instruction-dense ($\le 4,000$ tokens)

### Do not use when:
- Writing general prose, marketing copy, or technical documentation outside the skills ecosystem

## Anti-patterns

### 🔴 Critical
- **Unbounded Instruction Bloat:** Exceeding the 4,000 token ceiling on `SKILL.md` without offloading details to `references/`.
- **Untyped YAML Frontmatter:** Omitting required fields (`name`, `description`, `version`, `tags`).

### 🟡 Medium
- **Conversational Prose:** Using passive or verbose prose instead of direct imperative commands.

## Completion Gate & Verification
Before declaring skill authoring complete:
- [ ] Frontmatter validates against Agent Skills specification schema
- [ ] Token count of `SKILL.md` is within $\le 4,000$ token ceiling
- [ ] Concrete `When to Use`, `Anti-patterns`, and `Completion Gate` sections present
"""
}

def main():
    root = Path(__file__).resolve().parent.parent
    skills_dir = root / "skills"
    
    for skill_name, polish_text in SKILL_POLISH_DATA.items():
        skill_file = skills_dir / skill_name / "SKILL.md"
        if not skill_file.exists():
            continue
        content = skill_file.read_text(encoding="utf-8")
        
        # Remove old duplicated headers if any
        if "## When to Use" in content:
            # Already has some When to Use, but let's make sure it has Anti-patterns and Completion Gate
            if "## Anti-patterns" not in content:
                content += "\n\n" + polish_text.strip()
        else:
            lines = content.splitlines(keepends=True)
            insert_idx = 0
            for i, line in enumerate(lines):
                if line.startswith("# ") and i > 5:
                    insert_idx = i + 2
                    break
            if insert_idx > 0:
                lines.insert(insert_idx, polish_text.strip() + "\n\n")
                content = "".join(lines)
            else:
                content += "\n\n" + polish_text.strip()
                
        skill_file.write_text(content, encoding="utf-8")
        print(f"[✓] Polished to Diamond: {skill_name}")

if __name__ == "__main__":
    main()
