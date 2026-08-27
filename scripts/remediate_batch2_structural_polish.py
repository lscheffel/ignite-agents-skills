#!/usr/bin/env python3
"""
scripts/remediate_batch2_structural_polish.py — Polishes structural headings & gates for Batch 2 skills
"""

from pathlib import Path

def polish_skill(skill_path: Path, name: str, when_to_use_block: str, completion_gate_block: str):
    skill_file = skill_path / "SKILL.md"
    content = skill_file.read_text(encoding="utf-8")
    
    if "## When to Use" not in content:
        # Insert after title/overview
        lines = content.splitlines(keepends=True)
        insert_idx = 0
        for i, line in enumerate(lines):
            if line.startswith("# ") and i > 5:
                insert_idx = i + 2
                break
        if insert_idx > 0:
            lines.insert(insert_idx, when_to_use_block + "\n\n")
            content = "".join(lines)
            
    if "## Completion Gate" not in content and "## Verification Gate" not in content:
        content = content + "\n\n" + completion_gate_block
        
    skill_file.write_text(content, encoding="utf-8")
    print(f"[✓] Polished: {name}")

def main():
    root = Path(__file__).resolve().parent.parent
    skills_dir = root / "skills"
    
    # 1. dispatching-parallel-agents
    dpa_wtu = """## When to Use

### Use when:
- 2+ independent tasks have zero shared dependencies and touch disjoint files
- Batch processing multiple distinct issues, features, or modules in parallel
- Running exploratory prototypes concurrently under strict time budgets

### Do not use when:
- Tasks have sequential dependencies where step B depends on output of step A
- Multiple subagents need to modify the exact same files or shared global state
- The system is operating near API rate limits (use sequential ReAct loop instead)"""

    dpa_gate = """## Completion Gate & Verification
Before declaring parallel dispatching complete:
- [ ] All subagent result envelopes received and schema-validated
- [ ] AST diff reconciliation executed with zero syntax errors
- [ ] Consolidated test suite executed with exit code 0"""
    polish_skill(skills_dir / "dispatching-parallel-agents", "dispatching-parallel-agents", dpa_wtu, dpa_gate)

    # 2. mcp-builder
    mcp_wtu = """## When to Use

### Use when:
- Building custom Model Context Protocol (MCP) servers (Stdio or SSE)
- Exposing tools, resources, and prompt templates to AI coding assistants
- Creating integrations between external APIs/databases and agent runtimes

### Do not use when:
- Standard CLI tools or direct scripts are sufficient without agent protocol binding
- Building purely monolithic web applications without MCP client requirements"""

    mcp_gate = """## Completion Gate & Verification
Before declaring MCP server production-ready:
- [ ] Stdio protocol tests pass with zero `stdout` contamination
- [ ] Tool parameters validate against JSON Schema Draft-07
- [ ] Error responses conform to JSON-RPC 2.0 format with `isError: true`"""
    polish_skill(skills_dir / "mcp-builder", "mcp-builder", mcp_wtu, mcp_gate)

    # 3. circuit-breaker
    cb_wtu = """## When to Use

### Use when:
- Protecting LLM API calls and external services against cascading failure
- Preventing runaway retry loops during rate limiting (HTTP 429) or outages (HTTP 5xx)
- Implementing graceful degradation with fallback tiers

### Do not use when:
- Handling expected validation errors (HTTP 400/422) that should fail immediately
- In-memory deterministic functions with no external I/O dependencies"""

    cb_gate = """## Completion Gate & Verification
Before concluding circuit breaker integration:
- [ ] 3-state transitions verified via unit tests (Closed -> Open -> Half-Open -> Closed)
- [ ] Full jitter exponential backoff verified under synthetic failure
- [ ] Structured fallback payload emitted during OPEN state"""
    polish_skill(skills_dir / "circuit-breaker", "circuit-breaker", cb_wtu, cb_gate)

    # 4. context7-mcp
    c7_wtu = """## When to Use

### Use when:
- Fetching authoritative current documentation for libraries, frameworks, SDKs, and APIs
- Investigating recent API changes, migrations, or syntax updates
- Resolving library identifiers in `/org/project` format

### Do not use when:
- Refactoring internal business logic without external library dependencies
- General programming language concepts (syntax basics, loops, math)"""

    c7_gate = """## Completion Gate & Verification
Before concluding Context7 query:
- [ ] Best matching library ID resolved via `resolve-library-id`
- [ ] Query executed passing complete technical question context
- [ ] Final answer strictly grounded in fetched documentation payload"""
    polish_skill(skills_dir / "context7-mcp", "context7-mcp", c7_wtu, c7_gate)

if __name__ == "__main__":
    main()
