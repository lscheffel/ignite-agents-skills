#!/usr/bin/env python3
"""
scripts/remediate_batch6_sota.py — Comprehensive Batch 6 Domain SOTA Elevation (ADR-035)
Injects Cohen's Kappa, Gherkin BDD, Flesch-Kincaid, OpenPyXL Streaming, and PDF/A standards
into the 10 Product, Content & Document Processing skills.
"""

from pathlib import Path

BATCH_6_DATA = {
    "product-spec-engineering": """
## Domain SOTA & Industry Engineering Standards

- **Behavior-Driven Development (BDD):** Gherkin Syntax (Given-When-Then) for executable acceptance criteria.
- **Product Prioritization Frameworks:** Kano Model (Must-be, One-dimensional, Attractive), MoSCoW, and RICE Scoring.
- **User Story Quality Standards:** INVEST Criteria (Independent, Negotiable, Valuable, Estimable, Small, Testable).
- **Specification Formats:** Product Requirement Documents (PRD), RFC/Technical Specs, and Decision Records.

### Kano Model Feature Classification Matrix:

| Category | Customer Satisfaction Dynamic | Engineering Mandate |
|:---|:---|:---|
| **Must-Be (Baseline)** | Absence causes extreme dissatisfaction; presence taken for granted. | Non-negotiable P0; absolute prerequisite. |
| **Performance (Linear)** | Satisfaction scales proportionally with capability (e.g. speed, latency). | Core competitive differentiator. |
| **Delighters (Attractive)** | Absence causes no dissatisfaction; presence triggers unexpected delight. | High-ROI innovation features. |

### Gherkin BDD Acceptance Criteria Contract:

```gherkin
Scenario: Agent queries skills by domain intention
  Given the dedicated Skills RAG database is synchronized
  When the agent calls `route_task` with query "implement circuit breaker"
  Then the system returns `circuit-breaker` as top match with confidence >= 0.85
```

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Zero Ambiguous Acceptance Criteria):** Acceptance criteria must never use subjective terms like "fast", "user-friendly", or "secure" without exact quantitative thresholds.
2. **Rule of Thumb 2 (INVEST Rule):** No single user story should exceed 3 days of implementation effort; split complex stories vertically through the architectural stack.
3. **Rule of Thumb 3 (Non-Functional Requirements Mandate):** Every PRD must define NFRs for Latency ($P_{95}$), Availability SLA, and Concurrent Load.
4. **Rule of Thumb 4 (Traceability Invariant):** Every engineering task in `*-TODO.md` must trace back to a specific requirement in the PRD or ADR.
""",

    "prompt-engineering": """
## Domain SOTA & Industry Engineering Standards

- **Prompt Optimization Paradigms:** Chain-of-Density (CoD), Few-Shot Chain-of-Thought (CoT), Tree of Thoughts (ToT), and DSPy Declarative Signatures.
- **Security & Delimiters:** XML/Markdown boundary tags (`<context>`, `<instruction>`, `<schema>`) preventing prompt injection.
- **Context Compaction:** High signal-to-noise ratio prompt compaction eliminating conversational fluff.
- **Output Determinism:** Strict JSON Schema generation and constrained decoding formats.

### Chain-of-Density (CoD) Stepwise Compression:
1. **Step 1 (Draft):** Generate initial summary capturing main points.
2. **Step 2 (Identify Missing Entities):** Identify 1-3 critical missing domain entities.
3. **Step 3 (Fuse & Condense):** Re-write summary retaining exact word count while infusing missing entities.

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (XML Tag Delimitation):** Always encapsulate untrusted user inputs or retrieved documents within explicit XML tags (`<user_data>...</user_data>`).
2. **Rule of Thumb 2 (Few-Shot Exemplar Rule):** When asking for complex structured output, provide at least 2 diverse few-shot input/output examples.
3. **Rule of Thumb 3 (Positive Constraints Over Negative):** Instruct the model on *what to do* rather than what *not* to do (e.g., "Output JSON only" vs "Do not output prose").
4. **Rule of Thumb 4 (Role & Target Persona):** Clearly declare the persona, expertise domain, and operational constraints at the start of system prompts.
""",

    "llm-as-judge": """
## Domain SOTA & Industry Engineering Standards

- **Evaluation Frameworks:** G-Eval (GPT-4 evaluation with CoT), MT-Bench, and AlpacaEval 2.0.
- **Statistical Reliability:** Cohen's Kappa ($\kappa \ge 0.70$) and Fleiss' Kappa for inter-annotator agreement.
- **Bias Mitigation:** Position Bias calibration (swapped pair scoring), Verbosity Bias normalization, and Self-Enhancement bias prevention.
- **Grading Scales:** Explicit 1-to-5 Rubric scales with distinct anchor definitions for each score.

### Cohen's Kappa Inter-Annotator Agreement Formula:

$$\kappa = \frac{P_o - P_e}{1 - P_e} \ge 0.70$$

Where $P_o$ is relative observed agreement and $P_e$ is hypothetical chance agreement probability.

### Pairwise Position Bias Normalization Formula:

$$\text{FinalScore}(A, B) = \frac{\text{Judge}(A \text{ first}, B \text{ second}) + \text{Judge}(B \text{ first}, A \text{ second})}{2}$$

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Symmetric Pairwise Evaluation):** Always run pairwise comparisons twice with candidate order swapped to eliminate first-position bias.
2. **Rule of Thumb 2 (Chain-of-Thought Evaluation):** The judge LLM must output its step-by-step reasoning *before* emitting the final numerical score.
3. **Rule of Thumb 3 (Rubric Anchor Points):** Never ask for a score of 1-5 without providing explicit, unambiguous definitions for what constitutes a 1, 3, and 5.
4. **Rule of Thumb 4 (Reference Ground Truth):** Provide the golden reference output whenever evaluating factual correctness.
""",

    "content-creator": """
## Domain SOTA & Industry Engineering Standards

- **Readability & Ergonomics:** Flesch Reading Ease ($RE$), Flesch-Kincaid Grade Level ($FKGL$), and Gunning Fog Index.
- **Copywriting Frameworks:** AIDA (Attention, Interest, Desire, Action), PAS (Problem, Agitation, Solution), and BAB (Before, After, Bridge).
- **Voice & Tone Consistency:** Formal Brand Voice Guidelines, active voice ratio ($\ge 90\%$), and conversational cadence.
- **Conversion Optimization:** Action-oriented CTAs, scannable subheadings, and inverted pyramid journalism hierarchy.

### Flesch Reading Ease Formula:

$$RE = 206.835 - (1.015 \times \text{ASL}) - (84.6 \times \text{ASW}) \ge 60.0$$

Where $\text{ASL}$ is Average Sentence Length and $\text{ASW}$ is Average Syllables per Word.

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Active Voice Mandate):** At least $90\%$ of sentences must use active voice ("The team deployed the release" vs "The release was deployed by the team").
2. **Rule of Thumb 2 (Scannable Structure):** No paragraph should exceed 4 lines; use bullet points and bold leading terms for high readability.
3. **Rule of Thumb 3 (Single Clear CTA):** Marketing and business content must drive toward a single primary call to action.
4. **Rule of Thumb 4 (Kill Fluff Words):** Eliminate redundant adverbs and filler phrases ("very", "really", "in order to", "essentially").
""",

    "content-research-writer": """
## Domain SOTA & Industry Engineering Standards

- **Academic Citation Standards:** APA 7th Edition, IEEE Citation Style, and BibTeX structured bibliographies.
- **Source Credibility Evaluation:** CRAAP Test (Currency, Relevance, Authority, Accuracy, Purpose).
- **Evidence-Based Argumentation:** Toulmin Model of Argument (Claim, Data, Warrant, Backing, Counterclaim, Rebuttal).
- **Fact-Checking & Provenance:** Primary source attribution, DOI verification, and hallucination elimination.

### CRAAP Source Evaluation Rubric (Target $\ge 80/100$):
- **Currency:** Published within past 24 months (or seminal foundational paper).
- **Relevance:** Directly addresses the technical research question.
- **Authority:** Peer-reviewed journal, IEEE/ACM conference, or official technical vendor documentation.
- **Accuracy:** Backed by reproducible empirical data and statistical methodology.
- **Purpose:** Informative and objective; free from undisclosed commercial bias.

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Primary Source Attribution):** Cite the original primary research or RFC rather than third-party blog summaries.
2. **Rule of Thumb 2 (Counterclaim Invariant):** Technical whitepapers must address competing alternative architectures and trade-offs before asserting recommendations.
3. **Rule of Thumb 3 (Verified DOIs):** All academic citations must include valid DOIs or canonical archive URLs.
4. **Rule of Thumb 4 (Zero Unsubstantiated Claims):** Quantitative assertions ("X is 5x faster than Y") must be backed by benchmark citations.
""",

    "email-composer": """
## Domain SOTA & Industry Engineering Standards

- **Executive Communication:** Bottom Line Up Front (BLUF), Minto Pyramid Principle, and MECE (Mutually Exclusive, Collectively Exhaustive).
- **Subject Line Geometry:** Character length $\le 50$ characters, front-loaded action verbs, and clear urgency tags (`[Action Required]`, `[FYI]`).
- **Email Deliverability & Hygiene:** Plain-text formatting fallback, spam trigger avoidance, and clear unsubscribe/signature blocks.
- **Tone Modulation:** Formal executive, collaborative peer, empathetic customer service, and firm escalation ladders.

### BLUF (Bottom Line Up Front) Structure:
1. **Line 1 (The Ask / Conclusion):** State the exact action requested and deadline.
2. **Body (Context / Bulleted Data):** Present 2-3 concise supporting facts or options.
3. **Closing (Next Steps):** Explicit confirmation of ownership and next checkpoint.

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (50-Character Subject Line Bound):** Subject lines must not exceed 50 characters to prevent mobile client truncation.
2. **Rule of Thumb 2 (Three-Sentence Rule for Simple Requests):** If an email requires a single decision, constrain the message to $\le 3$ concise sentences.
3. **Rule of Thumb 3 (Explicit Ownership):** State clearly *who* is responsible for *what* by *when* (`@Person: Action by Date`).
4. **Rule of Thumb 4 (No Passive Aggression):** Maintain professional, direct, and collaborative tone even during escalations.
""",

    "docx-processing": """
## Domain SOTA & Industry Engineering Standards

- **Document Object Model (DOM):** Open Packaging Conventions (OPC), Office Open XML (OOXML - ECMA-376), and AST manipulation.
- **Template Engines:** `docxtpl` Jinja2-style document template rendering with mail-merge safety.
- **Style Inheritance & Layout:** Native Word styles, table formatting with explicit column widths, and header/footer relationships.
- **Safety & Portability:** XML entity protection, namespace isolation, and clean font embedding.

### Document Generation Protocol:
1. Load base corporate template containing pre-configured styles (`Heading 1`, `Table Grid`).
2. Populate template context dictionary validating all keys against JSON Schema.
3. Render document and verify all table columns have explicit percentage/point widths.

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Template-Driven Generation):** Never construct complex DOCX files programmatically from scratch; use pre-styled `.docx` templates via `docxtpl`.
2. **Rule of Thumb 2 (Explicit Table Widths):** All table cells and columns must specify explicit widths to prevent Word rendering collapses.
3. **Rule of Thumb 3 (Namespace Isolation):** When modifying raw XML parts, preserve all original OOXML schema namespaces (`w:`, `r:`, `m:`).
4. **Rule of Thumb 4 (Zero Broken Placeholders):** Validate that all template variables `{{ key }}` are resolved before saving the final `.docx` artifact.
""",

    "pdf-processing": """
## Domain SOTA & Industry Engineering Standards

- **Archival Standards:** ISO 19005 (PDF/A-1b, PDF/A-2b) for long-term digital document preservation.
- **Spatial Table Extraction:** Vector bounding box analysis (PDFPlumber, Tabula) and layout-aware text extraction.
- **OCR Fallback Pipeline:** Tesseract OCR (v5.x) preprocessing (deskew, binarization, DPI scaling to 300 DPI).
- **Security & Metadata:** PDF metadata stripping (exif), encryption (AES-256), and digital signature verification.

### Spatial Extraction vs OCR Fallback Pipeline:

```text
Input PDF ──> Native Text Layer Present?
                 ├── YES ──> Spatial Vector Extraction (PDFPlumber) ──> Structured Data
                 └── NO  ──> Render Page to Image (300 DPI) ──> Tesseract OCR ──> Text
```

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Check Native Text First):** Always check for native vector font glyphs before invoking expensive OCR engines.
2. **Rule of Thumb 2 (DPI Scaling for OCR):** Scanned PDF pages must be rasterized at exactly 300 DPI with grayscale binarization before OCR processing.
3. **Rule of Thumb 3 (PDF/A Archival Output):** Generated business reports, invoices, and certificates must be saved in PDF/A compliant format with embedded fonts.
4. **Rule of Thumb 4 (Sanitize Metadata):** Strip author paths, printer IDs, and sensitive metadata before distributing generated PDF files.
""",

    "xlsx-processing": """
## Domain SOTA & Industry Engineering Standards

- **Streaming Memory Bounds:** OpenPyXL Read-Only / Write-Only streaming mode (`read_only=True`, `write_only=True`) for large datasets.
- **Formula & Syntax Engine:** OpenPyXL Formula syntax trees, dynamic named ranges, and formula caching (`data_only=True`).
- **Data Validation & Styling:** Cell data validation dropdowns, conditional formatting rules, and column auto-fit sizing.
- **Type Safety & Sanitization:** Strict CSV/XLSX formula injection prevention (sanitize leading `=`, `+`, `-`, `@`).

### Streaming Memory Algebra:
For worksheets exceeding 10,000 rows, memory consumption must remain bounded:

$$\text{Memory}(\text{Stream}) = O(1) \quad \text{vs} \quad \text{Memory}(\text{DOM}) = O(N_{\text{rows}} \times N_{\text{cols}})$$

### Formula Injection Sanitization Pattern:
```python
def sanitize_cell(value: str) -> str:
    if isinstance(value, str) and value.startswith(('=', '+', '-', '@', '\t', '\r')):
        return "'" + value
    return value
```

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Stream on Large Datasets):** Any spreadsheet with $>10,000$ rows MUST be processed using OpenPyXL `read_only=True` streaming mode.
2. **Rule of Thumb 2 (Formula Injection Defense):** All user-supplied spreadsheet cell values must be sanitized to prevent CSV/Excel Formula Injection attacks.
3. **Rule of Thumb 3 (Data Only for Analysis):** When reading spreadsheets for mathematical data analysis, use `data_only=True` to retrieve cached computed values.
4. **Rule of Thumb 4 (Auto-Fit Column Widths):** Generated spreadsheets must calculate maximum character length per column and apply proportional widths.
""",

    "changelog-generator": """
## Domain SOTA & Industry Engineering Standards

- **Specification Standards:** Keep a Changelog (v1.1.0) and Semantic Versioning (SemVer v2.0.0).
- **Commit Parsing Standards:** Conventional Commits (v1.0.0) format (`feat`, `fix`, `docs`, `refactor`, `perf`, `test`, `chore`).
- **Release Categorization:** Automatic grouping into `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, and `Security`.
- **Breaking Change Semantics:** Automatic Major bump detection on `BREAKING CHANGE:` or `!` commit syntax.

### SemVer 2.0.0 Automated Bump Decision Matrix:

| Commit Types in Release Range | SemVer Bump | Example Version Transition |
|:---|:---:|:---|
| Any commit with `BREAKING CHANGE:` or `type!:` | **MAJOR** | `1.4.2` $\to$ `2.0.0` |
| Contains `feat:` commits with zero breaking changes | **MINOR** | `1.4.2` $\to$ `1.5.0` |
| Only `fix:`, `perf:`, `refactor:` commits | **PATCH** | `1.4.2` $\to$ `1.4.3` |

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Keep a Changelog Conformity):** All changelog outputs must strictly follow the Keep a Changelog format with dated ISO headers (`## [1.5.0] - 2026-08-26`).
2. **Rule of Thumb 2 (Human-Centric Summaries):** Transform technical git commit messages into clear, user-facing descriptions of what changed.
3. **Rule of Thumb 3 (Unreleased Section):** Always maintain an active `## [Unreleased]` section at the top of `CHANGELOG.md` for in-progress changes.
4. **Rule of Thumb 4 (PR & Issue Linkage):** Include clickable links to corresponding pull requests, issues, and commit SHAs for full traceability.
"""
}

def main():
    root = Path(__file__).resolve().parent.parent
    skills_dir = root / "skills"
    
    for skill_name, sota_text in BATCH_6_DATA.items():
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
