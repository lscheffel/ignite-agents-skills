#!/usr/bin/env bash
# validate-skill.sh - Validação estrita de YAML e conformidade de SKILL.md
# Uso: bash scripts/validate-skill.sh [skill-directory | --all]

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="${1:-skills}"

python3 -c "
import sys, os, yaml

target = sys.argv[1]
repo_root = sys.argv[2]

if target == '--all' or target == 'skills' or target == os.path.join(repo_root, 'skills'):
    skills_dir = os.path.join(repo_root, 'skills')
    targets = [os.path.join(skills_dir, d) for d in sorted(os.listdir(skills_dir)) if os.path.isdir(os.path.join(skills_dir, d)) and not d.startswith('.')]
else:
    if os.path.isfile(target) and os.path.basename(target) == 'SKILL.md':
        targets = [os.path.dirname(os.path.abspath(target))]
    else:
        targets = [os.path.abspath(target)]

errors = []
validated = 0

for sdir in targets:
    sname = os.path.basename(sdir)
    skill_md = os.path.join(sdir, 'SKILL.md')
    if not os.path.isfile(skill_md):
        # If it's just a non-skill folder in skills (e.g., templates or data), skip if not a skill
        if os.path.exists(os.path.join(sdir, 'scripts')) or os.path.exists(os.path.join(sdir, 'references')):
            errors.append(f'[{sname}] Faltando arquivo obrigatório SKILL.md')
        continue

    try:
        with open(skill_md, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        errors.append(f'[{sname}] Erro ao ler SKILL.md: {e}')
        continue

    if not content.startswith('---'):
        errors.append(f'[{sname}] SKILL.md deve iniciar com delimitador YAML \"---\"')
        continue

    parts = content.split('---', 2)
    if len(parts) < 3:
        errors.append(f'[{sname}] SKILL.md possui delimitadores \"---\" incompletos')
        continue

    fm_raw = parts[1]
    try:
        fm = yaml.safe_load(fm_raw)
    except Exception as e:
        errors.append(f'[{sname}] Sintaxe YAML inválida no frontmatter: {e}')
        continue

    if not isinstance(fm, dict):
        errors.append(f'[{sname}] Frontmatter deve ser um objeto/dicionário YAML')
        continue

    for req in ['name', 'description', 'version']:
        if req not in fm or not str(fm[req]).strip():
            errors.append(f'[{sname}] Campo obrigatório ausente ou vazio: \"{req}\"')

    if 'name' in fm and fm['name'] != sname:
        errors.append(f'[{sname}] Nome no frontmatter (\"{fm[\"name\"]}\") não corresponde ao diretório (\"{sname}\")')

    validated += 1

if errors:
    print(f'❌ Falha na validação ({len(errors)} erro(s) em {validated} skill(s)):')
    for err in errors:
        print(f'   {err}')
    sys.exit(1)
else:
    print(f'✅ Validação de conformidade YAML concluída com sucesso: {validated} skill(s) 100% válidas.')
    sys.exit(0)
" "$TARGET" "$REPO_ROOT"