---
name: skill-discovery
version: 3.0.0
description: "Single authoritative router and dynamic discovery engine for all canonical skills in the repository."
domain: core-governance
triggers:
  - skill-discovery
  - discovery
  - catalog
  - validate
  - list-skills
tags:
  - skill-discovery
  - core-governance
  - router
  - dynamic-indexing
  - schema-validation
metadata:
  author: "Luciano Scheffel / Antigravity Refactored"
  provenance: "internal"
  last_audited: "2026-08-05"
---

# Skill Discovery & Router Engine

Single authoritative router and dynamic indexing engine for the canonical Skills Repository.

## Executable CLI Engine

The engine is backed by `scripts/discovery.py`. Execute via Python:

```bash
python Skills/skill-discovery/scripts/discovery.py <command>
```

### Available Subcommands

1. **`catalog`**: Scans the `/Skills` directory dynamically and outputs a complete JSON catalog of all active skills.
   ```bash
   python Skills/skill-discovery/scripts/discovery.py catalog
   ```
2. **`validate`**: Runs the ADR-004 Quality Gate check, validating YAML frontmatter schema, CRLF/LF line endings, and CJK character corruptions across all skills.
   ```bash
   python Skills/skill-discovery/scripts/discovery.py validate
   ```
3. **`list`**: Displays canonical skills neatly grouped by their 6 core domains.
   ```bash
   python Skills/skill-discovery/scripts/discovery.py list
   ```
4. **`explain <skill_name>`**: Displays metadata, triggers, and path for a specific skill.
   ```bash
   python Skills/skill-discovery/scripts/discovery.py explain ui-ux-pro-max
   ```

## Domain Categories
- **`core-governance`**: Governance, ADRs, Discovery, Lifecycle, AGENTS.md management.
- **`engineering-quality`**: Debugging, TDD, Testing Mastery, Security Review, Code Review, Performance.
- **`architecture-systems`**: Architecture Review, API Design, Database Architecture, DDD, Observability.
- **`agentic-workflow`**: Planning Execution, Subagents, Agent Orchestration, Git Workflows.
- **`frontend-ux`**: UI/UX Pro Max, Mobile Design, UX Research, React Best Practices.
- **`domain-stack`**: MCP Builder, PHP/Laravel, Product Spec Engineering, Tech Docs, Document Processing.
