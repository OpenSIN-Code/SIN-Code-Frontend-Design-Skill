#!/usr/bin/env bash
# Purpose: CLI wrapper for design_token_extract
# Docs: design-tokens.doc.md
#
# Usage:
#   design-tokens.sh path/to/file.css --format=css
#   design-tokens.sh tailwind.config.js --format=tailwind
#   design-tokens.sh tokens.json --format=json
#   design-tokens.sh figma-export.json --format=figma
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

if [[ $# -lt 1 ]]; then
  echo "Usage: $(basename "$0") <file> [--format=css|tailwind|scss|json|figma]" >&2
  exit 1
fi

INPUT="$1"
shift

FORMAT="css"

for arg in "$@"; do
  case "$arg" in
    --format=*) FORMAT="${arg#*=}" ;;
    *) echo "Unknown arg: $arg" >&2; exit 1 ;;
  esac
done

if [[ ! -f "$INPUT" ]]; then
  echo "❌ File not found: $INPUT" >&2
  exit 1
fi

SOURCE=$(cat "$INPUT")

cd "$PROJECT_ROOT" && PYTHONPATH=src python3 -c "
import json
from sin_frontend_design import TokenExtractor
extractor = TokenExtractor()
tokens = extractor.extract('''$SOURCE''', source_format='$FORMAT')
print(json.dumps(tokens.to_dict(), indent=2, default=str))
"
