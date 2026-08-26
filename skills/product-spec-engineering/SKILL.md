---
name: product-spec-engineering
version: 1.0.0
description: PRD generation, technical spec writing, and reverse engineering requirements.
domain: domain-stack
triggers:
- product-spec-engineering
- domain-stack
tags:
- product-spec-engineering
- domain-stack
metadata:
  author: Antigravity Architecture / Refactored
  provenance: internal
  last_audited: '2026-08-05'
---

# Product Spec Engineering Hub

PRD generation, technical spec writing, and reverse engineering requirements.


## Sub-Domain / Component: `spec-writing`

# Specification Writing

## Overview

Specifications define WHAT the software should do, never HOW. This skill applies the Jobs to Be Done (JTBD) methodology to break requirements into properly scoped, testable specification files that drive autonomous implementation. Every spec produces Given/When/Then acceptance criteria free of implementation details.

**This is a RIGID skill.** Every phase, gate, and format rule must be followed exactly.

## The Cardinal Rule

**[HARD-GATE:SPEC]** Specifications must NEVER contain implementation details.

| Forbidden | Allowed |
|-----------|---------|
| Code blocks or snippets | Behavioral descriptions |
| Variable names or function signatures | Observable outcomes |
| Technology choices ("use React", "use PostgreSQL") | Capability requirements ("renders in browser", "persists data") |
| Algorithm suggestions ("use K-means clustering") | Success criteria ("extracts 5-10 dominant colors") |
| Architecture patterns ("use MVC") | User-facing behaviors |
| Library references ("use Zod for validation") | Validation requirements ("rejects malformed input") |

**Why:** Implementation-free specs preserve flexibility. The implementing agent can choose the best approach for the codebase, technology, and constraints — and change course without spec updates.

## Phase 1: Jobs to Be Done (JTBD)

Identify the user's or system's jobs using this format:

```
When [situation], I want to [motivation], so I can [expected outcome].
```

**Examples:**
- "When I upload an image, I want to extract its color palette, so I can use those colors in my design."
- "When I receive an API request, I want to validate the payload, so I can reject malformed data before processing."

Gather jobs through discovery questions:
1. Who is the user/actor?
2. What situation triggers this need?
3. What outcome do they want?
4. What happens if they cannot accomplish this?

STOP after JTBD identification — present all jobs to the user for confirmation before breaking into topics.

## Phase 2: Topics of Concern

Break each job into discrete topics. Apply the **"One Sentence Without 'And'" test:**

| Test | Result | Action |
|------|--------|--------|
| "This spec covers color extraction." | PASS | Single topic — one spec file |
| "This spec covers color extraction and palette rendering." | FAIL | Two topics — split into two spec files |
| "This spec covers user authentication and session management." | FAIL | Split into two specs |
| "This spec covers input validation for the registration form." | PASS | Single topic — one spec file |

Each topic becomes one specification file.

STOP after topic breakdown — confirm the list of spec files before writing them.

## Phase 3: Write Specification Files

**File naming convention:** `<int>-<descriptive-name>.md`

```
specs/
├── 01-color-extraction.md
├── 02-palette-rendering.md
├── 03-export-formats.md
└── 04-color-accessibility.md
```

### Specification File Template

```markdown
# [Topic Name]

## Job to Be Done
When [situation], I want to [motivation], so I can [expected outcome].

## Acceptance Criteria

### [Criterion 1 Name]
- Given [precondition]
- When [action]
- Then [observable outcome]
- And [additional observable outcome]

### [Criterion 2 Name]
- Given [precondition]
- When [action]
- Then [observable outcome]

## Edge Cases
- [Describe boundary condition and expected behavior]
- [Describe error condition and expected behavior]

## Data Contracts
- Input: [Describe shape, constraints, valid ranges]
- Output: [Describe shape, guarantees, invariants]

## Non-Functional Requirements
- Performance: [measurable target, e.g., "responds within 200ms for 95th percentile"]
- Accessibility: [specific standard, e.g., "WCAG 2.1 AA"]
- Security: [specific requirement, e.g., "input sanitized against XSS"]
```

