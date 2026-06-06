"""UI reviewer — checks code/HTML against the design system.

Docs: reviewer.doc.md
"""
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .system import DEFAULT_TOKENS, DesignSystem, SPACING_SCALE, TYPOGRAPHY_SCALE


SEVERITY_LEVELS = ("info", "warning", "error")


@dataclass
class ReviewFinding:
    """A single design-system issue found in the code."""

    rule: str
    severity: str
    message: str
    line_hint: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule": self.rule,
            "severity": self.severity,
            "message": self.message,
            "line_hint": self.line_hint,
        }


@dataclass
class ReviewReport:
    """Result of a design review: pass/fail + list of findings."""

    ok: bool
    score: int
    findings: List[ReviewFinding] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ok": self.ok,
            "score": self.score,
            "findings": [f.to_dict() for f in self.findings],
        }


class DesignReviewer:
    """Reviews HTML/CSS/JSX/TSX code for design system adherence.

    Checks performed:
    - Hardcoded color values that don't match the color ramps
    - Hardcoded spacing values not on the 4px grid
    - Hardcoded font sizes not on the typography scale
    - Missing alt attributes on <img>
    - Missing form labels
    - Missing button roles
    - Missing focus styles
    """

    HEX_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b")
    PX_RE = re.compile(r"(\d+(?:\.\d+)?)\s*px\b")
    RGB_RE = re.compile(r"rgba?\([^)]+\)")
    IMG_RE = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
    ALT_RE = re.compile(r"\balt\s*=", re.IGNORECASE)
    INPUT_RE = re.compile(r"<input\b[^>]*>", re.IGNORECASE)
    LABEL_RE = re.compile(r"<label\b[^>]*>", re.IGNORECASE)
    BUTTON_RE = re.compile(r"<button\b[^>]*>", re.IGNORECASE)
    ONCLICK_DIV_RE = re.compile(r"<div\b[^>]*\bonclick\s*=", re.IGNORECASE)
    FOCUS_RE = re.compile(r"(focus|focus-visible|focus-within)\s*[:{]", re.IGNORECASE)

    def __init__(self, system: Optional[DesignSystem] = None) -> None:
        self.system = system or DesignSystem()

    def _is_known_color(self, value: str) -> bool:
        v = value.lower().strip()
        for ramp in DEFAULT_TOKENS.color.values():
            for hex_value in ramp.as_dict().values():
                if v == hex_value.lower():
                    return True
        return v in {"transparent", "currentcolor", "inherit", "none", "unset", "initial"}

    def _is_known_spacing(self, px_value: float) -> bool:
        return int(round(px_value)) in SPACING_SCALE

    def _is_known_typography(self, px_value: float) -> bool:
        return int(round(px_value)) in TYPOGRAPHY_SCALE

    def _hex_to_lower(self, value: str) -> str:
        return value.lower().strip()

    def review(self, code: str) -> ReviewReport:
        """Run all checks on the given source code. Returns a ReviewReport."""
        findings: List[ReviewFinding] = []
        if not isinstance(code, str) or not code.strip():
            return ReviewReport(ok=True, score=100, findings=[])

        findings.extend(self._check_colors(code))
        findings.extend(self._check_spacing(code))
        findings.extend(self._check_typography(code))
        findings.extend(self._check_a11y_images(code))
        findings.extend(self._check_a11y_inputs(code))
        findings.extend(self._check_a11y_buttons(code))
        findings.extend(self._check_focus_visible(code))

        # Score: 100 - 5*errors - 2*warnings - 1*info. Floor at 0.
        score = 100
        for f in findings:
            if f.severity == "error":
                score -= 5
            elif f.severity == "warning":
                score -= 2
            else:
                score -= 1
        score = max(0, score)
        ok = score >= 80 and not any(f.severity == "error" for f in findings)
        return ReviewReport(ok=ok, score=score, findings=findings)

    def _check_colors(self, code: str) -> List[ReviewFinding]:
        findings: List[ReviewFinding] = []
        for match in self.HEX_RE.finditer(code):
            value = match.group(0)
            if not self._is_known_color(self._hex_to_lower(value)):
                findings.append(
                    ReviewFinding(
                        rule="color.hardcoded",
                        severity="warning",
                        message=f"Hardcoded color '{value}' is not in the design system palette. Use a token like var(--color-primary-500).",
                        line_hint=value,
                    )
                )
        return findings

    def _check_spacing(self, code: str) -> List[ReviewFinding]:
        findings: List[ReviewFinding] = []
        for match in self.PX_RE.finditer(code):
            try:
                val = float(match.group(1))
            except ValueError:
                continue
            # Skip if this looks like a font-size, border-width, or radius context.
            # Simple heuristic: we still flag if not on the 4px grid.
            if not self._is_known_spacing(val) and val > 0:
                findings.append(
                    ReviewFinding(
                        rule="spacing.off-grid",
                        severity="warning",
                        message=f"Spacing value {val}px is not on the 4px grid. Allowed: {SPACING_SCALE}.",
                        line_hint=f"{val}px",
                    )
                )
        return findings

    def _check_typography(self, code: str) -> List[ReviewFinding]:
        findings: List[ReviewFinding] = []
        # Heuristic: only flag px values when they appear in `font-size` declarations.
        for line in code.splitlines():
            if "font-size" in line.lower() or "fontsize" in line.lower():
                for match in self.PX_RE.finditer(line):
                    try:
                        val = float(match.group(1))
                    except ValueError:
                        continue
                    if val > 0 and not self._is_known_typography(val):
                        findings.append(
                            ReviewFinding(
                                rule="typography.off-scale",
                                severity="info",
                                message=f"Font size {val}px is not on the typography scale. Allowed: {TYPOGRAPHY_SCALE}.",
                                line_hint=line.strip(),
                            )
                        )
        return findings

    def _check_a11y_images(self, code: str) -> List[ReviewFinding]:
        findings: List[ReviewFinding] = []
        for img in self.IMG_RE.finditer(code):
            tag = img.group(0)
            if not self.ALT_RE.search(tag):
                findings.append(
                    ReviewFinding(
                        rule="a11y.img-alt",
                        severity="error",
                        message="<img> tag is missing an 'alt' attribute.",
                        line_hint=tag[:80],
                    )
                )
        return findings

    def _check_a11y_inputs(self, code: str) -> List[ReviewFinding]:
        findings: List[ReviewFinding] = []
        inputs = self.INPUT_RE.findall(code)
        labels = self.LABEL_RE.findall(code)
        if inputs and not labels:
            # Inputs without any label is a WCAG violation.
            findings.append(
                ReviewFinding(
                    rule="a11y.input-label",
                    severity="error",
                    message="Found <input> elements but no <label>. Pair every input with a label.",
                    line_hint=None,
                )
            )
        return findings

    def _check_a11y_buttons(self, code: str) -> List[ReviewFinding]:
        findings: List[ReviewFinding] = []
        if self.ONCLICK_DIV_RE.search(code):
            findings.append(
                ReviewFinding(
                    rule="a11y.div-onclick",
                    severity="warning",
                    message="<div onclick=...> is not keyboard-accessible. Use <button> or add role='button' + tabindex + keydown handler.",
                    line_hint=None,
                )
            )
        return findings

    def _check_focus_visible(self, code: str) -> List[ReviewFinding]:
        findings: List[ReviewFinding] = []
        if "outline: none" in code.lower() and not self.FOCUS_RE.search(code):
            findings.append(
                ReviewFinding(
                    rule="a11y.focus-visible",
                    severity="warning",
                    message="'outline: none' detected but no replacement focus style found. Add a visible focus ring.",
                    line_hint="outline: none",
                )
            )
        return findings
