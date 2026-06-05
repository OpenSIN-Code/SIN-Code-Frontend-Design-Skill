# components.py

**What:** Component spec generator — produces UI specs for `button`, `input`, `card`, `modal`.

**Why it exists:** Agents need to emit *structured* component specs (props,
tokens, a11y, code) rather than freeform snippets. The output is consumed by
the MCP server, bash scripts, and the v0-pool integration.

**Exports:**
- `ComponentGenerator` — main class; one method per component.
- `ComponentSpec` — dataclass with `name`, `framework`, `variant`, `size`,
  `tokens_used`, `props`, `a11y`, `code`.
- `SUPPORTED_FRAMEWORKS = ("react", "vue", "svelte", "html")`
- `SUPPORTED_VARIANTS = ("primary", "secondary", "ghost", "outline", "danger")`
- `SUPPORTED_SIZES = ("xs", "sm", "md", "lg", "xl")`

**Per-component outputs:**
| Component | Tokens | A11y checks |
|-----------|--------|-------------|
| Button    | color, spacing, radius, motion | native button, focus, contrast |
| Input     | color (border + focus ring)    | label pairing, aria-invalid |
| Card      | color, spacing, radius, shadow | heading hierarchy, no nested links |
| Modal     | color, spacing, overlay, z-index | role=dialog, focus trap, Escape |

**Files that import this:** `mcp_server.py`, `pages.py`, `tests/test_components.py`.

**Caveats:**
- The "code" field is a working skeleton, not a styled polished component.
  The `use_v0=true` MCP option upgrades it via the v0-pool.
- The size-to-px mapping uses a 2px step from the `md` baseline.
