# Skill Audit Bulletin — {skill_name} (v{version})

**Audit date:** {date}
**Overall grade:** {S/A/B/C/D/F} — {0-100}/100
**One-line verdict:** {frase única, sem hedging}
**Recommended action:** {ADOPT AS-IS / ADOPT WITH ADJUSTMENTS / REFACTOR / DEPRECATE}

## 1. Executive Summary
- Strongest point: {evidenciado}
- Weakest point: {evidenciado}
- Principal risk if implemented without changes: {1 sentence}
- Effort to reach the next grade level: {LOW / MEDIUM / HIGH}

## 2. Compliance Structural and Metadata
| Field | Status | Comment |
|---|---|---|
| name | ✅/⚠️/❌ | |
| description | ✅/⚠️/❌ | |
| version | ✅/⚠️/❌ | |
| tags | ✅/⚠️/❌ | |
| related_skills | ✅/⚠️/❌ | |

## 3. Semantic Analysis of Triggering
- Description score: {0-10}
- Keyword coverage gaps: {list + example sentence}
- Risk of collision with related/sibling skills: {list + likelihood}
- False positive scenario(s): {concrete example}
- False negative scenario(s): {concrete example}

## 4. Applicability and Scope
- Clarity of border score: {0-10}
- Decision tree solidity: {evidenciado}
- Overlap/conflict with related_skills: {evidenciado}

## 5. Depth and Coverage of Workflow
- Phase-by-phase evaluation: {table or list}
- Checkpoint quality: {evidenciado}
- Estimated coverage of edge cases: {%} — missing: {list}

## 6. Technical Correction and Robustness
- Validated examples/commands: {list with pass/fail + justification}
- Correction issues found: {evidenciado, with reference to section}

## 7. Universality and Portability
- Environment lock-ins: {list}
- Behavior outside the assumed environment: {amusing / silent failure / unknown}

## 8. Maintainability
- Versioning discipline: {evidenciado}
- Modularity (sections updatable independently?): {evidenciado}
- Risk of external rot (12-month horizon): {list + likelihood}

## 9. Ergonomics for the Executor Agent
- Actionability without inference: {0-10}
- Adequacy of density/size: {evidenciado}
- Excessive trust in the executor model's judgment: {evidenciado}

## 10. Risk Matrix
| Risk | Likelihood | Impact | Mitigation (ref) |
|---|---|---|---|
| | | | → see §13 |

## 11. Pros
- {bullet evidenciado}

## 12. Cons
- {bullet evidenciado} → mitigated in §13

## 13. Mitigations and Recommendations
### Quick wins (< 1h)
- {concrete and specific edit}
### Medium (structurally but scoped)
- {concrete and specific edit}
### Structural (redesign level)
- {concrete and specific edit}

## 14. Scoring Breakdown
| Category | Weight | Score (0-10) | Weighted |
|---|---|---|---|
| Semantic Triggering Precision | 20% | | |
| Applicability / Border Clarity | 10% | | |
| Depth and Coverage | 15% | | |
| Technical Correction | 15% | | |
| Universality / Portability | 10% | | |
| Maintainability | 10% | | |
| Executor Agent Ergonomics | 10% | | |
| Risk Profile (inverted) | 10% | | |
| **Total** | 100% | | **{X}/100** |

## 15. Final Verdict
{2-3 sentences, direct, without hedging. Explicitly declare whether this skill is safe for auto-load in a production registry today.}