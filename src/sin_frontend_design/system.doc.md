# system.py

**What:** SOTA design system primitives — typography, color, spacing, motion, themes.

**Why it exists:** Single source of truth for design tokens. Mirrors Anthropic's
frontend-design philosophy: 11-step typography scale, 6-ramp color palette,
4px-grid spacing, predictable motion, semantic theme mapping.

**Exports:**
- `TYPOGRAPHY_SCALE` — `[12, 14, 16, 18, 20, 24, 30, 36, 48, 60, 72]`
- `SPACING_SCALE` — `[4, 8, 12, 16, 24, 32, 48, 64, 96]`
- `RADIUS_DEFAULT = 8`, `RADIUS_CARD = 16`
- `DURATION_HOVER_MS = 200`, `DURATION_TRANSITION_MS = 300`, `DURATION_PAGE_MS = 500`
- Color ramps: `NEUTRAL`, `PRIMARY`, `SECONDARY`, `SUCCESS`, `WARNING`, `ERROR`
- `DesignTokens` — frozen dataclass bundling all 4 families
- `Theme` — semantic-role → ramp mapping
- `LIGHT_THEME`, `DARK_THEME` — built-in themes
- `DesignSystem` — the loader; exposes tokens, themes, philosophy, and `to_dict()`

**Why these specific values:**
- 11-step type scale matches common 1.25 ratio from 16.
- 4px grid is the modern industry default.
- 200ms / 300ms motion is below the human perception threshold for "snappy".

**Files that import this:** `components.py`, `reviewer.py`, `__init__.py`.

**Caveats:**
- `DesignTokens` is frozen — create a new one to change values.
- Dark theme currently uses the same ramps as light; production code should
  override `register_theme()` with inverted 600→500 mappings.