### Acceptance Criteria Quality Rules

| Rule | Good Example | Bad Example |
|------|-------------|-------------|
| Observable behavioral outcome | "Extracts 5-10 dominant colors from any image" | "Use K-means clustering with k=8" |
| Testable | "Color data persists across sessions" | "Store in PostgreSQL JSONB column" |
| Specific and measurable | "Palette changes appear within 500ms" | "Use WebSocket for real-time updates" |
| Independent (stands alone) | "Palette renders when image loads" | "Implement with React useEffect hook" |
| Implementation-free | "Passwords cannot be recovered from stored data" | "Use bcrypt with 12 salt rounds" |

STOP after writing specs — run the audit checklist before proceeding to Phase 4.

### Spec Audit Checklist

| # | Check | Pass Criteria |
|---|-------|--------------|
| 1 | No implementation details | Zero code, function names, or tech choices |
| 2 | One Sentence Without 'And' test | Each spec covers exactly one topic |
| 3 | All criteria are Given/When/Then | No free-form prose criteria |
| 4 | All criteria are testable | Each can be verified by a test |
| 5 | Edge cases documented | At least 2 per spec |
| 6 | Data contracts defined | Input and output shapes specified |
| 7 | Consistent naming | `<int>-<descriptive-name>.md` format |

## Phase 4: Story Map Organization

Organize specs into a story map for release planning:

```
CAPABILITY 1    CAPABILITY 2    CAPABILITY 3    CAPABILITY 4
─────────────   ─────────────   ─────────────   ─────────────
basic upload    auto-extract    manual arrange  export PNG
bulk upload     palette gen     templates       export SVG
drag-drop       color names     grid layout     share link
                accessibility   animation       collaborate
```

- **Horizontal rows** = candidate releases
- **Top row** = minimum viable release
- Each row adds capabilities across the board

### SLC Release Criteria

For each horizontal slice, evaluate:

| Criterion | Question | Standard |
|-----------|----------|----------|
| **Simple** | Can it ship fast with narrow scope? | Weeks, not months |
| **Lovable** | Will people actually want to use it? | Delightful, not just functional |
| **Complete** | Does it fully accomplish a job? | End-to-end, not half-done |

**[HARD-GATE]** A release must satisfy ALL three. "Simple but incomplete" is not shippable. "Complete but not lovable" is not shippable.

STOP after story map — get user confirmation on release slicing before finalizing.

## Phase 5: Specs Audit Mode

When auditing existing specs (rather than writing new ones):

1. Read all spec files in `specs/`
2. Check each against the Cardinal Rule (no code, no implementation details)
3. Verify "One Sentence Without 'And'" test
4. Ensure consistent naming convention
5. Verify Given/When/Then format for all acceptance criteria
6. Flag violations and auto-fix where possible

Deploy up to 100 parallel subagents via the `Agent` tool (with `subagent_type="Explore"`) — one per spec file — for large spec sets.

## Anti-Patterns / Common Mistakes

| Mistake | Why It Is Wrong | What To Do Instead |
|---------|----------------|-------------------|
| Including code snippets in specs | Locks implementation approach | Describe behavior, not mechanism |
| Naming technologies ("use Redis") | Prevents better alternatives | Describe capability ("caches results") |
| Combining topics with "and" | Spec too broad, hard to implement/test | Split into separate spec files |
| Vague acceptance criteria ("works well") | Cannot write a test for it | Specific measurable outcome |
| Missing edge cases | Bugs in boundary conditions | Document at least 2 edge cases per spec |
| Skipping data contracts | Input/output ambiguity | Always define shapes and constraints |
| Writing specs after code | Specs justify code instead of driving it | Specs come BEFORE implementation |
| Acceptance criteria that describe UI layout | Implementation detail | Describe what the user can accomplish |

## Anti-Rationalization Guards

