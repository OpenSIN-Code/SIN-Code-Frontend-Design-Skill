#!/usr/bin/env bash
# Purpose: CLI wrapper for design_a11y_check
# Docs: design-a11y.doc.md
#
# Usage:
#   design-a11y.sh path/to/page.html
#   design-a11y.sh path/to/page.html --fg=#000000 --bg=#ffffff
#   echo "<html>...</html>" | design-a11y.sh -
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

if [[ $# -lt 1 ]]; then
  echo "Usage: $(basename "$0") <file|-> [--fg=#000000] [--bg=#ffffff]" >&2
  exit 1
fi

INPUT="$1"
shift

FG=""
BG=""

for arg in "$@"; do
  case "$arg" in
    --fg=*) FG="${arg#*=}" ;;
    --bg=*) BG="${arg#*=}" ;;
    *) echo "Unknown arg: $arg" >&2; exit 1 ;;
  esac
done

if [[ "$INPUT" == "-" ]]; then
  CODE=$(cat)
else
  if [[ ! -f "$INPUT" ]]; then
    echo "❌ File not found: $INPUT" >&2
    exit 1
  fi
  CODE=$(cat "$INPUT")
fi

cd "$PROJECT_ROOT" && PYTHONPATH=src python3 -c "
import json
from sin_frontend_design import A11yChecker
checker = A11yChecker()
report = checker.check('''$CODE''')
result = report.to_dict()
if '$FG' and '$BG':
    result['contrast'] = checker.check_contrast('$FG', '$BG')
print(json.dumps(result, indent=2, default=str))
"
