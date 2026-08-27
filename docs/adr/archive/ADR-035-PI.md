# ADR-035 Implementation Plan (PI): Product, Content & Document Processing Domain SOTA

> **Companion Artifact to:** [ADR-035.md](./ADR-035.md) & [ADR-035-BP.md](./ADR-035-BP.md)  
> **Type:** Phased Implementation Plan (Tier II)  
> **Status:** READY FOR EXECUTION  

---

## 1. Execution Phases

### Phase 1: Product Engineering, Prompts & LLM Evaluation
- [x] 1.1 Ingest BDD Gherkin acceptance criteria, Kano Model feature scoring, and INVEST story rules into `skills/product-spec-engineering/SKILL.md`.
- [x] 1.2 Ingest Chain-of-Density (CoD), Few-Shot exemplars, and DSPy declarative optimization into `skills/prompt-engineering/SKILL.md`.
- [x] 1.3 Ingest Cohen's Kappa ($\kappa \ge 0.70$), position bias calibration, and G-Eval rubrics into `skills/llm-as-judge/SKILL.md`.

### Phase 2: Copywriting, Academic Research & Communication
- [x] 2.1 Ingest Flesch Reading Ease ($RE \ge 60$) and AIDA conversion copywriting into `skills/content-creator/SKILL.md`.
- [x] 2.2 Ingest APA 7th edition citation schemas and CRAAP source evaluation scoring into `skills/content-research-writer/SKILL.md`.
- [x] 2.3 Ingest Executive BLUF (Bottom Line Up Front) and subject line open-rate geometry into `skills/email-composer/SKILL.md`.

### Phase 3: Binary Document Engines & Changelogs
- [x] 3.1 Ingest OOXML hierarchy AST manipulation and docxtpl template contracts into `skills/docx-processing/SKILL.md`.
- [x] 3.2 Ingest PDF/A archival compliance, vector table extraction, and OCR ladders into `skills/pdf-processing/SKILL.md`.
- [x] 3.3 Ingest OpenPyXL chunked streaming (`read_only=True`), formula ASTs, and data validation into `skills/xlsx-processing/SKILL.md`.
- [x] 3.4 Ingest Keep a Changelog (v1.1.0) and Conventional Commits 1.0.0 SemVer bump tree into `skills/changelog-generator/SKILL.md`.

### Phase 4: Structural Polishing & Gating
- [x] 4.1 Polish structural headings (`When to Use`, `Completion Gate`) across all 10 Batch 6 skills.

### Phase 5: Validation, Batch Audit & Ledger Recalculation
- [x] 5.1 Execute `scripts/batch_skill_auditor.py` over Batch 6 skills.
- [x] 5.2 Verify all 10 skills achieve Grade B+ / A / S (Target Catalog Average > 86.0).
- [x] 5.3 Synchronize `docs/audit/skills/SKILL_AUDIT_LEDGER.md`.
- [x] 5.4 Run full test suite and pages build.
