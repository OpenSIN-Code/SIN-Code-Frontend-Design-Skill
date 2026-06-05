#!/usr/bin/env bash
# Purpose: Create a component spec from the shell
# Docs: scripts/design-component.doc.md
#
# Wraps design_component_create. Supports button, input, card, modal.
# For complex components, set --use-v0 to call the v0-pool.
#
# Usage:
#   design-component.sh button --framework=react
#   design-component.sh input --framework=html --placeholder="Email"
#   design-component.sh modal --framework=react --use-v0
