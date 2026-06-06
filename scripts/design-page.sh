#!/usr/bin/env bash
# Purpose: CLI wrapper for design_page_scaffold
# Docs: design-page.doc.md
#
# Usage:
#   design-page.sh landing --framework=html --title="My SaaS"
#   design-page.sh pricing --framework=react
#   design-page.sh docs --framework=html
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

if [[ $# -lt 1 ]]; then
  echo "Usage: $(basename "$0") <layout> [--framework=html] [--title=Untitled]" >&2
  echo "Layouts: landing | pricing | docs | blog" >&2
  exit 1
fi

LAYOUT="$1"
shift

FRAMEWORK="html"
TITLE="Untitled page"

for arg in "$@"; do
  case "$arg" in
    --framework=*) FRAMEWORK="${arg#*=}" ;;
    --title=*) TITLE="${arg#*=}" ;;
    *) echo "Unknown arg: $arg" >&2; exit 1 ;;
  esac
done

cd "$PROJECT_ROOT" && PYTHONPATH=src python3 -c "
import json
from sin_frontend_design import PageScaffolder
s = PageScaffolder()
page = s.scaffold(layout='$LAYOUT', framework='$FRAMEWORK', title='$TITLE')
print(json.dumps(page.to_dict(), indent=2, default=str))
"
