# Validate skills/index.json against the actual files in the filesystem.
# Usage: ./scripts/validate-index.sh
#
# Check:
# 1. Each skill listed in index.json has a corresponding folder in skills/<name>/
# 2. Each file in "files" exists in skills/<name>/<file>
# 3. The "name" in index.json matches the "name" declared in the frontmatter of SKILL.md
# 4. No file in "files" contains the prefix "skills/" (a common error that breaks Kilo)
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_DIR="$REPO_ROOT/skills"
INDEX_JSON="$SKILLS_DIR/index.json"
if ! command -v jq &> /dev/null; then
  echo "ERROR: jq not found. Install with: sudo apt install jq" >&2
  exit 1
fi
if [ ! -f "$INDEX_JSON" ]; then
  echo "ERROR: $INDEX_JSON not found." >&2
  exit 1
fi
errors=0
count=$(jq '.skills | length' "$INDEX_JSON")
echo "Validating $count skills in $INDEX_JSON ..."