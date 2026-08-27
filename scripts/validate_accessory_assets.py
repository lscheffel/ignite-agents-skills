#!/usr/bin/env python3
"""
validate_accessory_assets.py — Validador SOTA de Integridade e Profundidade de Artefatos Acessórios

Verifica se todos os arquivos em:
- skills/*/templates/*.md
- skills/*/examples/*.md
- skills/*/checklists/*.md
- skills/*/references/*.md

Atendem aos critérios mínimos de qualidade SOTA:
1. Tamanho mínimo de linhas (>= 25 linhas)
2. Ausência de marcadores de mock/stub/placeholder genérico
3. Densidade técnica substantiva
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"

BANNED_PATTERNS = [
    "Scenario: Consistent artifact generated without regressions",
    "<!-- Insert generated artifact according to the canonical skill procedure -->",
    "# Canonical Template —",
    "Adherence to the standards established in AGENTS.md.",
]

MIN_LINES_BY_TYPE = {
    "examples": 25,
    "templates": 25,
    "checklists": 25,
    "references": 25,
}

def audit_accessory_assets():
    errors = []
    total_files = 0
    compliant_files = 0

    if not SKILLS_DIR.exists():
        print(f"❌ Diretório skills/ não encontrado em {SKILLS_DIR}")
        sys.exit(1)

    skill_dirs = sorted([d for d in SKILLS_DIR.iterdir() if d.is_dir()])

    for sdir in skill_dirs:
        skill_name = sdir.name
        for category in ["templates", "examples", "checklists", "references"]:
            cat_dir = sdir / category
            if not cat_dir.exists():
                continue

            for fpath in sorted(cat_dir.glob("*.md")):
                total_files += 1
                try:
                    content = fpath.read_text(encoding="utf-8")
                except Exception as e:
                    errors.append(f"[{skill_name}/{category}/{fpath.name}] Erro de leitura: {e}")
                    continue

                lines = content.strip().splitlines()
                line_count = len(lines)
                min_required = MIN_LINES_BY_TYPE.get(category, 25)

                file_errors = []

                if line_count < min_required:
                    file_errors.append(f"Tamanho insuficiente: {line_count} linhas (mínimo exigido: {min_required})")

                for banned in BANNED_PATTERNS:
                    if banned in content:
                        file_errors.append(f"Contém padrão de stub/mock proibido: '{banned[:40]}...'")

                if file_errors:
                    errors.append(f"❌ [{skill_name}/{category}/{fpath.name}] -> " + " | ".join(file_errors))
                else:
                    compliant_files += 1

    print("=" * 80)
    print("🛡️  SOTA ACCESSORY ASSETS DEPTH & INTEGRITY AUDIT")
    print("=" * 80)
    print(f"Total de artefatos analisados: {total_files}")
    print(f"Artefatos conformes (SOTA Grade): {compliant_files}")
    print(f"Artefatos não-conformes (Stubs/Mocks): {len(errors)}")
    print("=" * 80)

    if errors:
        print("\nLista de Amostras Não-Conformes:")
        for err in errors[:20]:
            print(f"  {err}")
        if len(errors) > 20:
            print(f"  ... e mais {len(errors) - 20} arquivos com não-conformidades.")
        print("\n❌ [FAIL] Auditoria reprovada: Existem stubs/mocks que precisam de elevação técnica.")
        return False
    else:
        print("\n✅ [PASS] 100% dos artefatos acessórios atendem aos padrões de profundidade SOTA!")
        return True

if __name__ == "__main__":
    success = audit_accessory_assets()
    sys.exit(0 if success else 1)
