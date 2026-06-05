# reviewer.py

**What:** UI reviewer — checks code against the design system.

**Why it exists:** A short, deterministic code review that catches the most
common design-system violations. Designed to run on every PR.

**Exports:**
- `DesignReviewer` — main class with `review(code)`.
- `ReviewFinding` — one issue (`rule`, `severity`, `message`, `line_hint`).
- `ReviewReport` — full report (`ok`, `score`, `findings`).
- `SEVERITY_LEVELS = ("info", "warning", "error")`

**Rules enforced:**
| Rule | Severity | What it catches |
|------|----------|-----------------|
| `color.hardcoded`        | warning | hex values not in the design palette |
| `spacing.off-grid`       | warning | px values not on the 4px grid |
| `typography.off-scale`   | info    | font-size not in the type scale |
| `a11y.img-alt`           | error   | <img> missing alt |
| `a11y.input-label`       | error   | <input> with no <label> anywhere |
| `a11y.div-onclick`       | warning | <div onclick=...> (not keyboard accessible) |
| `a11y.focus-visible`     | warning | outline:none with no focus replacement |

**Scoring:** `100 − 5*errors − 2*warnings − 1*info`, floored at 0.
A report is `ok` when score ≥ 80 and no errors.

**Files that import this:** `mcp_server.py`, `tests/test_reviewer.py`.

**Caveats:**
- The "input without label" rule is conservative: it triggers if any input
  exists and no `<label>` appears anywhere. Fine for whole-page review.
- The contrast check lives in `a11y.py` (deterministic math), not here.
