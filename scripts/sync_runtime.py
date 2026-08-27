#!/usr/bin/env python3
"""
sync_runtime.py — SOTA Multi-Target Runtime Synchronizer & Zombie Purger

Performs atomic mirror synchronization of the canonical 60 skills from
`ignite-agents-skills/skills/` into all known local agent runtime directories,
while aggressively pruning stale, orphan, or unmanaged skill directories.

Supported Targets:
  1. Antigravity IDE / Gemini CLI : ~/.gemini/config/skills
  2. Kilo Code Cache Extension   : ~/.cache/kilo/skills
  3. Kilo Code Global Hub        : ~/.kilo/skills
  4. Agent Skills Standard Root  : ~/.agents/skills
  5. GitHub Copilot Skills       : ~/.copilot/skills
  6. Alibaba Tongyi Lingma       : ~/.lingma/skills
  7. Cursor AI Skills            : ~/.cursor/skills
  8. Codeium Windsurf Skills     : ~/.windsurf/skills
  9. Continue.dev Prompts/Skills : ~/.continue/skills
 10. Claude Code / Anthropic     : ~/.claude/skills
 11. OpenCode / Codex            : ~/.opencode/skills

Usage:
  python3 scripts/sync_runtime.py --status
  python3 scripts/sync_runtime.py --deploy
  python3 scripts/sync_runtime.py --purge-stale
  python3 scripts/sync_runtime.py --json
"""

import argparse
import hashlib
import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

# ─── Configuration & Paths ───────────────────────────────────────────────────

REPO_ROOT = Path(__file__).resolve().parent.parent
CANONICAL_SKILLS_DIR = REPO_ROOT / "skills"
INDEX_JSON_PATH = CANONICAL_SKILLS_DIR / "index.json"
HOME = Path.home()

# Target Runtime Registry with priority and behavior
RUNTIME_TARGETS = [
    {
        "id": "antigravity",
        "name": "Antigravity IDE / Gemini CLI (SSOT)",
        "path": HOME / ".gemini" / "config" / "skills",
        "type": "primary",
        "auto_sync": True,
        "prune_orphans": True,
    },
    {
        "id": "kilo_cache",
        "name": "Kilo Code Extension Cache",
        "path": HOME / ".cache" / "kilo" / "skills",
        "type": "secondary",
        "auto_sync": True,
        "prune_orphans": True,
    },
    {
        "id": "kilo_global",
        "name": "Kilo Code Global Root",
        "path": HOME / ".kilo" / "skills",
        "type": "secondary",
        "auto_sync": True,
        "prune_orphans": True,
    },
    {
        "id": "agents_std",
        "name": "Agent Skills Standard Root",
        "path": HOME / ".agents" / "skills",
        "type": "secondary",
        "auto_sync": True,
        "prune_orphans": True,
    },
    {
        "id": "copilot",
        "name": "GitHub Copilot Skills Hub",
        "path": HOME / ".copilot" / "skills",
        "type": "secondary",
        "auto_sync": True,
        "prune_orphans": True,
    },
    {
        "id": "lingma",
        "name": "Tongyi Lingma Skills Hub",
        "path": HOME / ".lingma" / "skills",
        "type": "secondary",
        "auto_sync": True,
        "prune_orphans": True,
    },
    {
        "id": "cursor",
        "name": "Cursor AI Skills Store",
        "path": HOME / ".cursor" / "skills",
        "type": "secondary",
        "auto_sync": False,  # Only if directory already exists
        "prune_orphans": True,
    },
    {
        "id": "windsurf",
        "name": "Codeium Windsurf Skills",
        "path": HOME / ".windsurf" / "skills",
        "type": "secondary",
        "auto_sync": False,
        "prune_orphans": True,
    },
    {
        "id": "continue",
        "name": "Continue.dev Prompts & Skills",
        "path": HOME / ".continue" / "skills",
        "type": "secondary",
        "auto_sync": False,
        "prune_orphans": True,
    },
    {
        "id": "claude",
        "name": "Claude Code Skills Hub",
        "path": HOME / ".claude" / "skills",
        "type": "secondary",
        "auto_sync": False,
        "prune_orphans": True,
    },
    {
        "id": "opencode",
        "name": "OpenCode / Codex Skills Hub",
        "path": HOME / ".opencode" / "skills",
        "type": "secondary",
        "auto_sync": False,
        "prune_orphans": True,
    },
]