- **[HARD-GATE]** Do NOT include ANY implementation details — no code, no tech names, no architecture
- **[HARD-GATE]** Do NOT skip the "One Sentence Without 'And'" test — split every compound topic
- **[HARD-GATE]** Do NOT accept acceptance criteria that are not in Given/When/Then format
- **[HARD-GATE]** Do NOT skip the audit checklist before finalizing specs
- **Do NOT skip** edge cases — every spec needs at least 2
- **Do NOT skip** data contracts — every spec needs input/output shapes
- **Do NOT** write specs after implementation — specs drive code, not the reverse

## Integration Points

| Skill | Relationship |
|-------|-------------|
| `autonomous-loop` | Planning mode reads specs to identify implementation gaps |
| `acceptance-testing` | Tests are derived directly from spec acceptance criteria |
| `reverse-engineering-specs` | Generates specs from existing code (brownfield) |
| `prd-generation` | PRD provides high-level requirements; specs detail them |
| `planning` | Plans reference spec acceptance criteria for task definition |
| `test-driven-development` | Red phase writes tests matching spec acceptance criteria |
| `writing-skills` | Skills can be specified using this methodology |

## Concrete Example: Complete Spec File

```markdown
# Image Color Extraction

## Job to Be Done
When I upload an image to the design tool, I want to automatically extract
its dominant colors, so I can use those colors in my design palette.

## Acceptance Criteria

### Dominant Color Extraction
- Given an uploaded image in PNG, JPG, or WebP format
- When the extraction process completes
- Then 5-10 dominant colors are returned as hex values
- And colors are ordered by prominence (most dominant first)

### Transparent Image Handling
- Given an uploaded image with transparent regions
- When the extraction process completes
- Then transparent regions are excluded from color analysis
- And at least 3 dominant colors are still returned

### Processing Feedback
- Given an image upload has started
- When extraction is in progress
- Then the user sees a progress indicator
- And extraction completes within 3 seconds for images up to 10MB

## Edge Cases
- Single-color image: returns 1 color (not an error)
- Very large image (>50MB): returns an error with size limit message
- Corrupted image file: returns an error with clear message, no crash
- Animated GIF: extracts colors from the first frame only

## Data Contracts
- Input: Image file (PNG, JPG, WebP), max 50MB
- Output: Array of 1-10 hex color strings, ordered by prominence
- Error output: Error object with code and human-readable message

## Non-Functional Requirements
- Performance: <3s for images up to 10MB, <10s for images up to 50MB
- Accessibility: Color values include WCAG contrast ratio against white/black
```

## Verification Gate

Before claiming specs are complete:

1. VERIFY the Cardinal Rule — zero implementation details in any spec
2. VERIFY every spec passes the "One Sentence Without 'And'" test
3. VERIFY all acceptance criteria use Given/When/Then format
4. VERIFY every spec has edge cases and data contracts
5. VERIFY the story map has at least one complete SLC release slice
6. VERIFY the user has confirmed the spec set

## Skill Type

**Rigid** — The no-implementation-details rule, JTBD structure, Given/When/Then format, and audit checklist must be followed exactly. No elements may be skipped or adapted.

---


## Sub-Domain / Component: `prd-generation`

# PRD Generation

## Overview

Transform high-level ideas into structured Product Requirements Documents through guided discovery. This skill walks through problem/solution/constraint discovery, generates a professional PRD with measurable goals and user stories, and ensures stakeholder approval before saving.

**Announce at start:** "I'm using the prd-generation skill to create a Product Requirements Document."

## Phase 1: Discovery

Ask these questions ONE AT A TIME (prefer multiple choice where possible).

**Do NOT skip discovery.** Even if the user provides a detailed brief, confirm understanding by asking at least 3 clarifying questions.

STOP after discovery — present a summary of collected answers and get confirmation before drafting.

### Problem Space Questions

| # | Question | Why It Matters |
|---|----------|----------------|
| 1 | What problem does this solve? | Anchors the entire PRD |
| 2 | Who are the target users? (personas, roles) | Shapes user stories |
| 3 | How are users currently solving this? | Identifies competitive landscape |
| 4 | What is the impact of NOT solving this? | Justifies priority |

