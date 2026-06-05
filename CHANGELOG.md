# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] — 2026-06-05

### Added
- Initial release of the SIN-Code-Frontend-Design-Skill
- 8 MCP tools: `design_system_load`, `design_component_create`, `design_page_scaffold`,
  `design_review`, `design_token_extract`, `design_a11y_check`, `design_responsive_test`,
  `design_figma_export`
- 6 bash scripts: `design-load.sh`, `design-component.sh`, `design-page.sh`,
  `design-review.sh`, `design-tokens.sh`, `design-a11y.sh`
- 8 Python modules: `system`, `components`, `pages`, `reviewer`, `tokens`, `a11y`,
  `responsive`, `mcp_server`
- SOTA design tokens: 11-step typography scale, 4px spacing grid, 6 color ramps,
  motion timing, two radii
- 4 page layouts: landing, pricing, docs, blog
- 4 component types: button, input, card, modal
- 5 source formats for token extraction: CSS, SCSS, Tailwind, JSON, Figma
- WCAG 2.2 AA compliance checker with 9 rule categories
- v0-pool integration at `http://localhost:27401/v1` with v0-1.5-lg / v0-1.5-md
- 202 passing tests across 10 test files
- 100% CoDocs coverage — every .py, .sh, test_*.py has a .doc.md companion
- ceo-audit workflow (SOTA repo review)
- `SIN_GITHUB_FALLBACK_TOKEN` repo secret configured
- Conventional Commits, immutable annotated tags, no branches (main only)
