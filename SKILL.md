---
name: frontend-design
description: "SOTA frontend design system + philosophy (Anthropic-compatible). Loads typography, color, spacing, motion tokens; generates button/input/card/modal specs; scaffolds pages; runs WCAG 2.2 AA checks. Uses v0-pool for code generation when --use-v0 is passed."
version: 1.0.0
category: frontend
requirements:
  - v0-pool running at http://localhost:27401 (optional — falls back to templates)
  - Python 3.10+
---

# Frontend Design Skill

SOTA design system + philosophy for AI agents. Anthropic-compatible tokens
(typography, color, spacing, motion), component specs, page scaffolding,
WCAG 2.2 AA checks, and v0-pool integration for code generation.

## Commands

```bash
# Load the design system
~/.config/opencode/skills/frontend-design/scripts/design-load.sh

# Create a component
~/.config/opencode/skills/frontend-design/scripts/design-component.sh button --framework=react
~/.config/opencode/skills/frontend-design/scripts/design-component.sh input --framework=html
~/.config/opencode/skills/frontend-design/scripts/design-component.sh card --framework=react
~/.config/opencode/skills/frontend-design/scripts/design-component.sh modal --use-v0

# Scaffold a page
~/.config/opencode/skills/frontend-design/scripts/design-page.sh landing --framework=html
~/.config/opencode/skills/frontend-design/scripts/design-page.sh pricing --framework=react

# Review existing UI
~/.config/opencode/skills/frontend-design/scripts/design-review.sh path/to/file.html

# Extract design tokens
~/.config/opencode/skills/frontend-design/scripts/design-tokens.sh tokens.css

# Check WCAG 2.2 AA
~/.config/opencode/skills/frontend-design/scripts/design-a11y.sh page.html
~/.config/opencode/skills/frontend-design/scripts/design-a11y.sh page.html --fg=#000 --bg=#fff
```

## MCP Tools (8)

| Tool | Purpose |
|------|---------|
| `design_system_load` | Load the SOTA design system (tokens, themes, philosophy) |
| `design_component_create` | Generate button/input/card/modal specs |
| `design_page_scaffold` | Scaffold a full page from a layout + sections |
| `design_review` | Review code for design system consistency |
| `design_token_extract` | Extract tokens from CSS/Tailwind/JSON/Figma |
| `design_a11y_check` | WCAG 2.2 AA compliance check + contrast |
| `design_responsive_test` | Generate breakpoints, identify current tier |
| `design_figma_export` | Export tokens to Figma Tokens JSON |

## v0-pool integration

The `design_component_create` tool calls the v0-pool at
`http://localhost:27401/v1` when `use_v0=true`:
- Complex prompts (>200 chars) → `v0-1.5-lg`
- Simple prompts → `v0-1.5-md`
- Offline / failure → fall back to built-in templates

## Design Philosophy

1. Hierarchy is created by contrast, not by decoration.
2. Type is the primary voice — choose one family and use scale.
3. Color is functional: primary, secondary, success, warning, error, neutral.
4. Spacing follows a 4px grid — never arbitrary values.
5. Motion is felt, not seen: 200ms hovers, 300ms transitions.
6. Components are predictable: same name, same shape, same tokens.
7. States are explicit: default, hover, focus, active, disabled.
8. Accessibility is non-negotiable: WCAG 2.2 AA is the floor.
9. Dark mode is not inverted — it's a parallel semantic map.
10. Famous brands feel calm because they use restraint.

## Token reference

### Typography (px)
`12 · 14 · 16 · 18 · 20 · 24 · 30 · 36 · 48 · 60 · 72`

### Spacing (px, 4px grid)
`4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 · 96`

### Motion
- Hover: 200ms ease-out
- Transition: 300ms ease-in-out
- Page: 500ms cubic-bezier(0.16, 1, 0.3, 1)

### Radius
- Default: 8px
- Card: 16px

### Color ramps (50–900)
- `neutral` — slate
- `primary` — indigo
- `secondary` — violet
- `success` — green
- `warning` — amber
- `error` — red

## Installation

```bash
# Skill installs into ~/.config/opencode/skills/frontend-design/
cd ~/dev/SIN-Code-Frontend-Design-Skill
bash install.sh
```

## Related Bundles

- **SINator-v0** — v0.dev pool (port 27401) with key rotation
- **SIN-Code-Bundle** — unified CLI for the SIN-Code agent stack
- **co-codocs** — 100% documentation coverage companion