### Solution Space Questions

| # | Question | Why It Matters |
|---|----------|----------------|
| 5 | What does success look like? (specific metrics) | Defines success metrics |
| 6 | What are must-have vs nice-to-have features? | Sets priority tiers |
| 7 | What are the explicit non-goals? | Prevents scope creep |
| 8 | Are there existing solutions to learn from? | Informs design decisions |

### Constraint Questions

| # | Question | Why It Matters |
|---|----------|----------------|
| 9 | What is the timeline? Any hard deadlines? | Scopes release plan |
| 10 | What technical constraints exist? | Narrows solution space |
| 11 | What resources are available? | Sets realistic expectations |
| 12 | Are there compliance or regulatory requirements? | Identifies non-functional reqs |

## Phase 2: Draft PRD

Generate the PRD using the template below. Dispatch the `prd-writer` agent with collected answers for heavy generation.

STOP after drafting — do NOT present as final until Phase 3 review is complete.

### PRD Template

```markdown
# [Product/Feature Name] — Product Requirements Document

## 1. Overview
One paragraph summarizing what this is and why it matters.

## 2. Problem Statement
- Current situation
- Pain points
- Impact of not solving

## 3. Goals & Non-Goals
### Goals
- [ ] Goal 1 (measurable)
- [ ] Goal 2 (measurable)

### Non-Goals
- Explicitly NOT doing X
- Explicitly NOT doing Y

## 4. User Stories
As a [persona], I want to [action], so that [benefit].

## 5. Functional Requirements
### FR-1: [Requirement Name]
- Description
- Acceptance criteria
- Priority (P0/P1/P2)

## 6. Non-Functional Requirements
- Performance: [specific targets]
- Security: [requirements]
- Accessibility: [standards]
- Scalability: [expectations]

## 7. Technical Constraints
- Platform/stack requirements
- Integration dependencies
- Data requirements

## 8. Success Metrics
| Metric | Current | Target | How to Measure |
|--------|---------|--------|----------------|

## 9. Timeline & Milestones
| Phase | Description | Target Date |
|-------|-------------|-------------|

## 10. Open Questions
- [ ] Question 1
- [ ] Question 2

## 11. Appendix
References, mockups, related documents
```

### Priority Classification

| Priority | Meaning | Rule |
|----------|---------|------|
| **P0** | Must-have for launch | Without this, the product does not ship |
| **P1** | Important, ship soon after launch | Significant value but not blocking |
| **P2** | Nice-to-have | Enhances experience, can wait |

## Phase 3: Review

Present the PRD section by section:

1. After each section, ask: "Does this capture your intent? Any changes?"
2. Revise based on feedback before moving to next section
3. Pay special attention to these high-signal sections:
   - Goals & Non-Goals (scope alignment)
   - User Stories (persona accuracy)
   - Success Metrics (measurability)
   - Functional Requirements (acceptance criteria completeness)

STOP after review — get explicit "approved" confirmation before saving.

## Phase 4: Save and Transition

After explicit approval:

1. Save to `docs/prds/YYYY-MM-DD-<feature>.md`
2. Commit the PRD with message: `docs(prd): add PRD for <feature>`
3. If implementation follows, invoke the `brainstorming` skill
4. If specs are needed, invoke the `spec-writing` skill

### Transition Decision Table

| User Intent | Next Skill | Rationale |
|-------------|-----------|-----------|
| "Let's build this" | `brainstorming` → `planning` | Explore approaches then plan |
| "Write the specs" | `spec-writing` | Break PRD into JTBD specs |
| "Just save it" | None | PRD is the deliverable |
| "Get estimates" | `task-decomposition` | Break into estimable tasks |

## Anti-Patterns / Common Mistakes

