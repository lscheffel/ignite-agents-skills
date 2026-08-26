# Examples — Usage Guide

This directory contains two sets of examples with different purposes. They are not interchangeable — each serves a specific audience and tier.

## `quadra/` — Few-Shot Mandatory (Tiers 2 and 3)

`ADR-001.md`, `ADR-001-BP.md`, `ADR-001-TODO.md`, `ADR-001-PI.md` form a
**complete and realistic Quadra** (JWT authentication). The SKILL.md instructs
the agent to read this directory before generating a PI (`adr-pi.md`) in Tiers 2/3,
precisely because these files are the Enterprise, SOTA — concise, concrete, and
placeholder-free reference quality.

**Maintenance Rule:** Any critical anti-pattern defined in the SKILL.md must also be respected here. A few-shot example that violates its own critical rule teaches the agent to violate it as well — this is exactly what happened with the absence of "Alternatives Considered" in `ADR-001.md` before v3.0.0 (see Audit Note in SKILL.md).

## `database-choice.md` — Didactic Example (Tiers 0/1)

A simpler and more explanatory example, designed for humans understanding the
concept of ADR for the first time or for small-scope decisions (Tier 0/1). It does not follow the complete frontmatter of governance artifacts — it is intentionally lighter.