#!/usr/bin/env python3
"""
SOTA Continuous Skill Audit Ledger Engine
Discovers all repository skills and maintains a persistent audit ledger in docs/audit/skills/
"""

import argparse
import datetime
import json
import os
import re
import sys
from pathlib import Path


def find_repo_root(start_path: Path) -> Path:
    """Finds repository root by searching for .git or AGENTS.md."""
    current = start_path.resolve()
    for parent in [current] + list(current.parents):
        if (parent / ".git").exists() or (parent / "AGENTS.md").exists():
            return parent
    return start_path.resolve()


def discover_all_skills(repo_root: Path) -> dict:
    """Discovers all skills in the repository from SKILL.md files."""
    skills = {}
    
    # Search patterns
    patterns = [
        "skills/*/SKILL.md",
        "*/SKILL.md",
        "plugins/*/skills/*/SKILL.md",
        "builtin/*/skills/*/SKILL.md",
    ]
    
    for pattern in patterns:
        for skill_md in repo_root.glob(pattern):
            # Skip templates or tests
            if "template" in str(skill_md).lower() or ".test" in str(skill_md).lower():
                continue
            
            try:
                content = skill_md.read_text(encoding="utf-8")
                match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
                if match:
                    frontmatter = match.group(1)
                    name_match = re.search(r"name:\s*(.+)", frontmatter)
                    ver_match = re.search(r"version:\s*(.+)", frontmatter)
                    
                    skill_name = name_match.group(1).strip().strip("'\"") if name_match else skill_md.parent.name
                    version = ver_match.group(1).strip().strip("'\"") if ver_match else "1.0.0"
                    
                    rel_path = skill_md.parent.relative_to(repo_root)
                    skills[skill_name] = {
                        "name": skill_name,
                        "path": str(rel_path),
                        "version": version,
                    }
            except Exception as e:
                print(f"[!] Warning parsing {skill_md}: {e}", file=sys.stderr)
                
    return skills


def load_ledger(ledger_json_path: Path) -> dict:
    """Loads existing ledger JSON or returns empty template."""
    if ledger_json_path.exists():
        try:
            return json.loads(ledger_json_path.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "version": "1.0.0",
        "last_updated": None,
        "total_skills": 0,
        "audited_skills": 0,
        "pending_skills": 0,
        "average_score": 0.0,
        "entries": {}
    }