# ─── Helper Functions ────────────────────────────────────────────────────────

def get_canonical_skills():
    """Returns a dict of {skill_name: Path} for all canonical skills with SKILL.md."""
    if not CANONICAL_SKILLS_DIR.exists():
        return {}
    skills = {}
    for d in sorted(CANONICAL_SKILLS_DIR.iterdir()):
        if d.is_dir() and (d / "SKILL.md").exists():
            skills[d.name] = d
    return skills


def compute_dir_sha256(dir_path: Path) -> str:
    """Computes a deterministic hash of all files inside a directory."""
    if not dir_path.exists():
        return ""
    hasher = hashlib.sha256()
    for root, _, files in os.walk(dir_path):
        for file in sorted(files):
            file_path = Path(root) / file
            try:
                hasher.update(file.encode("utf-8"))
                hasher.update(file_path.read_bytes())
            except Exception:
                pass
    return hasher.hexdigest()[:16]


def atomic_copy_tree(src: Path, dst: Path):
    """Atomically copies src directory to dst, replacing destination cleanly."""
    temp_dst = dst.parent / f".tmp_{dst.name}_{os.getpid()}"
    if temp_dst.exists():
        shutil.rmtree(temp_dst)
    shutil.copytree(src, temp_dst, symlinks=True, ignore=shutil.ignore_patterns("*.pyc", "__pycache__", ".git*"))
    if dst.exists():
        if dst.is_dir() and not dst.is_symlink():
            shutil.rmtree(dst)
        else:
            dst.unlink()
    temp_dst.rename(dst)


# ─── Core Audit & Synchronization Engine ─────────────────────────────────────

def audit_runtime_targets(canonical_skills: dict) -> list:
    """Inspects all runtime targets, detecting active skills, orphans and drift."""
    results = []
    canonical_names = set(canonical_skills.keys())

    for target in RUNTIME_TARGETS:
        tpath: Path = target["path"]
        exists = tpath.exists()
        active_skills = set()
        orphan_items = set()

        if exists and tpath.is_dir():
            for item in tpath.iterdir():
                if item.name in canonical_names and (item / "SKILL.md").exists():
                    active_skills.add(item.name)
                else:
                    orphan_items.add(item.name)

        missing_skills = canonical_names - active_skills
        status = "NOT_INSTALLED"
        if exists:
            if orphan_items:
                status = "ORPHANS_FOUND"
            elif len(missing_skills) == 0:
                status = "SYNCED"
            elif len(active_skills) > 0:
                status = "PARTIAL_DRIFT"
            else:
                status = "EMPTY"

        results.append({
            "id": target["id"],
            "name": target["name"],
            "path": str(tpath),
            "type": target["type"],
            "exists": exists,
            "status": status,
            "active_count": len(active_skills),
            "orphan_count": len(orphan_items),
            "missing_count": len(missing_skills),
            "orphans": sorted(list(orphan_items)),
            "auto_sync": target["auto_sync"] or exists,
        })
    return results


