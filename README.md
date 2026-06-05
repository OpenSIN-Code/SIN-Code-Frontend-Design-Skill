# SIN-Code-Frontend-Design-Skill

[![GitNexus](https://img.shields.io/badge/GitNexus-knowledge%20graph-8B5CF6)](.gitnexus/)
[![CEO Audit](https://github.com/OpenSIN-Code/SIN-Code-Frontend-Design-Skill/actions/workflows/ceo-audit.yml/badge.svg)](.github/workflows/ceo-audit.yml)

> **SOTA design system + philosophy (Anthropic-compatible).** 8 MCP tools, 6
> bash scripts, 100% CoDocs, 202 passing tests. Falls back to templates if the
> v0-pool is offline.

The SIN counterpart to Anthropic's official `frontend-design` skill (277K
installs). Provides a design system, component generator, page scaffolder, and
WCAG 2.2 AA checker that agents load **before** writing frontend code.

## Architecture

```
Agent (opencode / Cursor / Claude)
    ↓ loads skill
SIN-Code-Frontend-Design-Skill
    ├─ MCP tools (8)
    ├─ Bash scripts (6)
    ├─ Python modules (8)
    └─ v0-pool integration (http://localhost:27401/v1)
         ↓ complex prompts
    SINator-v0 (v0-1.5-lg)
         ↓ simple prompts
    v0-1.5-md
         ↓ offline → templates
    Built-in component specs
```

## MCP Tools

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

## Quick-Start

```bash
git clone https://github.com/OpenSIN-Code/SIN-Code-Frontend-Design-Skill.git
cd SIN-Code-Frontend-Design-Skill
chmod +x install.sh
./install.sh
```

## Usage

### As MCP server

```bash
# Launch the FastMCP server
python3 -m sin_frontend_design.mcp_server
```

### From Python

```python
from sin_frontend_design import (
    DesignSystem,
    ComponentGenerator,
    PageScaffolder,
    DesignReviewer,
    TokenExtractor,
    A11yChecker,
    BreakpointGenerator,
)

# 1. Load the design system
ds = DesignSystem()
print(ds.philosophy())

# 2. Generate a component
g = ComponentGenerator()
button = g.button(framework="react", variant="primary", size="md", label="Save")
print(button.code)

# 3. Scaffold a page
s = PageScaffolder()
page = s.scaffold(layout="landing", framework="html", title="My SaaS")
print(page.code)

# 4. Review existing UI
reviewer = DesignReviewer()
report = reviewer.review("<button>Click</button>")
print(report.score, report.findings)

# 5. Extract tokens from existing CSS
extractor = TokenExtractor()
tokens = extractor.extract(open("tokens.css").read(), source_format="css")

# 6. Check WCAG 2.2 AA
checker = A11yChecker()
a11y = checker.check(open("page.html").read())
print(a11y.ok, a11y.score)

# 7. Get responsive breakpoints
bg = BreakpointGenerator()
print(bg.test(viewport_width=1280))  # 'lg'
```

### From shell

```bash
# Load the design system
./scripts/design-load.sh

# Generate components
./scripts/design-component.sh button --framework=react --variant=primary
./scripts/design-component.sh input --framework=html --placeholder="Email"
./scripts/design-component.sh card --framework=react
./scripts/design-component.sh modal --use-v0

# Scaffold a page
./scripts/design-page.sh landing --framework=html --title="My SaaS"
./scripts/design-page.sh pricing --framework=react

# Review UI
./scripts/design-review.sh path/to/page.html
echo "<button>Click</button>" | ./scripts/design-review.sh -

# Extract tokens
./scripts/design-tokens.sh tokens.css
./scripts/design-tokens.sh tailwind.config.js --format=tailwind

# Check accessibility
./scripts/design-a11y.sh page.html
./scripts/design-a11y.sh page.html --fg=#000000 --bg=#ffffff
```

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

## Tests

```bash
# All tests
PYTHONPATH=src python3 -m pytest tests/ -v
# 202 passed
```

## CoDocs

100% CoDocs coverage — every `.py` in `src/sin_frontend_design/` has a matching
`.doc.md` companion, and every `.sh` script and test file does too.

## v0-pool integration

The `design_component_create` tool calls the v0-pool at
`http://localhost:27401/v1` when `use_v0=true`:
- Complex prompts (>200 chars) → `v0-1.5-lg`
- Simple prompts → `v0-1.5-md`
- Offline / failure → fall back to built-in templates

## Files

```
SIN-Code-Frontend-Design-Skill/
├── README.md
├── SKILL.md
├── CHANGELOG.md
├── AGENTS.md
├── INSTALL.md
├── install.sh
├── pyproject.toml
├── requirements.txt
├── .gitignore
├── .github/workflows/ceo-audit.yml
├── src/sin_frontend_design/
│   ├── __init__.py (+ .doc.md)
│   ├── system.py (+ .doc.md)     — typography, color, spacing, motion
│   ├── components.py (+ .doc.md)  — button/input/card/modal specs
│   ├── pages.py (+ .doc.md)       — page scaffolder (hero, features, ...)
│   ├── reviewer.py (+ .doc.md)    — design system review
│   ├── tokens.py (+ .doc.md)      — token extraction (CSS/Tailwind/Figma)
│   ├── a11y.py (+ .doc.md)        — WCAG 2.2 AA checker
│   ├── responsive.py (+ .doc.md)  — breakpoint generator
│   └── mcp_server.py (+ .doc.md)  — FastMCP server with 8 tools
├── scripts/
│   ├── design-load.sh
│   ├── design-component.sh
│   ├── design-page.sh
│   ├── design-review.sh
│   ├── design-tokens.sh
│   └── design-a11y.sh
└── tests/
    ├── test_system.py
    ├── test_components.py
    ├── test_pages.py
    ├── test_reviewer.py
    ├── test_tokens.py
    ├── test_a11y.py
    ├── test_responsive.py
    ├── test_server.py
    ├── test_scripts.py
    └── test_codocs.py
```

## Related

- [SINator-v0](https://github.com/OpenSIN-Code/SINator-v0) — v0.dev pool
- [SIN-Code-Bundle](https://github.com/OpenSIN-Code/SIN-Code-Bundle) — unified CLI
- [Anthropic frontend-design](https://github.com/anthropics/skills/tree/main/skills/frontend-design) — original

## License

OpenSIN AI · Open source · Built for agents.
