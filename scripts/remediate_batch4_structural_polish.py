#!/usr/bin/env python3
"""
scripts/remediate_batch4_structural_polish.py — Polishes structural headings & gates for Batch 4 skills
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
    
    # 1. database-architecture
    da_wtu = """## When to Use

### Use when:
- Designing relational or NoSQL database schemas, entities, and relationships
- Optimizing indexing strategies ($S_{\\text{idx}} \\ge 0.15$), query performance, and connection pools
- Planning zero-downtime database migrations via the Expand-Contract pattern

### Do not use when:
- In-memory data structures or simple JSON file storage without database engine"""

    da_gate = """## Completion Gate & Verification
Before declaring database architecture change complete:
- [ ] Schema normalized to 3NF/BCNF (or documented de-normalization rationale)
- [ ] Index selectivity calculated and verified with `EXPLAIN ANALYZE`
- [ ] Idempotent migration with reversible rollback vector verified"""
    polish_skill(skills_dir / "database-architecture", "database-architecture", da_wtu, da_gate)

    # 2. security-review
    sec_wtu = """## When to Use

### Use when:
- Auditing source code and infrastructure for vulnerabilities against OWASP Top 10
- Conducting STRIDE threat modeling on new features, services, or APIs
- Verifying cryptographic configurations, input sanitization, and authorization rules

### Do not use when:
- Routine non-security stylistic code formatting reviews"""

    sec_gate = """## Completion Gate & Verification
Before concluding security review:
- [ ] All STRIDE threat vectors evaluated with mitigation strategies
- [ ] Zero hardcoded secrets, SQL injection vulnerabilities, or insecure deserialization
- [ ] CVSS v3.1 scores assigned to any identified vulnerabilities with remediation tickets"""
    polish_skill(skills_dir / "security-review", "security-review", sec_wtu, sec_gate)

    # 3. performance-optimization
    perf_wtu = """## When to Use

### Use when:
- Diagnosing latency bottlenecks, throughput limits, or high CPU/memory consumption
- Sizing concurrent thread/connection pools using Little's Law ($L = \\lambda W$)
- Optimizing Core Web Vitals (LCP, INP, CLS) and database query execution times

### Do not use when:
- Premature optimization of cold paths or trivial sub-millisecond routines"""

    perf_gate = """## Completion Gate & Verification
Before concluding performance optimization:
- [ ] Profiler baseline captured before and after changes
- [ ] Latency reduction verified under synthetic benchmark load
- [ ] Zero memory leaks or unbounded cache growth under stress test"""
    polish_skill(skills_dir / "performance-optimization", "performance-optimization", perf_wtu, perf_gate)

    # 4. deployment
    dep_wtu = """## When to Use

### Use when:
- Creating or updating CI/CD deployment pipelines, container definitions, and manifests
- Configuring Canary, Blue-Green, or Rolling update deployment strategies
- Establishing automated health check probes and metric-driven rollback thresholds

### Do not use when:
- Local development sandbox testing without deployment infrastructure"""

    dep_gate = """## Completion Gate & Verification
Before concluding deployment execution:
- [ ] Immutable build artifact verified with green automated test suite
- [ ] Liveness and Readiness probes configured and returning HTTP 200
- [ ] Automated rollback vector tested and verified"""
    polish_skill(skills_dir / "deployment", "deployment", dep_wtu, dep_gate)

    # 5. php-laravel-ecosystem
    php_wtu = """## When to Use

### Use when:
- Developing or refactoring applications within the modern PHP / Laravel ecosystem
- Implementing Pest v3 architectural tests, Laravel Pint styling, and Larastan Level 8+
- Designing Laravel Octane high-performance async workflows and Livewire components

### Do not use when:
- Non-PHP runtimes (Python, TypeScript, Go, Rust)"""

    php_gate = """## Completion Gate & Verification
Before concluding Laravel ecosystem implementation:
- [ ] Pest test suite passes with architectural expectations verified
- [ ] Laravel Pint formatting applied with zero style violations
- [ ] Larastan static analysis passes at Level 8"""
    polish_skill(skills_dir / "php-laravel-ecosystem", "php-laravel-ecosystem", php_wtu, php_gate)

if __name__ == "__main__":
    main()
