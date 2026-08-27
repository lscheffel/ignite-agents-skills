#!/usr/bin/env bash
# Auto-generate skills/index.json from filesystem with strict YAML frontmatter parsing.
# Usage: ./scripts/sync-index.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 -c "
import os, sys, json, yaml, re

repo_root = sys.argv[1]
skills_dir = os.path.join(repo_root, 'skills')
index_json_path = os.path.join(skills_dir, 'index.json')
readme_path = os.path.join(repo_root, 'README.md')

# Read version from README.md
index_version = '3.0.0'
if os.path.exists(readme_path):
    with open(readme_path, 'r', encoding='utf-8') as f:
        rm_text = f.read()
    m = re.search(r'version-v(\d+\.\d+\.\d+)', rm_text)
    if not m:
        m = re.search(r'^\*\*v(\d+\.\d+\.\d+)', rm_text, re.MULTILINE)
    if m:
        index_version = m.group(1)

skills_list = []
skill_dirs = sorted([d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d)) and not d.startswith('.')])

for sname in skill_dirs:
    sdir = os.path.join(skills_dir, sname)
    skill_md = os.path.join(sdir, 'SKILL.md')
    if not os.path.isfile(skill_md):
        continue

    with open(skill_md, 'r', encoding='utf-8') as f:
        content = f.read()

    parts = content.split('---', 2)
    if len(parts) < 3:
        print(f'⚠️ Warning: {sname} missing frontmatter delimiters', file=sys.stderr)
        continue

    fm = yaml.safe_load(parts[1]) or {}
    name = fm.get('name', sname)
    version = str(fm.get('version', '2.0.0'))
    description = str(fm.get('description', '')).strip()
    
    tags = fm.get('tags', [])
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.strip('[]').split(',') if t.strip()]
    elif not isinstance(tags, list):
        tags = []

    related_skills = fm.get('related_skills', [])
    if isinstance(related_skills, str):
        related_skills = [r.strip() for r in related_skills.strip('[]').split(',') if r.strip()]
    elif not isinstance(related_skills, list):
        related_skills = []

    # Collect files
    files = []
    for root, _, filenames in os.walk(sdir):
        for fname in sorted(filenames):
            if '__pycache__' in root or fname.endswith('.pyc') or fname == '.DS_Store':
                continue
            full_f = os.path.join(root, fname)
            rel_f = os.path.relpath(full_f, sdir)
            files.append(rel_f)
    files.sort()

    entry = {
        'name': name,
        'version': version,
        'description': description,
        'tags': tags,
        'related_skills': related_skills,
        'files': files
    }
    skills_list.append(entry)
    print(f'  ✓ {name}')

skills_list.sort(key=lambda x: x['name'])

final_data = {
    'skills': skills_list,
    'version': index_version,
    'schema_version': '2.0.0',
    'description': f'Registro centralizado de skills ultra-high quality grade para agentes compatíveis com o padrão Agent Skills. Hospedado como GitHub Pages. ({len(skills_list)} skills)',
    'validation': {
        'min_lines_per_skill': 150,
        'required_sections': ['Quando Usar', 'Workflow', 'Anti-patterns', 'Checklists', 'Edge Cases'],
        'required_fields': ['name', 'description', 'version', 'tags', 'related_skills']
    }
}

with open(index_json_path, 'w', encoding='utf-8') as f:
    json.dump(final_data, f, indent=2, ensure_ascii=False)
    f.write('\n')

print(f'\n✅ Index gerado: {len(skills_list)} skills → {index_json_path}')
" "$REPO_ROOT"
