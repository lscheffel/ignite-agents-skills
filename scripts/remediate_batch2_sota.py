#!/usr/bin/env python3
"""
scripts/remediate_batch2_sota.py — Comprehensive Batch 2 Domain SOTA Elevation (ADR-031)
Injects mathematical loop models, circuit breaker FSM equations, subagent DAG topologies,
and JSON-RPC 2.0 MCP standards into the 9 AI Agents & Loops skills.
"""

from pathlib import Path

BATCH_2_DATA = {
    "agent-development": """
## Domain SOTA & Industry Engineering Standards

- **Agent Architecture Frameworks:** ReAct (Yao et al.), Plan-and-Solve (Wang et al.), Reflexion (Shinn et al.), and Toolformer (Schick et al.).
- **Protocol & Transport Standards:** Model Context Protocol (MCP 2024-11-05 standard) and JSON-RPC 2.0.
- **Safety & Guardrails:** OWASP Top 10 for LLM Applications (Prompt Injection, Insecure Output Handling, Excessive Agency).
- **Idempotency & Resilience:** Deterministic tool call contracts (RFC 7231) with guaranteed state recovery.

### Mathematical ReAct Loop Convergence Model:
To prevent non-terminating loops and context exhaustion, the agent loop enforces strict convergence bounds:

$$N_{\\text{turns}} \\le N_{\\text{max}} = \\min(25, \\lfloor \\frac{C_{\\text{window}} - C_{\\text{prompt}}}{C_{\\text{turn\\_avg}}} \\rfloor)$$

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Bounded Exploration Invariant):** If an agent loop executes $>3$ consecutive tool calls without producing a new observation or reducing task uncertainty, the loop MUST trip a soft circuit breaker.
2. **Rule of Thumb 2 (Strict Tool Schema Contract):** Every tool definition must provide type annotations, descriptions, and mutually exclusive parameter validations.
3. **Rule of Thumb 3 (Stateful Memory Compaction):** When context reaches $70\\%$ of context window capacity, trigger memory compaction summarizing previous turns into structured key-value state.
4. **Rule of Thumb 4 (Deterministic Exit Gate):** The agent loop MUST terminate only when acceptance criteria are verified with automated test execution.
""",

    "agent-orchestration": """
## Domain SOTA & Industry Engineering Standards

- **Multi-Agent Orchestration Patterns:** Directed Acyclic Graph (DAG) Workflow Execution, Hierarchical Supervisor-Worker, and Peer-to-Peer Consensus.
- **Data Exchange Contracts:** Immutable JSON Schema payloads and CloudEvents (v1.0.2) message encapsulation.
- **Deadlock & Cycle Prevention:** Tarjan's Strongly Connected Components algorithm for runtime DAG dependency verification.
- **Fault Isolation:** Bulkhead Pattern and Circuit Breaker isolation per agent worker node.

### Multi-Agent DAG Execution Algebra:
The orchestration graph $G = (V, E)$ must be strictly acyclic:

$$\\text{Cycle}(G) = \\emptyset \\quad \\text{and} \\quad \\text{InDegree}(v_{\\text{sink}}) \\ge 1$$

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Zero Shared Mutable State):** Agents must never share mutable memory; all state handoffs occur via explicit, validated message envelopes.
2. **Rule of Thumb 2 (Worker Timeout Bound):** Every delegated worker task must specify a strict wall-clock timeout ($T_{\\text{worker}} \\le 120\\text{s}$) with automated fallback.
3. **Rule of Thumb 3 (Fan-In Synthesis Gate):** An aggregator agent must validate the completeness of all parent nodes before emitting the final consolidated response.
4. **Rule of Thumb 4 (Role Containment Invariant):** Specialized subagents are prohibited from executing tasks outside their defined system prompt boundary.
""",

    "agent-planning-execution": """
## Domain SOTA & Industry Engineering Standards

- **Planning Paradigms:** Hierarchical Task Network (HTN) Planning, Least-to-Most Prompting, and Tree of Thoughts (ToT).
- **Execution Tracking:** Milestone-driven State Machine with explicit rollback vectors.
- **Software Quality Gates:** Test-Driven Development (TDD) cycle integration within execution loops.
- **Artifact Governance:** Bidirectional cross-linking between Implementation Plans (`*-PI.md`), Task Backlogs (`*-TODO.md`), and Evidence Records (`*-ER.md`).

### Task Decomposition & Dependency Graph Formula:
The complexity of plan decomposition is bounded by the Critical Path Length ($L_{\\text{crit}}$):

$$L_{\\text{crit}} = \\max_{p \\in \\text{Paths}} \\sum_{t \\in p} \\text{Duration}(t)$$

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Atomicity Rule):** No single plan step should touch $>3$ files or exceed 50 lines of code changes without intermediate test verification.
2. **Rule of Thumb 2 (Fail-Fast Checkpoints):** If a validation step fails, halt forward execution immediately; never proceed to downstream dependent tasks.
3. **Rule of Thumb 3 (Explicit Pre/Post-Conditions):** Every task in the roadmap must define deterministic entry prerequisites and verifiable exit deliverables.
4. **Rule of Thumb 4 (Dynamic Plan Adaptation):** When runtime surprises occur, update the written plan artifact first before modifying additional code.
""",

    "subagent-driven-development": """
## Domain SOTA & Industry Engineering Standards

- **Subagent Isolation Standards:** Sandboxed execution environments with bounded filesystem access and isolated git workspaces.
- **Context Hygiene:** Ephemeral subagent context lifecycles (spawn $\\to$ execute single task $\\to$ synthesize $\\to$ destroy).
- **Contract Enforcement:** JSON Schema validation on subagent structured return values.
- **Observability & Tracing:** OpenTelemetry-compatible span tracking across parent and child agent executions.

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Single Responsibility Subagent):** A subagent must be assigned exactly ONE discrete unit of work (e.g., "implement function X with tests").
2. **Rule of Thumb 2 (Parent Synthesizer Rule):** The parent agent must verify subagent test results before accepting any code modifications.
3. **Rule of Thumb 3 (Subagent Context Pruning):** Never pass the full conversation transcript to a subagent; inject only the minimal necessary context (CAP).
4. **Rule of Thumb 4 (Failure Escalation):** If a subagent fails its task twice, terminate the subagent and escalate to human review or alternate strategy.
""",

    "dispatching-parallel-agents": """
## Domain SOTA & Industry Engineering Standards

- **Concurrency & Parallelism Models:** Actor Model, Fork-Join Parallelism, and Work-Stealing Pool architectures.
- **Resource Budgeting:** Mathematical Token Partitioning across concurrent execution threads.
- **Merge & Conflict Resolution:** Three-way merge algorithms and deterministic AST reconciliation.
- **Rate Limiting & Throttling:** Token Bucket algorithm for API request pacing under concurrent agent load.

### Dynamic Token Budget Partitioning Formula:

$$B_{\\text{subagent}}^{(i)} = \\frac{B_{\\text{total}} - B_{\\text{orchestrator}}}{M} \\times W_i \\quad \\text{where} \\quad \\sum_{i=1}^M W_i = 1.0$$

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (File Partitioning Invariant):** Two parallel subagents MUST NEVER be assigned to modify the same file concurrently (Strict File Ownership Isolation).
2. **Rule of Thumb 2 (Concurrency Limit):** Maximum concurrent active subagents is bounded by $M_{\\text{max}} = 5$ to prevent API throttling and lock contention.
3. **Rule of Thumb 3 (Join Synchronization Gate):** The orchestrator must block on `Promise.all` / `gather` until all dispatched subagents report completion or timeout.
4. **Rule of Thumb 4 (Deterministic Conflict Resolution):** If merge conflicts arise, the orchestrator triggers an isolated resolution agent with AST diff context.
""",

    "circuit-breaker": """
## Domain SOTA & Industry Engineering Standards

- **Resilience Design Pattern:** Michael Nygard's Circuit Breaker (Release It!) and Martin Fowler's Fault Tolerance models.
- **Finite State Machine (FSM):** 3-State deterministic transitions (Closed $\\leftrightarrow$ Open $\\leftrightarrow$ Half-Open).
- **Backoff Algebra:** Full Jitter Exponential Backoff (AWS Architecture Guidelines / Decoupled Systems).
- **Health Telemetry:** Rolling window failure rate monitoring with Prometheus-compatible error counters.

### Circuit Breaker State Transition Matrix:

| Current State | Event | Next State | Action / Side Effect |
|:---|:---|:---|:---|
| **CLOSED** | Consecutive Failures $\\ge 5$ | **OPEN** | Trip breaker, reject calls immediately with fast-fail. |
| **OPEN** | Cooldown Period ($T_{\\text{cool}} \\ge 60\\text{s}$) Elapsed | **HALF-OPEN** | Allow probe request ($N_{\\text{probe}} = 1$) to test backend. |
| **HALF-OPEN** | Probe Request Succeeded | **CLOSED** | Reset failure counter to 0, restore normal traffic. |
| **HALF-OPEN** | Probe Request Failed | **OPEN** | Reset cooldown timer with doubled backoff ceiling. |

### Exponential Backoff with Full Jitter Equation:

$$T_{\\text{sleep}} = \\text{Uniform}(0, \\min(T_{\\text{max}}, T_{\\text{base}} \\times 2^k))$$

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Fast-Fail Rule):** When in OPEN state, reject downstream calls instantly without attempting network I/O.
2. **Rule of Thumb 2 (Error Classification):** 4xx client errors (e.g. 400 Bad Request) must NOT trip the circuit breaker; only 5xx, timeouts, and network exceptions trip the breaker.
3. **Rule of Thumb 3 (Half-Open Safety):** During HALF-OPEN state, strictly limit concurrency to 1 probe request.
4. **Rule of Thumb 4 (Fallback Mandate):** Every breaker-protected invocation must provide a deterministic degraded fallback response.
""",

    "resilient-execution": """
## Domain SOTA & Industry Engineering Standards

- **Fault Tolerance Patterns:** Graceful Degradation, Bulkhead Isolation, Retry with Budgeting, and Self-Healing Systems.
- **Idempotency Standards:** RFC 7231 safe methods and cryptographic idempotency key generation.
- **Disaster Recovery:** Automated Rollback Vectors and State Checkpoint Hydration.
- **Chaos Engineering:** Antifragile validation under synthetic failure injection.

### Degradation Ladder (4 Tiers):
1. **Tier 1 (Optimal):** Full live execution with external model inference and active tooling.
2. **Tier 2 (Cached/RAG Fallback):** Local SQLite RAG semantic search when external LLM endpoints are degraded.
3. **Tier 3 (Rule-Based Static Fallback):** Deterministic heuristic rules when semantic models are unavailable.
4. **Tier 4 (Safe Refusal):** Fast-fail with structured error diagnostic when data corruption risk is detected.

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Idempotent Retry Mandate):** Retries are strictly forbidden on non-idempotent operations without transaction rollback capabilities.
2. **Rule of Thumb 2 (Max Retry Limit):** Maximum retry attempts is capped at $K_{\\text{max}} = 3$; subsequent failures escalate down the degradation ladder.
3. **Rule of Thumb 3 (State Checkpointing):** Save execution state before executing any high-risk file modification or external API invocation.
4. **Rule of Thumb 4 (Self-Healing Recovery):** When an unhandled exception occurs, the system must capture the stack trace, rollback disk state, and alert the orchestrator.
""",

    "context7-mcp": """
## Domain SOTA & Industry Engineering Standards

- **Live Documentation Retrieval:** Real-time API resolution, version pinning, and authoritative documentation indexing.
- **Model Context Protocol Integration:** Fast MCP lazy-loading, caching, and token-optimized query dispatch.
- **Semantic Routing:** Two-phase retrieval (1. `resolve-library-id` $\\to$ 2. `query-docs`).
- **Knowledge Freshness:** Strict prioritization of Context7 over model training weights for libraries and SDKs.

### Context7 Operating Protocol:
1. **Phase 1 (Resolve ID):** Call `resolve-library-id` using official library name and question context. Select match matching `/org/project`.
2. **Phase 2 (Query Docs):** Call `query-docs` passing full natural language technical question.
3. **Phase 3 (Doc Ingestion):** Answer strictly based on fetched documentation payload.

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Never Guess Modern APIs):** For popular evolving frameworks (Next.js, React 19, Tailwind, Prisma), Context7 lookup is MANDATORY before writing code.
2. **Rule of Thumb 2 (Full Question Rule):** Always pass the complete user technical question to `query-docs`, never isolated single keywords.
3. **Rule of Thumb 3 (Version Specificity):** When a specific version is mentioned by the user (e.g. "Vite 6"), select the version-tagged library ID.
4. **Rule of Thumb 4 (Fallback to Web Search):** If Context7 returns empty results after 2 attempts, fall back to official web search with domain whitelisting.
""",

    "mcp-builder": """
## Domain SOTA & Industry Engineering Standards

- **Protocol Specification:** Model Context Protocol (MCP 2024-11-05 Specification) and JSON-RPC 2.0.
- **Transport Architectures:** Stdio Stream Transport (POSIX stdin/stdout) and Server-Sent Events (SSE) with HTTP POST.
- **Schema & Validation:** JSON Schema Draft-07 for tool parameters and resource URI templates.
- **Security & Authorization:** Tool execution sandboxing, input sanitization, and path traversal prevention.

### Stdio JSON-RPC 2.0 Transport Protocol Architecture:

```text
Client (Antigravity/Kilo)                       MCP Server (Stdio)
       │                                                │
       │─── JSON-RPC 2.0 Request ("tools/list") ───────>│
       │<── JSON-RPC 2.0 Result (Tool Definitions) ─────│
       │                                                │
       │─── JSON-RPC 2.0 Request ("tools/call") ───────>│
       │<── JSON-RPC 2.0 Result (Execution Payload) ────│
```

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Stdio Cleanliness Invariant):** An MCP Stdio server MUST NEVER print debug strings or raw text to `stdout`; all logging must use `stderr` to prevent JSON-RPC parsing crashes.
2. **Rule of Thumb 2 (Strict Tool Typing):** Every tool schema must specify `type: "object"`, `properties`, and `required` arrays.
3. **Rule of Thumb 3 (Backpressure & Timeout):** Async tool handlers must complete within 30 seconds or return a structured JSON-RPC timeout error.
4. **Rule of Thumb 4 (Atomic Tool Returns):** Return values must follow the canonical `{ content: [{ type: "text", text: "..." }], isError: false }` format.
"""
}

