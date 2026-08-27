#!/usr/bin/env python3
"""
scripts/remediate_batch6_structural_polish.py — Polishes structural headings & gates for Batch 6 skills
"""

from pathlib import Path

def polish_skill(skill_path: Path, name: str, when_to_use_block: str, completion_gate_block: str):
    skill_file = skill_path / "SKILL.md"
    if not skill_file.exists():
        return
    content = skill_file.read_text(encoding="utf-8")
    
    if "## When to Use" not in content:
        lines = content.splitlines(keepends=True)
        insert_idx = 0
        for i, line in enumerate(lines):
            if line.startswith("# ") and i > 5:
                insert_idx = i + 2
                break
        if insert_idx > 0:
            lines.insert(insert_idx, when_to_use_block + "\n\n")
            content = "".join(lines)
            
    if "## Completion Gate" not in content and "## Verification Gate" not in content:
        content = content + "\n\n" + completion_gate_block
        
    skill_file.write_text(content, encoding="utf-8")
    print(f"[✓] Polished: {name}")

def main():
    root = Path(__file__).resolve().parent.parent
    skills_dir = root / "skills"
    
    # 1. llm-as-judge
    laj_wtu = """## When to Use

### Use when:
- Establishing automated LLM evaluation benchmarks and model grading
- Evaluating conversational outputs against 1-5 rubrics with CoT justifications
- Measuring Cohen's Kappa ($\kappa \ge 0.70$) agreement between model and human evaluators

### Do not use when:
- Deterministic unit tests with exact binary assertion matching"""

    laj_gate = """## Completion Gate & Verification
Before concluding LLM judge evaluation:
- [ ] Symmetric pairwise evaluation executed to eliminate position bias
- [ ] Step-by-step reasoning emitted before numerical score
- [ ] Inter-annotator agreement ($\kappa \ge 0.70$) verified across evaluation sample"""
    polish_skill(skills_dir / "llm-as-judge", "llm-as-judge", laj_wtu, laj_gate)

    # 2. content-creator
    cc_wtu = """## When to Use

### Use when:
- Drafting marketing copy, landing page headlines, and social media posts
- Optimizing text for Flesch Reading Ease ($RE \ge 60$) and active voice ($\ge 90\%$)
- Applying AIDA, PAS, or BAB conversion copywriting frameworks

### Do not use when:
- Writing dense academic research papers with formal bibliography citations"""

    cc_gate = """## Completion Gate & Verification
Before concluding copywriting draft:
- [ ] Readability verified ($RE \ge 60$) with concise paragraphs ($\le 4$ lines)
- [ ] Active voice ratio verified $\ge 90\%$
- [ ] Single clear call-to-action (CTA) included"""
    polish_skill(skills_dir / "content-creator", "content-creator", cc_wtu, cc_gate)

    # 3. email-composer
    ec_wtu = """## When to Use

### Use when:
- Drafting executive emails, project status updates, and stakeholder proposals
- Formatting messages according to the Bottom Line Up Front (BLUF) hierarchy
- Optimizing subject lines for mobile open rates ($N_{\text{chars}} \le 50$)

### Do not use when:
- Real-time chat messages (Slack/Discord) or long-form documentation"""

    ec_gate = """## Completion Gate & Verification
Before concluding email draft:
- [ ] Subject line constrained to $\le 50$ characters with urgency tag
- [ ] BLUF ask placed on the very first line of the email body
- [ ] Explicit ownership and deadlines assigned for all next steps"""
    polish_skill(skills_dir / "email-composer", "email-composer", ec_wtu, ec_gate)

    # 4. pdf-processing
    pdf_wtu = """## When to Use

### Use when:
- Extracting text, tables, and form fields from PDF documents programmatically
- Generating ISO 19005 compliant PDF/A archival reports and certificates
- Running OCR fallback pipelines on scanned image-only PDF files

### Do not use when:
- Simple plain text or Markdown document generation without PDF styling requirements"""

    pdf_gate = """## Completion Gate & Verification
Before concluding PDF processing:
- [ ] Native vector text extracted without rasterization if text layer is present
- [ ] Generated PDFs validated for PDF/A compliance and font embedding
- [ ] Sensitive author metadata stripped from generated outputs"""
    polish_skill(skills_dir / "pdf-processing", "pdf-processing", pdf_wtu, pdf_gate)

    # 5. docx-processing
    docx_wtu = """## When to Use

### Use when:
- Programmatically generating Word documents (.docx) from structured data templates
- Performing mail-merge operations and filling document tables dynamically
- Modifying OOXML paragraph styles, headers, footers, and table layouts

### Do not use when:
- Unstyled plain text files or raw Markdown documentation"""

    docx_gate = """## Completion Gate & Verification
Before concluding Word document generation:
- [ ] All template placeholder variables `{{ key }}` successfully resolved
- [ ] Explicit column widths defined for all table grids
- [ ] Output opens cleanly in Microsoft Word and LibreOffice without XML errors"""
    polish_skill(skills_dir / "docx-processing", "docx-processing", docx_wtu, docx_gate)

    # 6. xlsx-processing
    xlsx_wtu = """## When to Use

### Use when:
- Generating complex multi-sheet Excel spreadsheets with formulas and conditional formatting
- Processing large tabular datasets ($>10,000$ rows) via streaming memory mode (`read_only=True`)
- Applying data validation dropdowns, column auto-sizing, and formula injection defenses

### Do not use when:
- Simple lightweight CSV dumps without formula or styling requirements"""

    xlsx_gate = """## Completion Gate & Verification
Before concluding spreadsheet generation:
- [ ] Large files ($>10,000$ rows) processed using memory streaming
- [ ] All user-supplied inputs sanitized against formula injection (`=`, `+`, `-`, `@`)
- [ ] Column widths auto-fitted and formulas validated"""
    polish_skill(skills_dir / "xlsx-processing", "xlsx-processing", xlsx_wtu, xlsx_gate)

    # 7. changelog-generator
    clg_wtu = """## When to Use

### Use when:
- Generating or updating `CHANGELOG.md` following the Keep a Changelog (v1.1.0) standard
- Parsing Conventional Commits (v1.0.0) into structured release notes
- Determining automated SemVer 2.0.0 version bumps (Major, Minor, Patch)

### Do not use when:
- Casual commit logs without release governance requirements"""

    clg_gate = """## Completion Gate & Verification
Before concluding changelog generation:
- [ ] Keep a Changelog categories (`Added`, `Changed`, `Fixed`, etc.) respected
- [ ] SemVer bump calculated accurately based on commit types
- [ ] Clickable links included for PRs, issues, and commit SHAs"""
    polish_skill(skills_dir / "changelog-generator", "changelog-generator", clg_wtu, clg_gate)

if __name__ == "__main__":
    main()
