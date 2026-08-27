# ADR-035 Blueprint: Product, Content & Document Processing Domain SOTA

> **Companion Artifact to:** [ADR-035.md](./ADR-035.md)  
> **Type:** Technical Architecture Blueprint (Tier II)  
> **Status:** APPROVED  

---

## 1. Mathematical Models & Evaluation Standards

### 1.1 Inter-Annotator Agreement & Evaluation Reliability (`llm-as-judge`)

Reliability of LLM-based evaluation against human ground truth is quantified via **Cohen's Kappa ($\kappa$)**:

$$\kappa = \frac{P_o - P_e}{1 - P_e}$$

Where:
- $P_o$ is relative observed agreement among judges.
- $P_e$ is hypothetical probability of chance agreement.

**Evaluation Threshold:**
- $\kappa \ge 0.70$: High agreement (Production-ready LLM benchmark).
- $\kappa < 0.60$: Marginal / noisy (Rubric calibration required).

#### Position Bias Calibration:
Every pairwise evaluation must execute in symmetric pairs:
$$\text{Score}(A, B) = \frac{\text{Eval}(A \text{ first}, B \text{ second}) + \text{Eval}(B \text{ first}, A \text{ second})}{2}$$

---

### 1.2 Readability & Cognitive Accessibility (`content-creator`, `email-composer`)

#### Flesch Reading Ease ($RE$):
$$RE = 206.835 - (1.015 \times \text{ASL}) - (84.6 \times \text{ASW})$$

Where $\text{ASL}$ is Average Sentence Length (words/sentence) and $\text{ASW}$ is Average Syllables per Word.

**Standard:** Target $RE \ge 60.0$ (Plain English, highly readable).

---

### 1.3 Memory-Safe Large File Streaming Algebra (`xlsx-processing`, `pdf-processing`)

For datasets with $N_{\text{rows}} > 10,000$ or file size $> 10\text{MB}$:

$$\text{Memory Overhead}_{\text{stream}} = O(N_{\text{chunk}}) \quad \text{where } N_{\text{chunk}} \le 1000 \ll N_{\text{total}}$$

---

### 1.4 Gherkin BDD Acceptance Criteria Contract (`product-spec-engineering`)

```gherkin
Feature: Skill Discovery Engine
  Scenario: Agent queries skills by domain intention
    Given the dedicated Skills RAG database is synchronized
    When the agent calls `route_task` with query "implement circuit breaker"
    Then the system returns `circuit-breaker` as top match with confidence >= 0.85
```
