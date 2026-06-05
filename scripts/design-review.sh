#!/usr/bin/env bash
# Purpose: CLI wrapper for design_review
# Docs: scripts/design-review.doc.md
#
# Usage:
#   design-review.sh path/to/file.htmlx
#   design-review.sh path/to/file.css
#   echo "<button>...</button>" | design-review.sh -
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

if [[ $# -lt 1 ]]; then
  echo "Usage: $(basename "$0") <file|->" >&2
  exit 1
fi

INPUT="$1"

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
from sin_frontend_design import DesignReviewer
reviewer = DesignReviewer()
report = reviewer.review('''$CODE''')
print(json.dumps(report.to_dict(), indent=2, default=str))
"
