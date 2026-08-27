root = Path(__file__).resolve().parent.parent
skills_dir = root / "skills"
for skill_name, sota_text in BATCH_1_DATA.items():
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
    else:
        new_content = content + "\n\n" + sota_text.strip()
    
    skill_file.write_text(new_content, encoding="utf-8")
    print(f"[✓] Elevated Domain SOTA for: {skill_name}")


# SOTA-Engineering