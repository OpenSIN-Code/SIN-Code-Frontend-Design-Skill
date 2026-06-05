#!/usr/bin/env bash
# Purpose: Extract design tokens from source code
# Docs: scripts/design-tokens.doc.md
#
# Wraps design_token_extract. Formats: css, scss, tailwind, json, figma.
#
# Usage:
#   design-tokens.sh tokens.css
#   design-tokens.sh tailwind.config.js --format=tailwind
