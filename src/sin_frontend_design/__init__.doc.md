# __init__.py

**What:** Package entry point for `sin_frontend_design`.

**Exports:**
- `DesignSystem` — load SOTA design tokens + philosophy
- `DesignTokens` — typography, color, spacing, motion primitives
- `Theme` — semantic color mapping (light/dark)
- `ComponentGenerator` — button/input/card/modal specs
- `ComponentSpec` — a generated component spec
- `PageScaffolder` — page-level section composition
- `PageScaffold` — full page output
- `DesignReviewer` — code review against the system
- `ReviewFinding`, `ReviewReport` — review outputs
- `TokenExtractor` — extract tokens from CSS/Tailwind/JSON/Figma
- `TokenSet` — extracted token set
- `A11yChecker` — WCAG 2.2 AA checker
- `A11yFinding`, `A11yReport` — a11y outputs
- `BreakpointGenerator` — responsive breakpoint tokens + CSS
- `ResponsiveTokens` — responsive token container

**Usage:**
```python
from sin_frontend_design import DesignSystem, ComponentGenerator
system = DesignSystem()
print(system.tokens.typography)
```

**Files that import this:** `mcp_server.py`, `tests/*`, all scripts.
