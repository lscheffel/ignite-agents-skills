#!/usr/bin/env bash
# Validate skills/index.json against the actual files in the filesystem.
# Usage: ./scripts/validate-index.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# 1. First validate YAML integrity of all skills
bash "$REPO_ROOT/scripts/validate-skill.sh" --all

# 2. Validate index.json structure against filesystem
python3 -c "
import sys, os, json, yaml

repo_root = sys.argv[1]
skills_dir = os.path.join(repo_root, 'skills')
index_file = os.path.join(skills_dir, 'index.json')

if not os.path.isfile(index_file):
    print(f'ERROR: {index_file} not found.', file=sys.stderr)
    sys.exit(1)

with open(index_file, 'r', encoding='utf-8') as f:
    index = json.load(f)

skills = index.get('skills', [])
print(f'Validating {len(skills)} skills in {index_file} ...')

errors = []
indexed_names = set()

for s in skills:
    name = s.get('name')
    if not name:
        errors.append('Skill in index.json missing \"name\" field')
        continue
    indexed_names.add(name)
    sdir = os.path.join(skills_dir, name)
    if not os.path.isdir(sdir):
        errors.append(f'[{name}] Directory not found at {sdir}')
        continue
    
    files = s.get('files', [])
    for rf in files:
        if rf.startswith('skills/'):
            errors.append(f'[{name}] File has invalid prefix \"skills/\": {rf}')
        fpath = os.path.join(sdir, rf)
        if not os.path.isfile(fpath):
            errors.append(f'[{name}] File declared in index.json missing on disk: {rf}')

disk_skills = [d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d)) and os.path.isfile(os.path.join(skills_dir, d, 'SKILL.md'))]
for ds in disk_skills:
    if ds not in indexed_names:
        errors.append(f'[{ds}] Directory exists on disk but is NOT registered in index.json')

if errors:
    print(f'❌ Validation failed with {len(errors)} error(s):')
    for e in errors:
        print(f'   - {e}')
    sys.exit(1)
else:
    print(f'✅ index.json is 100% synchronized and valid with filesystem ({len(skills)} skills).')
    sys.exit(0)
" "$REPO_ROOT"