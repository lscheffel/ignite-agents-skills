for skill_dir in sorted(skills_dir.iterdir()):
    if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
        elevate_skill(skill_dir)