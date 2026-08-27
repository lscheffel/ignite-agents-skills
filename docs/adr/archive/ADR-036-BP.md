# ADR-036 Blueprint: Meta-Skills, Bootstrapping & SDLC Lifecycle Domain SOTA

> **Companion Artifact to:** [ADR-036.md](./ADR-036.md)  
> **Type:** Technical Architecture Blueprint (Tier II)  
> **Status:** APPROVED  

---

## 1. Mathematical Models & Retrieval Standards

### 1.1 Hybrid Reciprocal Rank Fusion (RRF) (`skill-discovery`, `find-skills`)

Fusion of BM25 lexical search and dense vector embedding similarity:

$$\text{RRF\_Score}(d) = \sum_{m \in \{\text{BM25}, \text{Vector}\}} \frac{1}{k + r_m(d)}$$

Where:
- $k = 60$ (Standard RRF constant smoothing ranking bias).
- $r_m(d)$ is the 1-indexed ordinal rank of document $d$ within retriever $m$.

---

### 1.2 Progressive Disclosure & Token Budget Geometry (`skill-creator`, `writing-skills`)

```text
┌─────────────────────────────────────────────────────────────┐
│ 1. Metadata Frontmatter (YAML)              ≤ 150 tokens    │
├─────────────────────────────────────────────────────────────┤
│ 2. When to Use / Activation Intent          ≤ 200 tokens    │
├─────────────────────────────────────────────────────────────┤
│ 3. Core Process / Decision Rules            ≤ 1,500 tokens  │
├─────────────────────────────────────────────────────────────┤
│ 4. Domain SOTA Standards & Math             ≤ 1,200 tokens  │
├─────────────────────────────────────────────────────────────┤
│ 5. Verification Checklist & Gate            ≤ 400 tokens    │
├─────────────────────────────────────────────────────────────┤
│ 6. Reference Links (Progressive Offload)    ≤ 200 tokens    │
└─────────────────────────────────────────────────────────────┘
TOTAL TOKEN CEILING PER SKILL.md:             ≤ 4,000 tokens
```

---

### 1.3 6-Pillar SSOT Documentation Reconciliation Matrix (`technical-documentation`)

| Pillar | File Path | Scope & Invariants |
|:---|:---|:---|
| **1. Overview** | `README.md` | High-level elevator pitch, quickstart, and badges. |
| **2. Usage Guide** | `USAGE.md` | Step-by-step developer and agent workflows. |
| **3. Changelog** | `CHANGELOG.md` | Keep a Changelog (v1.1.0) history linked to releases. |
| **4. Release Notes** | `RELEASE-NOTES.md` | Curated migration guides for major/minor bumps. |
| **5. Governance** | `AGENTS.md` / `GEMINI.md` | SSOT execution rules, MCP routing, and constraints. |
| **6. Audit & History** | `docs/audit/` & `docs/adr/` | Immutable ledgers and cryptographic evidence records. |
