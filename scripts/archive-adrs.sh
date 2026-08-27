# Archive ADRs with "Implementado" status to cold storage.
# Usage: ./scripts/archive-adrs.sh [--dry-run]
#
# Moves ADR-*.md files with "## Status\nImplementado" to docs/adr/archive/
# Also moves associated BP, TODO, and implementation-plan files.
# Keeps files accessible as reference.