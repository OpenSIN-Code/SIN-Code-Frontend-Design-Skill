#!/usr/bin/env bash
# Purpose: Run a WCAG 2.2 AA check from the shell
# Docs: scripts/design-a11y.doc.md
#
# Wraps design_a11y_check. Pass a file or stdin via `-`. Optional
# --fg / --bg trigger a WCAG contrast calculation.
#
# Usage:
#   design-a11y.sh page.html
#   design-a11y.sh page.html --fg=#000000 --bg=#ffffff
