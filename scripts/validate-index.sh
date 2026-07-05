#!/usr/bin/env bash
# Valida skills/index.json contra os arquivos reais no filesystem.
# Uso: ./scripts/validate-index.sh
#
# Checa:
#   1. Cada skill listada em index.json tem uma pasta correspondente em skills/<name>/
#   2. Cada arquivo em "files" existe em skills/<name>/<file>
#   3. O "name" no index.json bate com o "name" declarado no frontmatter do SKILL.md
#   4. Nenhum arquivo em "files" contém o prefixo "skills/" (erro comum que quebra o Kilo)

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_DIR="$REPO_ROOT/skills"
INDEX_JSON="$SKILLS_DIR/index.json"

if ! command -v jq &> /dev/null; then
  echo "ERRO: jq não encontrado. Instale com: sudo apt install jq" >&2
  exit 1
fi

if [ ! -f "$INDEX_JSON" ]; then
  echo "ERRO: $INDEX_JSON não encontrado." >&2
  exit 1
fi

errors=0
count=$(jq '.skills | length' "$INDEX_JSON")

echo "Validando $count skills em $INDEX_JSON ..."
echo

for i in $(seq 0 $((count - 1))); do
  name=$(jq -r ".skills[$i].name" "$INDEX_JSON")
  skill_dir="$SKILLS_DIR/$name"

  if [ ! -d "$skill_dir" ]; then
    echo "FALHA [$name]: pasta skills/$name/ não existe."
    errors=$((errors + 1))
    continue
  fi

  files_count=$(jq ".skills[$i].files | length" "$INDEX_JSON")
  for j in $(seq 0 $((files_count - 1))); do
    file=$(jq -r ".skills[$i].files[$j]" "$INDEX_JSON")

    if [[ "$file" == skills/* ]]; then
      echo "FALHA [$name]: entrada '$file' contém prefixo 'skills/' — isso quebra a resolução do Kilo ({url}/{name}/{file}). Use path relativo, ex.: '${file#skills/$name/}'."
      errors=$((errors + 1))
      continue
    fi

    if [ ! -f "$skill_dir/$file" ]; then
      echo "FALHA [$name]: arquivo '$file' não encontrado em skills/$name/$file"
      errors=$((errors + 1))
    fi
  done

  skill_md="$skill_dir/SKILL.md"
  if [ -f "$skill_md" ]; then
    frontmatter_name=$(sed -n '/^name:/p' "$skill_md" | head -1 | sed 's/^name:[[:space:]]*//')
    if [ "$frontmatter_name" != "$name" ]; then
      echo "FALHA [$name]: frontmatter do SKILL.md declara name='$frontmatter_name', esperado '$name'."
      errors=$((errors + 1))
    fi
  fi
done

echo
# 5. Verificar consistência de versão README ↔ index.json
index_version=$(jq -r '.version' "$INDEX_JSON")
readme_version=$(grep -oP '^\*\*v\K[0-9]+\.[0-9]+\.[0-9]+' "$REPO_ROOT/README.md" | head -1)
if [ "$index_version" != "$readme_version" ]; then
  echo "FALHA: Versão em index.json ($index_version) não bate com README.md ($readme_version)"
  errors=$((errors + 1))
else
  echo "OK: Versão consistente ($index_version)"
fi

echo
if [ "$errors" -eq 0 ]; then
  echo "OK: todas as $count skills validadas sem erros."
  exit 0
else
  echo "FALHA: $errors problema(s) encontrado(s)."
  exit 1
fi
