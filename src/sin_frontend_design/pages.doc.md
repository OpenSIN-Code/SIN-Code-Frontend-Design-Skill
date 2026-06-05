# pages.py

**What:** Page scaffolder — composes a full page from sections.

**Why it exists:** SOTA landing pages follow a small set of well-known layouts
(landing, pricing, docs, blog). Each layout has a default section recipe that
can be overridden section by section.

**Exports:**
- `PageScaffolder` — main class.
- `PageSection` — one section (`kind`, `content`, `tokens_used`).
- `PageScaffold` — full page output (`layout`, `framework`, `title`, `sections`, `code`).
- `SUPPORTED_SECTIONS = ("hero", "features", "pricing", "cta", "footer", "testimonials", "faq")`
- `SUPPORTED_LAYOUTS = ("landing", "pricing", "docs", "blog")`

**Layouts:**
| Layout    | Default sections |
|-----------|-----------------|
| landing   | hero, features, testimonials, cta, footer |
| pricing   | hero, pricing, faq, footer |
| docs      | hero, features, footer |
| blog      | hero, features, footer |

**Files that import this:** `mcp_server.py`, `tests/test_pages.py`.

**Caveats:**
- The default content is in English; pass `overrides={"hero": {"headline": "..."}}`
  to `scaffold()` to localize.
- The HTML output uses semantic class names (`.hero`, `.features`, etc.) that
  are expected to be styled by your design-system CSS.
