#!/usr/bin/env bash
# Auto-generate skills/index.json from filesystem.
# Scans skills/*/SKILL.md, extracts frontmatter, lists all files.
# Uso: ./scripts/sync-index.sh
#
# This script is idempotent — running it multiple times produces the same output.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_DIR="$REPO_ROOT/skills"
INDEX_JSON="$SKILLS_DIR/index.json"

if ! command -v jq &> /dev/null; then
  echo "ERRO: jq não encontrado. Instale com: sudo apt install jq" >&2
  exit 1
fi

# Start building the index
skills_array="[]"
skill_count=0

for skill_dir in "$SKILLS_DIR"/*/; do
  [ -d "$skill_dir" ] || continue
  skill_md="$skill_dir/SKILL.md"
  [ -f "$skill_md" ] || continue

  skill_name=$(basename "$skill_dir")

  # Extract frontmatter fields from SKILL.md
  frontmatter_name=$(sed -n '/^name:/p' "$skill_md" | head -1 | sed 's/^name:[[:space:]]*//')
  frontmatter_desc=$(sed -n '/^description:/p' "$skill_md" | head -1 | sed 's/^description:[[:space:]]*//')
  frontmatter_version=$(sed -n '/^version:/p' "$skill_md" | head -1 | sed 's/^version:[[:space:]]*//')
  frontmatter_tags=$(sed -n '/^tags:/p' "$skill_md" | head -1 | sed 's/^tags:[[:space:]]*//')
  frontmatter_related=$(sed -n '/^related_skills:/p' "$skill_md" | head -1 | sed 's/^related_skills:[[:space:]]*//')

  # Use frontmatter name if present, otherwise use directory name
  name="${frontmatter_name:-$skill_name}"
  version="${frontmatter_version:-2.0.0}"
  description="${frontmatter_desc:-}"

  # Parse tags from YAML array format: [tag1, tag2, tag3]
  if [[ "$frontmatter_tags" == \[*\] ]]; then
    tags_json=$(echo "$frontmatter_tags" | sed 's/\[//;s/\]//' | tr ',' '\n' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | sed 's/^"//;s/"$//' | jq -R . | jq -s .)
  else
    tags_json="[]"
  fi

  # Parse related_skills from YAML array format
  if [[ "$frontmatter_related" == \[*\] ]]; then
    related_json=$(echo "$frontmatter_related" | sed 's/\[//;s/\]//' | tr ',' '\n' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | sed 's/^"//;s/"$//' | jq -R . | jq -s .)
  else
    related_json="[]"
  fi

  # Collect all files (SKILL.md + templates/ + examples/ + checklists/)
  files_json="[]"
  while IFS= read -r -d '' file; do
    rel_path="${file#$skill_dir}"
    files_json=$(echo "$files_json" | jq --arg f "$rel_path" '. + [$f]')
  done < <(find "$skill_dir" -type f -print0 | sort -z)

  # Build skill entry
  entry=$(jq -n \
    --arg name "$name" \
    --arg version "$version" \
    --arg description "$description" \
    --argjson tags "$tags_json" \
    --argjson related_skills "$related_json" \
    --argjson files "$files_json" \
    '{name: $name, version: $version, description: $description, tags: $tags, related_skills: $related_skills, files: $files}')

  skills_array=$(echo "$skills_array" | jq --argjson entry "$entry" '. + [$entry]')
  skill_count=$((skill_count + 1))
  echo "  ✓ $name"
done

# Sort skills by name for deterministic output
skills_array=$(echo "$skills_array" | jq 'sort_by(.name)')

# Build final index.json
jq -n \
  --argjson skills "$skills_array" \
  --arg version "2.0.3" \
  --arg schema_version "2.0.0" \
  --arg description "Registro centralizado de skills ultra-high quality grade para agentes compatíveis com o padrão Agent Skills. Hospedado como GitHub Pages. ($skill_count skills)" \
  '{
    skills: $skills,
    version: $version,
    schema_version: $schema_version,
    description: $description,
    validation: {
      min_lines_per_skill: 150,
      required_sections: ["Quando Usar", "Workflow", "Anti-patterns", "Checklists", "Edge Cases"],
      required_fields: ["name", "description", "version", "tags", "related_skills"]
    }
  }' > "$INDEX_JSON"

echo
echo "✅ Index gerado: $skill_count skills → $INDEX_JSON"