| Mistake | Why It Is Wrong | What To Do Instead |
|---------|----------------|-------------------|
| Skipping discovery and jumping to draft | Produces assumptions-based PRD | Always complete Phase 1 first |
| Goals without metrics | Cannot measure success | Every goal needs a number |
| Missing non-goals | Scope creep guaranteed | Explicitly list what is out of scope |
| User stories without acceptance criteria | Untestable requirements | Add Given/When/Then to each story |
| Generic success metrics ("improve UX") | Unmeasurable | Use specific numbers: "reduce load time to <2s" |
| Presenting entire PRD at once for review | User overwhelmed, gives superficial approval | Present section by section |
| Copying competitor features verbatim | Misses actual user needs | Focus on user problems, not solutions |

## Anti-Rationalization Guards

- **Do NOT** skip discovery because "the user already described it well enough"
- **Do NOT** leave placeholder text in any section — fill every section or mark as "TBD: [reason]"
- **Do NOT** proceed to save without explicit user approval of each section
- **Do NOT** invent success metrics — they must come from the user

## Integration Points

| Skill | Relationship |
|-------|-------------|
| `brainstorming` | Upstream: explores ideas before PRD; downstream: explores implementation after PRD |
| `spec-writing` | Downstream: PRD provides high-level requirements; specs detail them with JTBD |
| `planning` | Downstream: plan references PRD requirements for task breakdown |
| `task-decomposition` | Downstream: breaks PRD into estimable work items |
| `tech-docs-generator` | Parallel: PRD informs what documentation is needed |
| `acceptance-testing` | Downstream: acceptance criteria from PRD feed test definitions |

## Verification Gate

Before claiming the PRD is complete:

1. VERIFY all 11 sections are filled (not placeholder text)
2. VERIFY every goal has a measurable metric
3. VERIFY non-goals are explicit and meaningful
4. VERIFY user stories have acceptance criteria
5. VERIFY user has approved each section individually
6. VERIFY the file is saved and committed

## Concrete Example: Discovery Summary

```
Problem: Users cannot find relevant search results in the dashboard.
Users: Data analysts (primary), team leads (secondary).
Current workaround: Export to Excel and use Ctrl+F.
Impact of not solving: 30min/day wasted per analyst (team of 12).
Success metric: Reduce average search time from 5min to <30s.
Must-have: Full-text search across all dashboard widgets.
Non-goal: Advanced boolean query syntax (P2, not launch).
Timeline: 6 weeks to MVP.
Constraint: Must work with existing Elasticsearch cluster.
```

This summary is presented to the user for confirmation before Phase 2 begins.

## Skill Type

**Flexible** — Adapt discovery depth and PRD structure to project context while preserving the discovery-before-drafting principle and section-by-section review process.

---


## Sub-Domain / Component: `reverse-engineering-specs`

# Reverse Engineering Specifications

## Overview

For brownfield/legacy projects without documentation, this skill generates implementation-free specifications by exhaustively analyzing existing code. The output is a complete behavioral description that drives autonomous development on top of the existing codebase — enabling safe refactoring, feature addition, and modernization.

**Key principle:** Document actual behavior, including bugs. Bugs are "documented features" until explicitly marked for fixing.

**This is a RIGID skill.** Every code path must be traced. No assumptions, no skipping.

## Phase 1: Exhaustive Code Investigation

**[HARD-GATE]** Every code path must be traced. No assumptions, no skipping.

Deploy parallel subagents via the `Agent` tool (up to 500, with `subagent_type="Explore"`) to analyze:

| Analysis Target | What to Document | Priority |
|----------------|-----------------|----------|
| Entry points | All ways the system can be invoked (HTTP, CLI, events, cron) | P0 |
| Code paths | Every branch, loop, conditional, early return | P0 |
| Data flows | Input → transformation → output for every pipeline | P0 |
| State mutations | Every place state is read, written, or deleted | P0 |
| Error handling | Try/catch blocks, error codes, fallback behaviors | P0 |
| Side effects | External calls, file I/O, database writes, event emissions | P1 |
| Configuration | Environment variables, config files, feature flags | P1 |
| Dependencies | External services, libraries, APIs consumed | P1 |
| Concurrency | Async operations, race conditions, locking mechanisms | P2 |
| Implicit behavior | Convention-based routing, middleware chains, decorators | P2 |

### Investigation Strategy Decision Table

