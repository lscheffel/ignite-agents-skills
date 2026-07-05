#!/usr/bin/env bash
# Archive ADRs with "Implementado" status to cold storage.
# Uso: ./scripts/archive-adrs.sh [--dry-run]
#
# Moves ADR-*.md files with "## Status\nImplementado" to docs/adr/archive/
# Also moves associated BP, TODO, and implementation-plan files.
# Keeps files accessible as reference.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ADR_DIR="$REPO_ROOT/docs/adr"
ARCHIVE_DIR="$ADR_DIR/archive"
DRY_RUN=false

if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=true
  echo "🔍 DRY RUN — no files will be moved"
  echo
fi

# Create archive directory if it doesn't exist
if [ "$DRY_RUN" = false ]; then
  mkdir -p "$ARCHIVE_DIR"
fi

archived=0
active=0
archived_nums=()

for adr_file in "$ADR_DIR"/ADR-*.md; do
  [ -f "$adr_file" ] || continue
  filename=$(basename "$adr_file")

  # Skip files already in archive or associated files (BP, TODO, etc.)
  [[ "$filename" == archive/* ]] && continue
  [[ "$filename" == *-BP.md ]] && continue
  [[ "$filename" == *-TODO.md ]] && continue
  [[ "$filename" == *-implementation-plan.md ]] && continue

  # Check if status is "Implementado"
  # Handle both single-line and multi-line status formats
  status_line=$(grep -A1 "^## Status" "$adr_file" | tail -1 | xargs)
  
  # Also check if "Implementado" appears anywhere in the status section
  status_block=$(sed -n '/^## Status$/,/^## [^S]/{p}' "$adr_file" | tr '\n' ' ')
  
  if [[ "$status_block" == *"Implementado"* ]] || [[ "$status_line" == *"Implementado"* ]]; then
    # Extract ADR number for finding related files
    adr_num=$(echo "$filename" | sed 's/ADR-\([0-9]*\).*/\1/')

    echo "📦 Archive: $filename (status: $status_line)"

    # Move main ADR file
    if [ "$DRY_RUN" = false ]; then
      mv "$adr_file" "$ARCHIVE_DIR/"
    fi

    # Move associated files (BP, TODO, implementation-plan)
    for suffix in "-BP.md" "-TODO.md" "-implementation-plan.md"; do
      assoc_file="$ADR_DIR/ADR-${adr_num}${suffix}"
      if [ -f "$assoc_file" ]; then
        echo "   └─ + $(basename "$assoc_file")"
        if [ "$DRY_RUN" = false ]; then
          mv "$assoc_file" "$ARCHIVE_DIR/"
        fi
      fi
    done

    archived=$((archived + 1))
    archived_nums+=("$adr_num")
  else
    active=$((active + 1))
    echo "🟢 Active: $filename (status: $status_line)"
  fi
done

echo
echo "📊 Summary:"
echo "   Active: $active"
echo "   Archived: $archived"
if [ $archived -gt 0 ]; then
  echo "   Archived ADRs: ${archived_nums[*]}"
fi

if [ "$DRY_RUN" = true ]; then
  echo
  echo "ℹ️  Dry run complete — no files were moved"
fi
