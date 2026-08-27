#!/usr/bin/env python3
"""
scripts/remediate_batch7_structural_polish.py — Polishes structural headings & gates for Batch 7 skills
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
    
    # 1. writing-skills
    ws_wtu = """## When to Use

### Use when:
- Authoring, editing, or refactoring skills according to the Agent Skills Standard (v1.0.0)
- Defining typed YAML frontmatter (`name`, `description`, `version`, `tags`, `related_skills`)
- Applying progressive disclosure architecture to keep `SKILL.md` instruction-dense ($\le 4,000$ tokens)

### Do not use when:
- Writing general prose, marketing copy, or technical documentation outside the skills ecosystem"""

    ws_gate = """## Completion Gate & Verification
Before declaring skill authoring complete:
- [ ] Frontmatter validates against Agent Skills specification schema
- [ ] Token count of `SKILL.md` is within $\le 4,000$ token ceiling
- [ ] Concrete `When to Use` and `Completion Gate` sections present"""
    polish_skill(skills_dir / "writing-skills", "writing-skills", ws_wtu, ws_gate)

    # 2. find-skills
    fs_wtu = """## When to Use

### Use when:
- Searching the local skill registry for matching tools and workflows via keyword or tags
- Executing instant SQLite FTS5 BM25 queries over the skills catalog
- Finding related companion skills for complex multi-agent workflows

### Do not use when:
- High-level abstract task routing across unstructured natural language queries (use `skill-discovery`)"""

    fs_gate = """## Completion Gate & Verification
Before concluding skill search:
- [ ] Relevant skills retrieved with name, version, and concise summary
- [ ] Sub-millisecond lookup latency achieved via local SQLite index
- [ ] Exact match or fuzzy match fallback clearly identified"""
    polish_skill(skills_dir / "find-skills", "find-skills", fs_wtu, fs_gate)

    # 3. verification-before-completion
    vbc_wtu = """## When to Use

### Use when:
- Concluding any technical task, bug fix, refactoring, or feature implementation
- Executing automated test suites and validation scripts before declaring completion
- Generating cryptographic Evidence Records (ER) and verification logs

### Do not use when:
- Exploratory brainstorming or early-stage conceptual research"""

    vbc_gate = """## Completion Gate & Verification
Before declaring task completed:
- [ ] All automated unit and integration tests execute with exit code 0
- [ ] Terminal output evidence captured and verified
- [ ] Git working tree verified clean without unintended modified files"""
    polish_skill(skills_dir / "verification-before-completion", "verification-before-completion", vbc_wtu, vbc_gate)

    # 4. git-workflow
    gw_wtu = """## When to Use

### Use when:
- Managing git branches, commit histories, and pull requests under Trunk-Based Development
- Crafting Conventional Commits (v1.0.0) with clean scope formatting
- Performing interactive rebases and synchronizing feature branches with trunk

### Do not use when:
- Non-git version control systems or direct production hotfixes bypassing review"""

    gw_gate = """## Completion Gate & Verification
Before concluding git operation:
- [ ] Branch life cycle kept $\le 24\text{h}$ under Trunk-Based Development
- [ ] Commits formatted cleanly according to Conventional Commits standard
- [ ] Branch rebases cleanly onto latest trunk with zero merge conflicts"""
    polish_skill(skills_dir / "git-workflow", "git-workflow", gw_wtu, gw_gate)

    # 5. release
    rel_wtu = """## When to Use

### Use when:
- Tagging and publishing production releases according to Semantic Versioning (SemVer 2.0.0)
- Generating cryptographically signed artifacts with SLSA Level 3 provenance
- Creating GitHub Releases with automated checksum manifests (`SHA256SUMS`)

### Do not use when:
- Local experimental development or unverified scratch builds"""

    rel_gate = """## Completion Gate & Verification
Before concluding release pipeline:
- [ ] Git release tag signed and immutable
- [ ] Full test suite verified green across all CI runners
- [ ] SHA-256 checksum manifest generated and published"""
    polish_skill(skills_dir / "release", "release", rel_wtu, rel_gate)

if __name__ == "__main__":
    main()