| Codebase Size | Strategy | Subagent Count |
|--------------|----------|---------------|
| Small (<50 files) | Single-pass full scan | 5-10 |
| Medium (50-500 files) | Module-by-module scan | 50-100 |
| Large (500+ files) | Entry-point-first, then depth scan | 200-500 |

STOP after investigation — present a summary of discovered entry points, data flows, and behaviors. Get confirmation before generating specs.

## Phase 2: Behavioral Specification Generation

Transform code analysis into implementation-free specs following the `spec-writing` skill format.

### Transformation Rules

| Rule | Explanation |
|------|-------------|
| Strip ALL implementation details | No function names, variable names, technology references |
| Describe WHAT, never HOW | Observable behavior only |
| Document actual behavior (bugs included) | Bugs become "current behavior" in specs |
| Use Given/When/Then format | For all acceptance criteria |
| Include data contracts | Input shapes, output shapes, invariants |
| Separate known issues | Bugs go in KNOWN_ISSUES.md, not inline |

### Implementation Detail Stripping

| Code Artifact | What You See | What You Write in Spec |
|--------------|-------------|----------------------|
| `jwt.verify(token, secret)` | Token validation with JWT | "Credentials are validated against the authentication system" |
| `redis.get(cacheKey)` | Redis cache lookup | "Previously computed results are retrieved from cache" |
| `if (user.role === 'admin')` | Role check | "Privileged operations require administrator access" |
| `res.status(429).json(...)` | Rate limiting response | "Excessive requests receive a rate limit error" |
| `bcrypt.hash(pw, 12)` | Password hashing | "Passwords are stored in a non-reversible format" |

STOP after spec generation — run the completeness checklist before organizing.

## Phase 3: Specification Organization

Create spec files following the naming convention:

```
specs/
├── 01-[first-capability].md
├── 02-[second-capability].md
├── ...
├── NN-[last-capability].md
└── KNOWN_ISSUES.md
```

### KNOWN_ISSUES.md Format

```markdown
# Known Issues

## [Issue Title]
- **Current behavior:** [What actually happens]
- **Expected behavior:** [What should happen, if known]
- **Affected specs:** [Which spec files reference this behavior]
- **Severity:** [Critical | High | Medium | Low]
- **Notes:** [Additional context]
```

### Severity Classification

| Severity | Criteria | Action |
|----------|----------|--------|
| **Critical** | Data loss, security vulnerability, system crash | Fix before any new features |
| **High** | Incorrect results, broken workflow | Fix in next release |
| **Medium** | Poor UX, performance issue | Plan for future fix |
| **Low** | Cosmetic, minor inconsistency | Fix opportunistically |

STOP after organization — present the spec file list and KNOWN_ISSUES for review.

## Phase 4: Quality Verification

**[HARD-GATE]** All checks must pass before this phase is complete.

| # | Check | Question | Status |
|---|-------|----------|--------|
| 1 | Entry points | Are ALL entry points documented? | [ ] |
| 2 | Code paths | Are ALL branches and conditionals traced? | [ ] |
| 3 | Data flows | Are ALL input→output pipelines described? | [ ] |
| 4 | State mutations | Are ALL state changes captured? | [ ] |
| 5 | Error handling | Are ALL error paths documented? | [ ] |
| 6 | Side effects | Are ALL external interactions noted? | [ ] |
| 7 | Edge cases | Are boundary conditions described? | [ ] |
| 8 | Concurrency | Are async behaviors documented? | [ ] |
| 9 | Configuration | Are ALL config options listed? | [ ] |
| 10 | Dependencies | Are ALL external dependencies identified? | [ ] |
| 11 | Implementation-free | Zero code, tech names, or architecture in specs? | [ ] |
| 12 | Given/When/Then | All acceptance criteria in correct format? | [ ] |

## Concrete Example: Code to Spec Transformation

### Code (input — what you analyze):
```javascript
function checkAuth(req, res, next) {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).json({ error: 'No token' });
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (e) {
    return res.status(403).json({ error: 'Invalid token' });
  }
}
```