def main():
    root = Path(__file__).resolve().parent.parent
    skills_dir = root / "skills"
    
    for skill_name, sota_text in BATCH_2_DATA.items():
        skill_file = skills_dir / skill_name / "SKILL.md"
        if not skill_file.exists():
            print(f"[!] Skill file not found: {skill_file}")
            continue
            
        content = skill_file.read_text(encoding="utf-8")
        if "## Domain SOTA & Industry Engineering Standards" in content:
            print(f"[*] Already has SOTA standards: {skill_name}")
            continue
            
        # Clean frontmatter if needed
        if "description: 'Use when the user needs to build AI agents" in content:
            content = content.replace("description: 'Use when the user needs to build AI agents — tool use patterns, memory\nrelated_skills:\n  - cap\n  - implementation\n  - technical-documentation\n  management, planning strategies, multi-agent coordination, evaluation, and safety\n  guardrails. Triggers: user says \"agent\", \"build an agent\", \"tool use\", \"agent loop\",\n  \"multi-agent\", \"memory management\", \"guardrails\", \"agent evaluation\".'",
                                      "description: 'Use when building AI agents — tool use patterns, memory management, planning strategies, multi-agent coordination, evaluation, and safety guardrails.'\nrelated_skills:\n  - cap\n  - implementation\n  - technical-documentation")
            
        if "## Operational Verification Checklist" in content:
            parts = content.split("## Operational Verification Checklist", 1)
            new_content = parts[0] + sota_text.strip() + "\n\n## Operational Verification Checklist" + parts[1]
        else:
            new_content = content + "\n\n" + sota_text.strip()
            
        skill_file.write_text(new_content, encoding="utf-8")
        print(f"[✓] Elevated Domain SOTA for: {skill_name}")

if __name__ == "__main__":
    main()
