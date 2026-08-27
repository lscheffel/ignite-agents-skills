#!/usr/bin/env python3
"""
scripts/remediate_batch5_structural_polish.py — Polishes structural headings & gates for Batch 5 skills
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
    
    # 1. artifacts-builder
    art_wtu = """## When to Use

### Use when:
- Creating standalone single-file HTML/CSS/JS applications, prototypes, or visual calculators
- Building interactive demos that must execute in a browser without a build step or npm
- Visualizing complex state machines, charts, or algorithms interactively

### Do not use when:
- Building enterprise multi-page web applications with server-side routing (use Next.js / Vite)"""

    art_gate = """## Completion Gate & Verification
Before declaring artifact deliverable complete:
- [ ] Single HTML file opens and executes cleanly in modern browsers
- [ ] Zero external insecure script CDNs; CSS/JS self-contained
- [ ] Responsive layout scales smoothly across mobile and desktop viewports"""
    polish_skill(skills_dir / "artifacts-builder", "artifacts-builder", art_wtu, art_gate)

    # 2. react-best-practices
    rbp_wtu = """## When to Use

### Use when:
- Designing React 19 component architectures, hooks, and data-fetching boundaries
- Deciding between Server Components (RSC) and Client Components (`'use client'`)
- Optimizing rendering performance, memoization, and Server Actions

### Do not use when:
- Pure vanilla HTML/CSS projects without React framework requirements"""

    rbp_gate = """## Completion Gate & Verification
Before concluding React architecture review:
- [ ] Server Component boundaries respected with minimal `'use client'` usage
- [ ] Server Action parameters validated with schema library
- [ ] Zero unnecessary re-renders or unmemoized object dependencies"""
    polish_skill(skills_dir / "react-best-practices", "react-best-practices", rbp_wtu, rbp_gate)

    # 3. seo-optimizer
    seo_wtu = """## When to Use

### Use when:
- Implementing technical SEO audits, JSON-LD Schema.org markup, and meta tags
- Optimizing Core Web Vitals (LCP, INP, CLS) and page indexability
- Setting up Open Graph social preview cards and XML sitemaps

### Do not use when:
- Internal authenticated intranets or private dashboards closed to web crawlers"""

    seo_gate = """## Completion Gate & Verification
Before concluding SEO optimization:
- [ ] JSON-LD structured data validates against Google Rich Results Test
- [ ] Core Web Vitals meet targets (LCP $\\le 2.5\\text{s}$, INP $\\le 200\\text{ms}$, CLS $\\le 0.1$)
- [ ] Unique title and meta descriptions configured for all target routes"""
    polish_skill(skills_dir / "seo-optimizer", "seo-optimizer", seo_wtu, seo_gate)

    # 4. mobile-design
    mob_wtu = """## When to Use

### Use when:
- Designing mobile user interfaces for React Native, Flutter, iOS, or Android
- Ensuring touch target ergonomic compliance ($48 \\times 48\\text{dp}$ / $44 \\times 44\\text{pt}$)
- Implementing bottom navigation, gesture controls, and offline-first mobile sync

### Do not use when:
- Desktop-only admin consoles or terminal CLI applications"""

    mob_gate = """## Completion Gate & Verification
Before concluding mobile design review:
- [ ] All touch targets meet minimum $48\\text{dp}$ / $44\\text{pt}$ geometry
- [ ] Safe area insets handled across notches and gesture bars
- [ ] Offline state transitions verified with optimistic UI"""
    polish_skill(skills_dir / "mobile-design", "mobile-design", mob_wtu, mob_gate)

    # 5. ux-researcher-designer
    uxr_wtu = """## When to Use

### Use when:
- Planning usability testing protocols, user interviews, and field studies
- Calculating empirical usability metrics (System Usability Scale - SUS)
- Conducting heuristic evaluations against Nielsen Norman Group standards

### Do not use when:
- Writing low-level frontend code or implementing CSS styles directly"""

    uxr_gate = """## Completion Gate & Verification
Before concluding UX research study:
- [ ] SUS score calculated with sample size $\\ge 5$ users
- [ ] Usability friction points mapped with severity ratings (0 to 4)
- [ ] Actionable design recommendations presented to product team"""
    polish_skill(skills_dir / "ux-researcher-designer", "ux-researcher-designer", uxr_wtu, uxr_gate)

if __name__ == "__main__":
    main()
