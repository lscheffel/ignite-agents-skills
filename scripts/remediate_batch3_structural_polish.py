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