### Spec (output — what you produce):
```markdown
# Request Authentication

## Job to Be Done
When a request arrives at a protected endpoint, I want to verify the
caller's identity, so I can ensure only authorized users access the system.

## Acceptance Criteria

### Valid Credentials
- Given a request with valid credentials in the authorization header
- When the request is processed
- Then the request proceeds to the next handler
- And the authenticated user identity is available to downstream handlers

### Missing Credentials
- Given a request without credentials
- When the request is processed
- Then a 401 status is returned
- And an error message indicates missing credentials

### Invalid Credentials
- Given a request with invalid or expired credentials
- When the request is processed
- Then a 403 status is returned
- And an error message indicates invalid credentials

## Edge Cases
- Malformed authorization header (missing "Bearer" prefix): treated as missing credentials
- Expired credentials: treated as invalid credentials

## Data Contracts
- Input: Authorization header in "Bearer <credential>" format
- Output on success: User identity object attached to request context
- Output on failure: JSON error response with appropriate status code
```

Notice: No mention of JWT, middleware, Express, environment variables, or any implementation detail.

## Anti-Patterns / Common Mistakes

| Mistake | Why It Is Wrong | What To Do Instead |
|---------|----------------|-------------------|
| Skipping "boring" code paths | Undocumented behavior causes bugs during refactoring | Trace EVERY path, even error handlers |
| Leaking implementation details into specs | Defeats the purpose of behavioral specs | Strip all tech names, function names, code |
| Marking bugs as "correct behavior" | Loses the information that it is a bug | Document in KNOWN_ISSUES.md with severity |
| Skipping async/concurrency analysis | Race conditions are the hardest bugs to find | Document all async behavior |
| Analyzing only happy paths | Most bugs live in error paths | Document ALL error handling paths |
| Guessing behavior instead of tracing code | Spec becomes fiction | Read every line — no assumptions |
| Generating specs without user review | Misunderstandings propagate | Present for review after each phase |

## Anti-Rationalization Guards

- **[HARD-GATE]** Do NOT skip any code path — every branch, conditional, and error handler must be traced
- **[HARD-GATE]** Do NOT include ANY implementation details in specs — no code, tech names, or architecture
- **[HARD-GATE]** Do NOT mark the completeness checklist as done until ALL 12 items pass
- **Do NOT skip** concurrency analysis — even if the code "looks synchronous"
- **Do NOT skip** configuration analysis — env vars and feature flags change behavior
- **Do NOT** assume behavior from function names — read the actual code
- **Do NOT** fix bugs while reverse-engineering — document them in KNOWN_ISSUES.md

## Integration Points

| Skill | Relationship |
|-------|-------------|
| `spec-writing` | Output follows spec-writing format; use for audit after generation |
| `autonomous-loop` | Specs feed into planning mode for gap analysis |
| `acceptance-testing` | Tests derived from reverse-engineered acceptance criteria |
| `self-learning` | Populate memory files with discovered project context |
| `planning` | After specs exist, plan improvements or new features |
| `systematic-debugging` | Known issues inform debugging priorities |

## Workflow After Reverse Engineering

| Step | Skill | Purpose |
|------|-------|---------|
| 1 | `reverse-engineering-specs` (this) | Generate behavioral specs from code |
| 2 | `spec-writing` (audit mode) | Verify quality and completeness |
| 3 | `planning` | Identify gaps, plan improvements |
| 4 | `autonomous-loop` | Implement features or fixes with specs as guide |

## Verification Gate

Before claiming reverse engineering is complete:

1. VERIFY the completeness checklist (all 12 items) passes
2. VERIFY zero implementation details in any spec file
3. VERIFY all acceptance criteria use Given/When/Then format
4. VERIFY KNOWN_ISSUES.md exists and categorizes all discovered bugs
5. VERIFY the user has reviewed the spec set and KNOWN_ISSUES

## Skill Type

**Flexible** — Adapt investigation depth and subagent count to codebase size while preserving the exhaustive-investigation and implementation-free output rules. No code paths may be skipped.