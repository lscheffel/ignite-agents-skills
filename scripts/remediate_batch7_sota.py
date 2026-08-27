#!/usr/bin/env python3
"""
scripts/remediate_batch7_sota.py — Comprehensive Batch 7 Domain SOTA Elevation (ADR-036)
Injects Agent Skills Spec v1.0, Reciprocal Rank Fusion (RRF), SLSA Level 3,
and 6-Pillar Documentation Reconciliation into the 10 Meta & Bootstrapping skills.
"""

from pathlib import Path

BATCH_7_DATA = {
    "writing-skills": """
## Domain SOTA & Industry Engineering Standards

- **Specification Standard:** Agent Skills Standard (v1.0.0) compliant with Kilo Code, OpenCode, Gemini CLI, and Antigravity.
- **Progressive Disclosure:** Minimal essential instructions in `SKILL.md` with deep domain offload into `references/` and `scripts/`.
- **Typed Frontmatter:** Strict YAML Frontmatter schema (`name`, `description`, `version`, `tags`, `related_skills`).
- **Instruction Density & Tone:** High-density, active-voice imperative guidance; zero conversational fluff.

### Agent Skills Frontmatter Formal Schema:

```yaml
---
name: "kebab-case-skill-name"
description: "High-density functional summary for semantic routing (<200 chars)"
version: "1.0.0"
tags:
  - "category"
  - "domain"
related_skills:
  - "companion-skill-1"
  - "companion-skill-2"
---
```

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Imperative Command Voice):** Write instructions as direct commands ("Execute", "Validate", "Inject") rather than passive descriptions ("The agent should execute").
2. **Rule of Thumb 2 (Token Ceiling Constraint):** Keep `SKILL.md` under 4,000 tokens; move detailed tables, background theory, or heavy code snippets into `references/` or companion scripts.
3. **Rule of Thumb 3 (Explicit Negative Triggers):** Always include an explicit "Do not use when" section under `## When to Use` to prevent false-positive agent routing.
4. **Rule of Thumb 4 (Executable Verification Gate):** Every skill must end with a concrete, checkable `## Completion Gate & Verification` checklist.
""",

    "skill-creator": """
## Domain SOTA & Industry Engineering Standards

- **Directory Layout & Modular Assets:** Canonical skill tree (`SKILL.md`, `scripts/`, `references/`, `resources/`).
- **Token Budget Allocation:** Frontmatter $\le 150$, When to Use $\le 200$, Core Workflow $\le 1,500$, Standards $\le 1,200$, Gate $\le 400$ tokens.
- **Automated Validation:** Schema verification via `validate-skill.sh` and index synchronization via `sync-index.sh`.
- **Deterministic Scaffolding:** CLI scaffolding engine generating test cases and documentation simultaneously.

### Canonical Skill Structure Tree:
```text
skills/{skill-name}/
├── SKILL.md                 # Primary instruction payload (≤4,000 tokens)
├── scripts/                 # Deterministic helper scripts & tools
├── references/              # Deep domain reference documentation
└── resources/               # Templates, configs, and boilerplate assets
```

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Validate on Creation):** Immediately run `bash scripts/validate-skill.sh skills/{skill-name}` after scaffolding.
2. **Rule of Thumb 2 (Unique Routing Intent):** The `description` field must contain distinct trigger keywords that prevent semantic collisions in vector RAG routing.
3. **Rule of Thumb 3 (Deterministic Code Execution):** Wrap complex computational tasks or multi-step transforms in dedicated Python/Bash scripts under `scripts/`.
4. **Rule of Thumb 4 (Automatic Index Sync):** Always invoke `./scripts/sync-index.sh` after creating or deleting any skill.
""",

    "skill-audit-bulletin": """
## Domain SOTA & Industry Engineering Standards

- **Dual-Axis Audit Methodology:** Structural & Metadata Quality (Axis 1) coupled with Domain SOTA Depth (Axis 2).
- **Master Ledger Synchronization:** Continuous tracking in `SKILL_AUDIT_LEDGER.md` with SHA-256 fingerprinting.
- **Automated ADR Triggers:** Automatic ADR escalation whenever a skill scores $<80/100$ or exhibits critical cognitive debt.
- **Continuous Drift Detection:** Real-time variance tracking across multi-batch remediation cycles.

### Scoring Grade Calibration Matrix:

| Score Range | Grade | Classification | Action Gate |
|:---|:---:|:---|:---|
| **$\ge 95.0$** | **S (Diamond)** | Exceptional / Industry Benchmark | Lock as canonical reference template. |
| **$90.0 - 94.9$** | **A+ / A (Platinum/Gold)** | Production SOTA Grade | Certified for mission-critical workflows. |
| **$80.0 - 89.9$** | **B+ / B (Silver)** | Standard Production Grade | Solid; eligible for iterative polish. |
| **$< 80.0$** | **C / F (Bronze/Fail)** | Sub-Standard / Deficient | Automatic ADR remediation trigger. |

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Dual-Axis Verification):** Never score a skill based solely on word count or file size; verify both structural compliance and domain-specific depth.
2. **Rule of Thumb 2 (Immediate ADR Escalation):** If any skill falls below 80.0 points, generate a remediation task in the active ADR backlog immediately.
3. **Rule of Thumb 3 (Ledger Immutability):** Keep historical audit scores transparently logged with commit timestamps in `SKILL_AUDIT_LEDGER.md`.
4. **Rule of Thumb 4 (Cross-Skill Consistency):** Audit companion skills jointly to guarantee unified terminology and non-contradictory workflows.
""",

    "skill-discovery": """
## Domain SOTA & Industry Engineering Standards

- **Hybrid Retrieval:** Reciprocal Rank Fusion (RRF) combining BM25 keyword matching and vector cosine similarity.
- **Local RAG Architecture:** SQLite3 + FTS5 full-text indexing + local ChromaDB / SQLite vector embeddings.
- **Confidence Calibration:** Dynamic routing thresholds with confidence score cutoffs ($\text{Threshold} \ge 0.75$).
- **Tool Protocol Integration:** MCP stdio tool server exposing `route_task` and `search_skills`.

### Reciprocal Rank Fusion (RRF) Mathematical Formula:

$$\text{RRF\_Score}(d) = \frac{1}{60 + r_{\text{BM25}}(d)} + \frac{1}{60 + r_{\text{Vector}}(d)}$$

Where $r_{\text{BM25}}(d)$ and $r_{\text{Vector}}(d)$ are the 1-indexed ranks from the lexical and vector retrievers.

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Hybrid Query Invariant):** Always fuse keyword search with vector semantic search to capture both exact token matches and conceptual intents.
2. **Rule of Thumb 2 (Sub-100ms Response Bound):** Skill routing must execute in under 100ms using local embedded databases (SQLite/FTS5).
3. **Rule of Thumb 3 (Top-K Routing Limit):** Return at most 3 most relevant skills for complex tasks to prevent agent context pollution.
4. **Rule of Thumb 4 (Confidence Gating):** If no skill meets the $0.75$ confidence cutoff, return an empty set rather than hallucinating irrelevant skills.
""",

    "find-skills": """
## Domain SOTA & Industry Engineering Standards

- **Lexical Search Engines:** SQLite FTS5 with BM25 ranking, Porter stemmer, and unicode61 tokenizer.
- **Query Expansion:** Automatic synonym expansion, kebab-case splitting, and tag matching.
- **Fuzzy Search Ladders:** Exact Match $\to$ Prefix Match (`prefix*`) $\to$ Trigram/Levenshtein Fuzzy Match.
- **Zero-Latency Invariants:** In-memory caching for sub-millisecond CLI routing lookups.

### Search Fallback Ladder:

```text
Query ──> Exact Match in index.json?
             ├── YES ──> Return Skill (Rank #1)
             └── NO  ──> SQLite FTS5 BM25 Search
                            ├── MATCH ──> Return Ranked Results
                            └── NO MATCH ──> Trigram Fuzzy Match Fallback
```

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Prefix Tokenization):** In FTS5 queries, always append `*` to the final search token to enable instant prefix matching.
2. **Rule of Thumb 2 (Clean CLI Output):** Format CLI search results with clear name, version, and 1-line description highlights.
3. **Rule of Thumb 3 (Instant Cache Invalidation):** Re-index SQLite FTS5 immediately upon detecting file modification events in `skills/`.
4. **Rule of Thumb 4 (Tag Weighting):** Assign $2\times$ relevance weighting to matches found within the frontmatter `tags` list.
""",

    "verification-before-completion": """
## Domain SOTA & Industry Engineering Standards

- **Zero-Unverified-Deliverable Invariant:** Never declare any task complete without executing and verifying actual test/validation commands.
- **Exit Code Verification:** Explicit assertion that validation commands exit with code `0 (ALL_PASS)`.
- **Evidence-Based Walkthroughs:** Document concrete proof of execution (diffs, test output logs, metrics) in `walkthrough.md`.
- **Pre-Commit Enforcement:** Automated pre-commit git hooks running test suites and audit engines before allowing commits.

### Verification State Machine:

```mermaid
graph LR
    A[Code Changes Made] --> B[Run Automated Tests]
    B -->|Tests Pass Code 0| C[Generate Evidence Record]
    B -->|Tests Fail| D[Systematic Debugging & Fix]
    D --> B
    C --> E[Declare Task Completed]
```

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Evidence Before Assertion):** Do not claim a bug is fixed or a feature works without showing the exact terminal command output demonstrating success.
2. **Rule of Thumb 2 (Zero Warnings on Build):** Deliverables must build with zero compiler/linter warnings on strict settings.
3. **Rule of Thumb 3 (Check Clean Git Tree):** Confirm `git status` shows only expected modified files before concluding.
4. **Rule of Thumb 4 (Automated Regression Check):** Run the entire test suite (`python3 -m unittest discover`) rather than only testing the isolated modified file.
""",

    "git-workflow": """
## Domain SOTA & Industry Engineering Standards

- **Trunk-Based Development:** Short-lived feature branches ($T_{\text{branch}} \le 24\text{h}$), continuous integration, and atomic merges.
- **Commit Disciplines:** Conventional Commits (v1.0.0) format with scope and descriptive summaries.
- **Branch Naming Conventions:** `feature/*`, `fix/*`, `docs/*`, `adr-XXX/*`, and `chore/*`.
- **Security & Integrity:** GPG/SSH signed commits and rebase-first history hygiene (`git pull --rebase`).

### Git Branching & Merge Strategy:

```text
main / master ─────────────────────────────────────────────────► (Deployable SSOT)
   │                                              ▲
   └──► feature/short-lived-branch (≤24h) ────────┘ (Squash / Rebase Merge)
```

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Short-Lived Branches):** Feature branches must not live longer than 24 hours without merging or rebasing onto trunk.
2. **Rule of Thumb 2 (Atomic Commits):** Each commit must represent a single, self-contained logical change that builds and passes all tests.
3. **Rule of Thumb 3 (Never Force Push Trunk):** Force pushing (`git push --force`) to `master` or `main` is strictly prohibited.
4. **Rule of Thumb 4 (Descriptive Commit Messages):** Follow `type(scope): summary` format; never use vague messages like "fix bug" or "updates".
""",

    "repo-bootstrap": """
## Domain SOTA & Industry Engineering Standards

- **6-Pillar Repository Governance:** `README.md`, `USAGE.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, and `LICENSE`.
- **Agent Governance Standard:** Canonical `AGENTS.md` and `GEMINI.md` anchoring Single Source of Truth (SSOT).
- **CI/CD & Automation Scaffolding:** GitHub Actions workflows for automated linting, testing, and multi-runtime skill deployment.
- **Git Hooks Automation:** Husky / standalone `.git/hooks/` pre-commit and post-commit verification scripts.

### Repository Governance File Hierarchy:

```text
.
├── AGENTS.md                 # SSOT Governance rules for AI coding agents
├── README.md                 # Project elevator pitch & overview
├── USAGE.md                  # Comprehensive developer & agent usage guide
├── CHANGELOG.md              # Keep a Changelog (v1.1.0) release ledger
├── CONTRIBUTING.md           # Contribution guidelines & PR etiquette
├── CODE_OF_CONDUCT.md       # Contributor Covenant Code of Conduct
├── SECURITY.md               # Vulnerability reporting & security policy
└── LICENSE                   # Open-source license (MIT/Apache-2.0)
```

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (SSOT Governance Invariant):** Every repository must contain an `AGENTS.md` specifying canonical tool use, architecture, and constraints.
2. **Rule of Thumb 2 (Security Policy Mandate):** Provide a clear `SECURITY.md` with private vulnerability disclosure instructions before public release.
3. **Rule of Thumb 3 (Deterministic Bootstrap Script):** Provide a single bootstrap command (`./scripts/bootstrap.sh` or `npm run setup`) that installs all dependencies and hooks.
4. **Rule of Thumb 4 (Consistent License):** Explicitly declare the open-source license in both `LICENSE` and `README.md`.
""",

    "release": """
## Domain SOTA & Industry Engineering Standards

- **Supply Chain Security:** Supply-chain Levels for Software Artifacts (SLSA Level 3) compliance and provenance attestation.
- **Cryptographic Asset Signing:** GPG commit signing and Cosign / Sigstore keyless container & binary signing.
- **Release Automation:** Semantic Release, GitHub Releases with automated asset uploads and SHA-256 checksum manifests.
- **Rollback Preparedness:** Automated canary releases, fast rollback triggers, and immutable release tags.

### Release Pipeline Flow:

```mermaid
graph LR
    A[SemVer Bump Trigger] --> B[Generate Changelog]
    B --> C[Run Full Test Suite]
    C --> D[Sign Git Tag GPG]
    D --> E[Generate SHA-256 Checksums]
    E --> F[Publish GitHub Release & Deploy]
```

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Cryptographic Checksums):** Every released binary or archive MUST be accompanied by an official `SHA256SUMS` manifest.
2. **Rule of Thumb 2 (Immutable Release Tags):** Never delete, move, or overwrite an existing release tag in git.
3. **Rule of Thumb 3 (Release Verification Checklist):** Release manager or agent must verify all CI checks are green before tagging.
4. **Rule of Thumb 4 (SLSA Provenance):** Generate machine-readable build provenance attestations for all production distribution artifacts.
""",

    "technical-documentation": """
## Domain SOTA & Industry Engineering Standards

- **6-Pillar SSOT Reconciliation:** Simultaneous synchronization across `README.md`, `USAGE.md`, `CHANGELOG.md`, `RELEASE-NOTES.md`, `STATE.md`, and `AGENTS.md`.
- **Architectural Visualization:** Mermaid.js diagrams (C4 component, Sequence, Entity-Relationship, Flowcharts).
- **Documentation Testing:** Automated Markdown linting, link checking, and code block syntax verification.
- **Living Documentation:** Continuous documentation updates integrated into the definition of done for all features.

### 6-Pillar SSOT Documentation Matrix:

| Pillar | File Target | Content Responsibility |
|:---|:---|:---|
| **Overview** | `README.md` | Executive summary, badges, key features, and quickstart. |
| **Usage** | `USAGE.md` | Step-by-step developer and agent workflows with code samples. |
| **Changelog** | `CHANGELOG.md` | Chronological release history (Keep a Changelog v1.1.0). |
| **Release Notes** | `RELEASE-NOTES.md` | High-impact release summaries, migration guides, and breaking changes. |
| **Governance** | `AGENTS.md` / `GEMINI.md` | Agent instructions, SSOT architecture, and execution constraints. |
| **Architecture** | `docs/adr/` & `docs/audit/` | Architecture Decision Records and audit ledgers. |

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Reconciliation Mandate):** When adding or modifying a feature, update all 6 canonical documentation pillars simultaneously.
2. **Rule of Thumb 2 (Mermaid Diagram Invariant):** Complex multi-agent or system architectures must include a rendered Mermaid diagram.
3. **Rule of Thumb 3 (Zero Broken Links):** All relative file and section links must be verified; zero 404 broken links allowed.
4. **Rule of Thumb 4 (Tested Code Samples):** All code snippets in documentation must be syntax-valid and tested against the active codebase.
"""
}

def main():
    root = Path(__file__).resolve().parent.parent
    skills_dir = root / "skills"
    
    for skill_name, sota_text in BATCH_7_DATA.items():
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
