---
name: sin-frontend-design
description: "OpenSIN-Code Skill — SOTA frontend design system + philosophy (Anthropic-compatible). Use when the user asks for design tokens, component specs (button, input, card, modal), page scaffolding, UI review, design-token extraction, WCAG a11y checks, responsive breakpoints, or Figma export. Falls back to templates if v0-pool is offline."
---

When the user asks to design, build, or review frontend UI:

1. **Load the design system first** with `design_system_load` (or
   `scripts/design-load.sh`). Internalize the 10-point philosophy.

2. **Generate components** with `design_component_create` (or
   `scripts/design-component.sh`). Pass `use_v0=true` for complex specs.

3. **Scaffold pages** with `design_page_scaffold` (or
   `scripts/design-page.sh`). Use layout=landing for product pages,
   pricing for plan pages, docs for documentation, blog for posts.

4. **Review existing UI** with `design_review` (or `scripts/design-review.sh`).
   Address `error` findings first, then `warning`, then `info`.

5. **Check accessibility** with `design_a11y_check` (or
   `scripts/design-a11y.sh`). WCAG 2.2 AA is the floor — never ship below it.

6. **Extract tokens** from existing code with `design_token_extract` (or
   `scripts/design-tokens.sh`). Re-export to Figma with `design_figma_export`.

7. **Test responsiveness** with `design_responsive_test` (or
   `scripts/design-responsive.sh`). The default 6-tier system is
   xs/sm/md/lg/xl/2xl.

8. **Always prefer templates** over v0 if the user did not ask for AI-generated
   code — templates are deterministic, fast, and offline-safe.

## Design tokens (memorize)

- Typography: 12, 14, 16, 18, 20, 24, 30, 36, 48, 60, 72
- Spacing (4px grid): 4, 8, 12, 16, 24, 32, 48, 64, 96
- Radius: 8 (default), 16 (card)
- Motion: 200ms ease-out (hover), 300ms ease-in-out (transition),
  500ms cubic-bezier(0.16, 1, 0.3, 1) (page)
- Colors: neutral, primary, secondary, success, warning, error
  (50–900 ramp each)
