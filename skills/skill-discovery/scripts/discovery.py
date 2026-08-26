"""Skill discovery utility - scans and validates skill bundles across the ecosystem.

Provides the `scan_skills()` function to discover and catalog registered skills,
including their metadata, templates, and structural compliance.
"""

import os
import sys
import json
import re
import yaml

SKILLS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

DOMAINS = [
    "core-governance",
    "engineering-quality",
    "architecture-systems",
    "agentic-workflow",
    "frontend-ux",
    "domain-stack"
]

def scan_skills():
    skills = {}
    if not os.path.exists(SKILLS_DIR):
        return skills

    for s_name in sorted(os.listdir(SKILLS_DIR)):
        s_dir = os.path.join(SKILLS_DIR, s_name)
        if not os.path.isdir(s_dir):
            continue
        skill_md = os.path.join(s_dir, "SKILL.md")
        if not os.path.isfile(skill_md):
            continue

        try:
            with open(skill_md, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()

            fm_match = re.search(r'^---\s*\r?\n(.*?)\r?\n---', content, re.DOTALL)
            fm_data = {}
            if fm_match:
                fm_data = yaml.safe_load(fm_match.group(1)) or {}

            skills[s_name] = {
                "name": fm_data.get("name", s_name),
                "version": fm_data.get("version", "1.0.0"),
                "description": fm_data.get("description", ""),
                "domain": fm_data.get("domain", "domain-stack"),
                "triggers": fm_data.get("triggers", [s_name]),
                "tags": fm_data.get("tags", []),
                "metadata": fm_data.get("metadata", {}),
                "path": skill_md
            }
        except Exception as e:
            skills[s_name] = {
                "name": s_name,
                "error": str(e),
                "path": skill_md
            }

    return skills

def cmd_catalog():
    skills = scan_skills()
    print(json.dumps(skills, indent=2, ensure_ascii=False))

def cmd_list():
    skills = scan_skills()
    grouped = {d: [] for d in DOMAINS}
    grouped["other"] = []

    for name, data in skills.items():
        domain = data.get("domain", "domain-stack")
        if domain in grouped:
            grouped[domain].append(name)
        else:
            grouped["other"].append(name)

    print("================================================================================")
    print("                      CANONICAL SKILLS INDEX BY DOMAIN                          ")
    print("================================================================================")
    for domain in DOMAINS:
        items = grouped[domain]
        print(f"\n📂 [{domain.upper()}] ({len(items)} skills):")
        for item in sorted(items):
            print(f"  • {item}")
    
    if grouped["other"]:
        print(f"\n📂 [OTHER / SPECIALIZED] ({len(grouped['other'])} skills):")
        for item in sorted(grouped["other"]):
            print(f"  • {item}")

def cmd_explain(skill_name):
    skills = scan_skills()
    if skill_name not in skills:
        print(f"❌ Skill '{skill_name}' not found in repository.")
        sys.exit(1)

    data = skills[skill_name]
    print(f"================================================================================")
    print(f" SKILL: {data.get('name')} (v{data.get('version')})")
    print(f"================================================================================")
    print(f"Domain:      {data.get('domain')}")
    print(f"Description: {data.get('description')}")
    print(f"Triggers:    {', '.join(data.get('triggers', []))}")
    print(f"Tags:        {', '.join(data.get('tags', []))}")
    print(f"Metadata:    {data.get('metadata')}")
    print(f"Path:        {data.get('path')}")

def cmd_validate():
    errors = []
    warnings = []
    valid_count = 0

    if not os.path.exists(SKILLS_DIR):
        print("❌ Skills directory not found.")
        sys.exit(1)

    for s_name in sorted(os.listdir(SKILLS_DIR)):
        s_dir = os.path.join(SKILLS_DIR, s_name)
        if not os.path.isdir(s_dir):
            continue

        skill_md = os.path.join(s_dir, "SKILL.md")
        if not os.path.isfile(skill_md):
            errors.append(f"[{s_name}] SKILL.md missing")
            continue

        with open(skill_md, "rb") as f:
            raw = f.read()

        if b"\r\n" in raw:
            warnings.append(f"[{s_name}] CRLF line endings detected")

        text = raw.decode("utf-8", errors="replace")

        if re.search(r'[\u4e00-\u9fff]', text):
            errors.append(f"[{s_name}] CJK character corruption detected")

        fm_match = re.search(r'^---\s*\r?\n(.*?)\r?\n---', text, re.DOTALL)
        if not fm_match:
            errors.append(f"[{s_name}] Missing YAML frontmatter")
            continue

        fm_text = fm_match.group(1)

        if re.search(r'^\s*\*\s+\w+', fm_text, re.MULTILINE):
            errors.append(f"[{s_name}] Invalid YAML list syntax (* instead of -)")

        try:
            data = yaml.safe_load(fm_text)
            if not isinstance(data, dict):
                errors.append(f"[{s_name}] Frontmatter is not a YAML dictionary")
            else:
                for req in ["name", "version", "description", "domain", "triggers"]:
                    if req not in data:
                        errors.append(f"[{s_name}] Missing mandatory field: '{req}'")
                valid_count += 1
        except Exception as e:
            errors.append(f"[{s_name}] YAML parsing error: {str(e)}")

    print("\n================================================================================")
    print("                       SKILL-DISCOVERY VALIDATION REPORT                        ")
    print("================================================================================")
    print(f"Total Skills Checked: {valid_count + len(errors)}")
    print(f"Valid Skills:         {valid_count}")
    print(f"Errors Found:         {len(errors)}")
    print(f"Warnings:             {len(warnings)}")

    if errors:
        print("\n❌ ERRORS:")
        for err in errors:
            print(f"  • {err}")
    if warnings:
        print("\n⚠️ WARNINGS:")
        for w in warnings:
            print(f"  • {w}")

    if errors:
        sys.exit(1)
    else:
        print("\n✅ ALL SKILLS PASSED GOVERNANCE & SCHEMA VALIDATION!")

def main():
    if len(sys.argv) < 2:
        print("Usage: python discovery.py <catalog|list|validate|explain <skill_name>>")
        sys.exit(1)

    cmd = sys.argv[1].lower()
    if cmd == "catalog":
        cmd_catalog()
    elif cmd == "list":
        cmd_list()
    elif cmd == "validate":
        cmd_validate()
    elif cmd == "explain":
        if len(sys.argv) < 3:
            print("Usage: python discovery.py explain <skill_name>")
            sys.exit(1)
        cmd_explain(sys.argv[2])
    else:
        print(f"Unknown command '{cmd}'. Available commands: catalog, list, validate, explain")
        sys.exit(1)

if __name__ == "__main__":
    main()
