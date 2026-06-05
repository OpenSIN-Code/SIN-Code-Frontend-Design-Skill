# mcp_server.py

**What:** FastMCP server exposing 8 frontend-design tools.

**Tools:**
| Tool | Purpose |
|------|---------|
| `design_system_load` | Load the SOTA design system (tokens, themes, philosophy) |
| `design_component_create` | Generate a component spec (button, input, card, modal) |
| `design_page_scaffold` | Scaffold a full page from a layout + sections |
| `design_review` | Review existing UI for design-system consistency |
| `design_token_extract` | Extract design tokens from CSS/Tailwind/JSON/Figma |
| `design_a11y_check` | WCAG 2.2 AA compliance check (HTML + optional contrast) |
| `design_responsive_test` | Generate responsive breakpoints and current tier |
| `design_figma_export` | Export extracted tokens to Figma Tokens JSON |

**v0-pool integration:**
- `design_component_create(use_v0=True)` calls the v0-pool at
  `http://localhost:27401/v1` and falls back to templates on failure.
- Uses `v0-1.5-lg` for complex prompts (or explicit `complexity="complex"`).
- Uses `v0-1.5-md` for simple prompts.
- Configured via env vars: `V0_BASE_URL`, `V0_API_KEY`, `V0_TIMEOUT`.

**Launch:**
```bash
python3 -m sin_frontend_design.mcp_server
```

**Files that import this:** `tests/test_server.py`.

**Caveats:**
- v0 calls are best-effort; templates are the SSOT fallback.
- Global state (none) — the server has no side-effects on import.
