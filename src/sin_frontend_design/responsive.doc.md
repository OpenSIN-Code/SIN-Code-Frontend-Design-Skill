# responsive.py

**What:** Responsive breakpoint generator.

**Why it exists:** One consistent set of breakpoints across every project.
Six tiers: xs / sm / md / lg / xl / 2xl.

**Exports:**
- `BreakpointGenerator` — main class.
- `ResponsiveTokens` — the token container.
- `DEFAULT_BREAKPOINTS` — the standard 6-tier list.

**Breakpoint table:**
| Name | Min px | Max px  | Device       |
|------|--------|---------|--------------|
| xs   | 0      | 479     | small phone  |
| sm   | 480    | 767     | large phone  |
| md   | 768    | 1023    | tablet       |
| lg   | 1024   | 1439    | laptop       |
| xl   | 1440   | 1919    | desktop      |
| 2xl  | 1920   | ∞       | wide desktop |

**Container widths:** xs/sm 100% · md 720px · lg 960px · xl 1140px · 2xl 1320px.

**Methods:**
- `tokens()` — return the full ResponsiveTokens.
- `media_query(name)` — return `@media (min-width: Npx) { ... }` for a tier.
- `all_media_queries()` — return all of them as a map.
- `css()` — return a complete CSS payload with tokens + media queries.
- `test(viewport_width)` — return which breakpoint a width falls into.

**Files that import this:** `mcp_server.py`, `tests/test_responsive.py`.

**Caveats:**
- The CSS payload assumes you have a `.container` class — adjust if you use
  a different convention.
- Breakpoints are intentionally mobile-first (min-width queries).
