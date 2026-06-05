#!/usr/bin/env bash
# Purpose: Review UI code from the shell
# Docs: scripts/design-review.doc.md
#
# Wraps design_review. Accepts a file path or stdin via `-`.
#
# Usage:
#   design-review.sh page.html
#   echo "<button class='x'>x</button>" | design-review.sh -