def update_ledger(
    repo_root: Path,
    target_skill: str = None,
    version: str = None,
    grade: str = None,
    score: float = None,
    physical_score: float = None,
    cognitive_score: float = None,
    action: str = None
):
    target_dir = repo_root / "docs" / "audit" / "skills"
    target_dir.mkdir(parents=True, exist_ok=True)
    
    ledger_json_path = target_dir / "SKILL_AUDIT_LEDGER.json"
    ledger_md_path = target_dir / "SKILL_AUDIT_LEDGER.md"
    
    discovered_skills = discover_all_skills(repo_root)
    ledger_data = load_ledger(ledger_json_path)
    entries = ledger_data.get("entries", {})
    
    # 1. Synchronize discovered skills into entries
    for s_name, s_info in sorted(discovered_skills.items()):
        if s_name not in entries:
            entries[s_name] = {
                "skill": s_name,
                "path": s_info["path"],
                "version": s_info["version"],
                "last_audited": None,
                "grade": "PENDING",
                "previous_score": "N/A",
                "current_score": "N/A",
                "physical_score": "N/A",
                "cognitive_score": "N/A",
                "status": "PENDING_AUDIT",
                "action": "PENDING_AUDIT"
            }
        else:
            # Update path and version if changed
            entries[s_name]["path"] = s_info["path"]
            if not target_skill or target_skill != s_name:
                entries[s_name]["version"] = s_info["version"]
                
    # Remove entries that no longer exist
    for existing_name in list(entries.keys()):
        if existing_name not in discovered_skills:
            del entries[existing_name]

    # 1.5 Scan docs/audit/skills/*_audit_bulletin.md to auto-populate from existing bulletins
    now_str = datetime.date.today().isoformat()
    for bfile in target_dir.glob("*_audit_bulletin.md"):
        bname = bfile.stem.replace("_audit_bulletin", "")
        if bname in entries:
            try:
                btext = bfile.read_text(encoding="utf-8")
                m_grade = re.search(r"\*\*Overall Grade:\*\*\s*\*\*([SABCDFPENDING\+]+)", btext)
                m_score = re.search(r"\*\*Combined 2D Score\*\*\s*\|\s*\*\*([\d\.]+)", btext)
                if not m_score:
                    m_score = re.search(r"\*\*Overall Grade:\*\*.*?([\d\.]+)\s*/\s*100", btext)
                m_phys = re.search(r"\*\*Axis 1: Physical Structural & Governance\*\*\s*\|\s*\*\*([\d\.]+)", btext)
                m_cogn = re.search(r"\*\*Axis 2: Domain SOTA & Cognitive Efficacy\*\*\s*\|\s*\*\*([\d\.]+)", btext)
                m_action = re.search(r"\*\*Recommended Action:\*\*\s*\*\*([^\*\n]+)\*\*", btext)
                m_date = re.search(r"\*\*Audit Date:\*\*\s*(\d{4}-\d{2}-\d{2})", btext)

                if m_score:
                    grade_val = m_grade.group(1).strip() if m_grade else "A"
                    score_val = float(m_score.group(1))
                    phys_val = float(m_phys.group(1)) if m_phys else score_val
                    cogn_val = float(m_cogn.group(1)) if m_cogn else score_val
                    action_val = m_action.group(1).strip() if m_action else "ADOPT_AS_IS"
                    date_val = m_date.group(1) if m_date else now_str

                    entries[bname]["grade"] = grade_val
                    entries[bname]["current_score"] = score_val
                    entries[bname]["physical_score"] = phys_val
                    entries[bname]["cognitive_score"] = cogn_val
                    entries[bname]["action"] = action_val
                    entries[bname]["status"] = action_val
                    entries[bname]["last_audited"] = date_val
            except Exception as e:
                pass
            
    # 2. If a specific skill audit is passed, update its record
    if target_skill:
        s_entry = entries.get(target_skill)
        if not s_entry:
            s_entry = {
                "skill": target_skill,
                "path": str(target_skill),
                "version": version or "1.0.0",
                "last_audited": now_str,
                "grade": grade or "A",
                "previous_score": "N/A",
                "current_score": score or 0.0,
                "physical_score": physical_score or score or 0.0,
                "cognitive_score": cognitive_score or score or 0.0,
                "status": action or "ADOPT_AS_IS",
                "action": action or "ADOPT_AS_IS"
            }
            entries[target_skill] = s_entry
        else:
            # Shift current score to previous score
            prev = s_entry.get("current_score")
            if prev != "N/A" and prev is not None:
                s_entry["previous_score"] = prev
            if version:
                s_entry["version"] = version
            s_entry["last_audited"] = now_str
            if grade:
                s_entry["grade"] = grade
            if score is not None:
                s_entry["current_score"] = score
            if physical_score is not None:
                s_entry["physical_score"] = physical_score
            if cognitive_score is not None:
                s_entry["cognitive_score"] = cognitive_score
            if action:
                s_entry["action"] = action
                s_entry["status"] = action

    # 3. Compute Summary Statistics
    total_skills = len(entries)
    audited_entries = [e for e in entries.values() if e.get("current_score") != "N/A"]
    audited_count = len(audited_entries)
    pending_count = total_skills - audited_count
    avg_score = (
        sum(float(e["current_score"]) for e in audited_entries) / audited_count
        if audited_count > 0 else 0.0
    )
    
    ledger_data["version"] = "1.0.0"
    ledger_data["last_updated"] = now_str
    ledger_data["total_skills"] = total_skills
    ledger_data["audited_skills"] = audited_count
    ledger_data["pending_skills"] = pending_count
    ledger_data["average_score"] = round(avg_score, 1)
    ledger_data["entries"] = entries
    
    # 4. Write JSON Ledger
    ledger_json_path.write_text(json.dumps(ledger_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    
    # 5. Write Markdown Ledger
    md_lines = [
        "# Continuous Skill Audit Ledger",
        "",
        f"> **Last Synchronized:** {now_str} | **Audited:** {audited_count}/{total_skills} Skills | **Average Score:** {round(avg_score, 1)}/100",
        "",
        "## Summary Metrics",
        "",
        f"- **Total Catalog Skills:** {total_skills}",
        f"- **Audited Skills:** {audited_count} ({(audited_count/total_skills*100):.1f}%)" if total_skills else "- **Audited Skills:** 0",
        f"- **Pending Audits:** {pending_count}",
        f"- **Average Quality Score:** {round(avg_score, 1)} / 100",
        "",
        "## Master Audit Ledger",
        "",
        "| Skill | Version | Audited Date | Grade | Prev Score | Curr Score | Physical | Cognitive | Status / Action |",
        "|---|---|:---:|:---:|:---:|:---:|:---:|:---:|---|"
    ]
    
    for s_name, item in sorted(entries.items(), key=lambda x: (x[1].get("current_score") == "N/A", x[0])):
        c_score = f"{item['current_score']}/100" if item['current_score'] != 'N/A' else "N/A"
        p_score = f"{item['previous_score']}/100" if item['previous_score'] != 'N/A' else "N/A"
        phys = f"{item['physical_score']}/100" if item['physical_score'] != 'N/A' else "N/A"
        cogn = f"{item['cognitive_score']}/100" if item['cognitive_score'] != 'N/A' else "N/A"
        grade_badge = f"**{item['grade']}**" if item['grade'] != "PENDING" else "PENDING"
        
        md_lines.append(
            f"| [`{s_name}`](../../../{item['path']}) | `{item['version']}` | {item['last_audited'] or '—'} | {grade_badge} | {p_score} | **{c_score}** | {phys} | {cogn} | {item['action']} |"
        )
        
    md_lines.append("")
    ledger_md_path.write_text("\n".join(md_lines), encoding="utf-8")
    
    print(f"[✓] Skill Audit Ledger updated: {ledger_md_path}")
    print(f"[✓] JSON Ledger persisted: {ledger_json_path}")
    print(f"[*] Total Skills: {total_skills} | Audited: {audited_count} | Pending: {pending_count} | Average Score: {round(avg_score, 1)}")


def main():
    parser = argparse.ArgumentParser(description="Update Continuous Skill Audit Ledger")
    parser.add_argument("--skill", help="Name of the audited skill")
    parser.add_argument("--version", help="Version of the audited skill")
    parser.add_argument("--grade", help="Audit Grade (A+, A, B, C, F)")
    parser.add_argument("--score", type=float, help="Current aggregate score (0-100)")
    parser.add_argument("--physical-score", type=float, help="Physical structural score (0-100)")
    parser.add_argument("--cognitive-score", type=float, help="Cognitive domain SOTA score (0-100)")
    parser.add_argument("--action", help="Action / Verdict (ADOPT_AS_IS, HOTFIX, REFACTOR, etc.)")
    parser.add_argument("--repo-root", help="Path to repository root")
    parser.add_argument("--sync-all", action="store_true", help="Sync all skills from repository root")
    
    args = parser.parse_args()
    
    repo_root = Path(args.repo_root) if args.repo_root else find_repo_root(Path.cwd())
    
    update_ledger(
        repo_root=repo_root,
        target_skill=args.skill,
        version=args.version,
        grade=args.grade,
        score=args.score,
        physical_score=args.physical_score,
        cognitive_score=args.cognitive_score,
        action=args.action
    )


if __name__ == "__main__":
    main()