def execute_sync_and_purge(canonical_skills: dict, prune_all_orphans: bool = True, targets_to_sync: list = None):
    """Executes atomic mirror deployment and aggressive pruning across runtime targets."""
    print("🚀 [Ignite Runtime Engine] Iniciando Deploy & Sincronização Atômica Multi-Target...\n")
    print(f"📦 Fonte Canônica: {CANONICAL_SKILLS_DIR} ({len(canonical_skills)} skills SOTA)\n")

    synced_targets = 0
    total_copied = 0
    total_pruned = 0

    for target in RUNTIME_TARGETS:
        tpath: Path = target["path"]
        should_sync = target["auto_sync"] or tpath.exists()
        if targets_to_sync and target["id"] not in targets_to_sync:
            continue

        if not should_sync and not tpath.exists():
            continue

        print(f"📁 Target: {target['name']}")
        print(f"   Path: {tpath}")

        # Ensure parent directory exists
        tpath.mkdir(parents=True, exist_ok=True)

        # 1. Prune orphans and non-canonical entries
        existing_items = list(tpath.iterdir())
        pruned_here = 0
        for item in existing_items:
            if item.name not in canonical_skills:
                try:
                    if item.is_dir() and not item.is_symlink():
                        shutil.rmtree(item)
                    else:
                        item.unlink()
                    print(f"   🗑️  [PURGED ORPHAN] {item.name}")
                    pruned_here += 1
                except Exception as e:
                    print(f"   ⚠️  Falha ao remover {item.name}: {e}")

        # 2. Atomic copy of canonical skills
        copied_here = 0
        for skill_name, src_dir in canonical_skills.items():
            dest_skill_dir = tpath / skill_name
            try:
                atomic_copy_tree(src_dir, dest_skill_dir)
                copied_here += 1
            except Exception as e:
                print(f"   ❌ Erro ao sincronizar {skill_name}: {e}")

        print(f"   ✅ Sincronizadas {copied_here}/{len(canonical_skills)} skills | {pruned_here} órfãos removidos.\n")
        synced_targets += 1
        total_copied += copied_here
        total_pruned += pruned_here

    print("═════════════════════════════════════════════════════════════════════════")
    print(f"🎉 Deploy Concluído: {synced_targets} Targets Sincronizados")
    print(f"📦 Total de Cópia Atômica: {total_copied} skills")
    print(f"🧹 Total de Zumbis Excluídos: {total_pruned} órfãos eliminados")
    print("═════════════════════════════════════════════════════════════════════════\n")


# ─── CLI Entrypoint ──────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="SOTA Multi-Target Runtime Synchronizer & Zombie Purger for Agent Skills"
    )
    parser.add_argument("--status", action="store_true", help="Exibe relatório de auditoria de todos os runtimes")
    parser.add_argument("--deploy", action="store_true", help="Executa deploy e sincronização atômica completa")
    parser.add_argument("--purge", action="store_true", help="Purga todas as pastas órfãs e zumbis")
    parser.add_argument("--target", type=str, help="ID específico do target para sincronizar (ex: antigravity, kilo_cache)")
    parser.add_argument("--json", action="store_true", help="Retorna saída estruturada em JSON")

    args = parser.parse_args()
    canonical_skills = get_canonical_skills()

    if len(canonical_skills) == 0:
        print("❌ ERRO: Nenhuma skill canônica encontrada em skills/", file=sys.stderr)
        sys.exit(1)

    # Default to status if no specific action provided
    if not args.deploy and not args.purge and not args.json:
        args.status = True

    if args.status:
        audit = audit_runtime_targets(canonical_skills)
        print("╔══════════════════════════════════════════════════════════════════════════════════════════╗")
        print("║                AGENT RUNTIME ECOSYSTEM AUDIT & DRIFT STATUS REPORT                       ║")
        print("╠══════════════════════════════════════════════════════════════════════════════════════════╣")
        print(f"║ SSOT Canônica : {CANONICAL_SKILLS_DIR} ({len(canonical_skills)} skills)                       ║")
        print("╠══════════════════════════════════════════════════════════════════════════════════════════╣")
        print(f"║ {'Runtime Name':<32} │ {'Status':<15} │ {'Active':<7} │ {'Orphans':<8} ║")
        print("╟──────────────────────────────────┼─────────────────┼─────────┼──────────╢")
        for r in audit:
            badge = "✅ SYNCED" if r["status"] == "SYNCED" else ("⚠️  " + r["status"])
            print(f"║ {r['name'][:32]:<32} │ {badge:<15} │ {r['active_count']:<7} │ {r['orphan_count']:<8} ║")
        print("╚══════════════════════════════════════════════════════════════════════════════════════════╝\n")

    if args.deploy or args.purge:
        targets = [args.target] if args.target else None
        execute_sync_and_purge(canonical_skills, prune_all_orphans=True, targets_to_sync=targets)

    if args.json:
        audit = audit_runtime_targets(canonical_skills)
        print(json.dumps({
            "timestamp": datetime.now().isoformat(),
            "canonical_count": len(canonical_skills),
            "runtimes": audit
        }, indent=2))


if __name__ == "__main__":
    main()
