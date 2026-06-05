# tokens.py

**What:** Design-token extraction from CSS, Tailwind, JSON, and Figma sources.

**Why it exists:** Migrating a legacy codebase to the SOTA system is easier if
the agent can pull existing tokens automatically and re-export them.

**Exports:**
- `TokenExtractor` — main class with `extract(source, source_format)`.
- `TokenSet` — extracted token container.
- `SUPPORTED_FORMATS = ("css", "tailwind", "scss", "json", "figma")`
- `TokenExtractor.export_figma(tokens)` — re-export to Figma Tokens JSON.

**Format detection & parsing:**
- `css` / `scss` — regex-based `--name: value;` extraction.
- `tailwind` — JSON-like object literal; strips JS comments, normalizes quotes.
- `json` — straight `json.loads()`.
- `figma` — Figma Tokens plugin format with RGBA 0–1 floats.

**Files that import this:** `mcp_server.py`, `tests/test_tokens.py`.

**Caveats:**
- The CSS parser uses regex, not a full AST. Unbalanced braces in nested
  selectors may confuse the parser; pass full `:root { ... }` blocks for
  reliable extraction.
- Tailwind parsing tolerates common JS-object-literal styles but cannot parse
  every valid JS expression.
