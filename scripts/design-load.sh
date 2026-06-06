#!/usr/bin/env bash
# Purpose: CLI wrapper for design_system_load
# Docs: design-load.doc.md
#
# Usage:
#   design-load.sh                  # Load default design system
#   design-load.sh --name=default   # Load named design system
#   design-load.sh --json           # Emit machine-readable JSON
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

NAME="default"
JSON_ONLY="false"

for arg in "$@"; do
  case "$arg" in
    --name=*) NAME="${arg#*=}" ;;
    --json) JSON_ONLY="true" ;;
    --help|-h)
      cat <<EOF
Usage: $(basename "$0") [--name=NAME] [--json]

Options:
  --name=NAME  Design system name (default: default)
  --json       Emit JSON only (no pretty header)
  --help       Show this help
EOF
      exit 0
      ;;
    *) echo "Unknown arg: $arg" >&2; exit 1 ;;
  esac
done

RESULT=$(cd "$PROJECT_ROOT" && PYTHONPATH=src python3 -c "
import json
from sin_frontend_design import DesignSystem
ds = DesignSystem()
print(json.dumps(ds.load('$NAME'), indent=2, default=str))
")

if [[ "$JSON_ONLY" == "true" ]]; then
  echo "$RESULT"
else
  echo "Design system: $NAME"
  echo "================================"
  echo "$RESULT"
fi
