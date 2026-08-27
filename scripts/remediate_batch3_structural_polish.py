#!/usr/bin/env python3
"""
scripts/remediate_batch3_structural_polish.py — Polishes structural headings & gates for Batch 3 skills
"""

from pathlib import Path

def polish_skill(skill_path: Path, name: str, when_to_use_block: str, completion_gate_block: str):
    skill_file = skill_path / "SKILL.md"
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
    
    # 1. code-review
    cr_wtu = """## When to Use

### Use when:
- Conducting comprehensive code reviews on Pull Requests or feature branches
- Auditing code changes for security, performance, architecture, and correctness
- Providing structured feedback with severity classification (P1/P2/P3)

### Do not use when:
- Triage of micro-diffs under 50 lines (use `code-review-lite` instead)
- Automated linting that can be handled by standard CI linters (ESLint/Prettier)"""

    cr_gate = """## Completion Gate & Verification
Before concluding code review:
- [ ] All P1 Blockers resolved or blocking merge
- [ ] All P2 Major issues either resolved or recorded in Tech Debt Registry
- [ ] Test coverage verified with green CI build"""
    polish_skill(skills_dir / "code-review", "code-review", cr_wtu, cr_gate)

    # 2. code-review-workflow
    crw_wtu = """## When to Use

### Use when:
- Orchestrating multi-party review lifecycles and PR approvals
- Managing review SLAs, code owners, and consensus transitions
- Enforcing branch protection and merge gating rules

### Do not use when:
- Performing the individual code inspection itself (use `code-review` instead)
- Sole author committing directly to personal experimental branches"""

    crw_gate = """## Completion Gate & Verification
Before declaring review workflow complete:
- [ ] Required reviewer quorum satisfied with LGTM
- [ ] Clean branch rebase verified against upstream master
- [ ] Zero unresolved P1/P2 conversation threads"""
    polish_skill(skills_dir / "code-review-workflow", "code-review-workflow", crw_wtu, crw_gate)

    # 3. systematic-debugging
    sd_wtu = """## When to Use

### Use when:
- Investigating non-trivial bugs, crashes, race conditions, or test regressions
- Executing root cause analysis (RCA) on production incidents
- Bisecting historical regressions across large commit ranges

### Do not use when:
- Trivial syntax errors or typos with obvious compiler error messages
- Routine feature development without an active defect or anomaly"""

    sd_gate = """## Completion Gate & Verification
Before concluding debugging investigation:
- [ ] Minimal reproduction script created and verified failing
- [ ] Root cause verified through falsifiable hypothesis testing
- [ ] Fix applied and permanent regression test passes with green build"""
    polish_skill(skills_dir / "systematic-debugging", "systematic-debugging", sd_wtu, sd_gate)

    # 4. clean-code
    cc_wtu = """## When to Use

### Use when:
- Writing new code or reviewing existing code against SOLID and Clean Code standards
- Reducing cognitive and cyclomatic complexity ($CC \\le 10$)
- Standardizing naming conventions, function hygiene, and error handling

### Do not use when:
- Low-level kernel drivers or extreme performance-critical inner loops where abstraction is prohibited"""

    cc_gate = """## Completion Gate & Verification
Before concluding Clean Code audit:
- [ ] Cyclomatic complexity verified $\\le 10$ per function
- [ ] Zero magic literals or undocumented constants
- [ ] Single Level of Abstraction Principle (SLAP) respected"""
    polish_skill(skills_dir / "clean-code", "clean-code", cc_wtu, cc_gate)

    # 5. test-driven-development
    tdd_wtu = """## When to Use

### Use when:
- Implementing any new feature, algorithm, domain logic, or bugfix
- Enforcing strict RED-GREEN-REFACTOR cycles with rapid feedback
- Building high-confidence test suites with high mutation scores ($MS \\ge 0.85$)

### Do not use when:
- Throwaway visual spike prototypes where code will be discarded entirely"""

    tdd_gate = """## Completion Gate & Verification
Before concluding TDD cycle:
- [ ] Red phase test failure verified before production code written
- [ ] Green phase test pass verified with minimal code
- [ ] Refactor phase completed with all tests remaining green"""
    polish_skill(skills_dir / "test-driven-development", "test-driven-development", tdd_wtu, tdd_gate)

if __name__ == "__main__":
    main()
