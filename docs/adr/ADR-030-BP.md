# ADR-030 Blueprint: Core Architecture & Governance Mathematical & Schema Specifications

> **Companion Artifact to:** [ADR-030.md](./ADR-030.md)  
> **Type:** Technical Architecture Blueprint (Tier II)  
> **Status:** APPROVED  

---

## 1. Domain Mathematical Formulas & Algorithmic Models

### 1.1 Architectural Blast Radius & Reversibility Index (`adr-architecture-elevation`, `adr-generator`)

The decision tier is calculated deterministically via the **Blast Radius Index ($BR$)**:

$$BR = (N_{\text{dependents}} \times 1.5) + (R_{\text{data}} \times 2.0) + (H_{\text{rollback}} \times 0.5)$$

Where:
- $N_{\text{dependents}} \in [0, \infty)$: Number of downstream modules/services directly consuming this contract.
- $R_{\text{data}} \in \{0, 1, 2, 3\}$: Data migration risk (0 = No state change, 1 = Additive non-breaking, 2 = Schema migration required, 3 = Destructive rewrite).
- $H_{\text{rollback}} \in [0, 48]$: Estimated human hours required to execute complete rollback.

**Tier Assignment Rule:**
- $BR < 3.0 \implies$ **Tier 0 (Lightweight ADR)**
- $3.0 \le BR < 7.0 \implies$ **Tier 1 (Standard Triad ADR + BP + TODO)**
- $BR \ge 7.0 \implies$ **Tier 2 (Quadra SOTA + PI + Mandatory Adversarial Review)**

---

### 1.2 Architectural Fitness Functions & Distance Metrics (`architecture-review`)

Coupling and stability conform to **Robert C. Martin's Package Metrics**:

1. **Afferent Coupling ($C_a$):** Number of external classes that depend on this package.
2. **Efferent Coupling ($C_e$):** Number of external classes this package depends upon.
3. **Instability ($I$):** $I = \frac{C_e}{C_a + C_e} \quad (I \in [0, 1])$
4. **Abstractness ($A$):** $A = \frac{N_{\text{abstract}}}{N_{\text{total}}} \quad (A \in [0, 1])$
5. **Normalized Distance from Main Sequence ($D$):**
   $$D = |A + I - 1| \quad (D \in [0, 1])$$

**Acceptance Criterion:** Any package with $D > 0.7$ fails the architectural review gate and requires decoupling/refactoring.

---

### 1.3 Dynamic Context Budgeting Formula (`cap`)

Context exploration budget ($B_{\text{ctx}}$ in tokens) is allocated dynamically:

$$B_{\text{ctx}} = B_{\text{base}} + (\alpha \times N_{\text{symbols}}) + (\beta \times N_{\text{files\_changed}})$$

Where:
- $B_{\text{base}} = 1,500$ tokens
- $\alpha = 250$ tokens/symbol
- $\beta = 800$ tokens/file
- Maximum exploration ceiling: $C_{\text{max}} = 12,000$ tokens.

---

### 1.4 Double Diamond Ambiguity Elimination Metric (`brainstorming`)

Ambiguity score ($A_{\text{score}}$) is evaluated after each Socratic query:

$$A_{\text{score}} = \frac{\text{Unresolved Core Invariants} + \text{Unspecified Non-Goals}}{\text{Total Identified Problem Dimensions}}$$

**Transition Gate:** Convergence (Phase 4/5) is strictly locked until $A_{\text{score}} \le 0.15$.

---

## 2. Machine-Readable Governance Schema Contracts (`governance`, `agents-md-management`)

Canonical agent compliance policy format stored at `.github/governance/agent-policies.json`:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "AgentGovernancePolicy",
  "type": "object",
  "required": ["version", "enforcement_level", "protected_branches", "commit_standards", "runtime_sync"],
  "properties": {
    "version": { "type": "string" },
    "enforcement_level": { "type": "string", "enum": ["STRICT_BLOCK", "WARN", "PERMISSIVE"] },
    "protected_branches": {
      "type": "array",
      "items": { "type": "string" }
    },
    "commit_standards": {
      "type": "object",
      "properties": {
        "require_conventional_commits": { "type": "boolean" },
        "pre_commit_audit_gate": { "type": "boolean" },
        "require_evidence_record_on_adr_closure": { "type": "boolean" }
      }
    },
    "runtime_sync": {
      "type": "object",
      "properties": {
        "sync_targets": { "type": "array", "items": { "type": "string" } },
        "purge_unmanaged_skills_only": { "type": "boolean" }
      }
    }
  }
}
```

---

## 3. Cryptographic Evidence Record Specification (`adr-archive`)

Every generated `ADR-XXX-ER.md` must include a cryptographically bound header block:

```markdown
## Cryptographic Execution Attestation
- **Commit SHA:** `<git-rev-parse-HEAD>`
- **Tree Hash:** `<git-rev-parse-HEAD^{tree}>`
- **Validation Exit Code:** `0 (PASS)`
- **Ledger Score Pre/Post:** `84.0 -> 96.5`
- **Auditor Signature:** `Antigravity SOTA Engine / v3.0`
```
