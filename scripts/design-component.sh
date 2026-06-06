#!/usr/bin/env bash
# Purpose: CLI wrapper for design_component_create
# Docs: design-component.doc.md
#
# Usage:
#   design-component.sh button --framework=react --variant=primary
#   design-component.sh input --framework=vue --placeholder="Email"
#   design-component.sh card --framework=html
#   design-component.sh modal --framework=react --use-v0
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

if [[ $# -lt 1 ]]; then
  echo "Usage: $(basename "$0") <component> [--framework=react] [--variant=primary] [--size=md] [--use-v0] [--label=...] [--placeholder=...] [--title=...]" >&2
  exit 1
fi

COMPONENT="$1"
shift

FRAMEWORK="react"
VARIANT="primary"
SIZE="md"
USE_V0="false"
LABEL=""
PLACEHOLDER=""
TITLE=""

for arg in "$@"; do
  case "$arg" in
    --framework=*) FRAMEWORK="${arg#*=}" ;;
    --variant=*) VARIANT="${arg#*=}" ;;
    --size=*) SIZE="${arg#*=}" ;;
    --use-v0) USE_V0="true" ;;
    --label=*) LABEL="${arg#*=}" ;;
    --placeholder=*) PLACEHOLDER="${arg#*=}" ;;
    --title=*) TITLE="${arg#*=}" ;;
    *) echo "Unknown arg: $arg" >&2; exit 1 ;;
  esac
done

cd "$PROJECT_ROOT" && PYTHONPATH=src python3 -c "
import json
from sin_frontend_design import ComponentGenerator
g = ComponentGenerator()
spec = g.generate(
    '$COMPONENT',
    framework='$FRAMEWORK',
    variant='$VARIANT',
    size='$SIZE',
    label='$LABEL' or 'Click me',
    placeholder='$PLACEHOLDER' or 'Type here...',
    title='$TITLE' or 'Title',
    input_type='text',
)
print(json.dumps(spec.to_dict(), indent=2, default=str))
"
