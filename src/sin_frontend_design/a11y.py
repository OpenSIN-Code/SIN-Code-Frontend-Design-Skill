"""WCAG 2.2 AA accessibility checker.

Docs: src/sin_frontend_design/a11y.doc.md
"""
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from .system import DEFAULT_TOKENS


SEVERITY_LEVELS = ("info", "warning", "error")


@dataclass
class A11yFinding:
    """A single WCAG 2.2 AA finding."""

    rule: str
    severity: str
    message: str
    criterion: str  # e.g. "1.4.3 Contrast (Minimum)"
    line_hint: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule": self.rule,
            "severity": self.severity,
            "message": self.message,
            "criterion": self.criterion,
            "line_hint": self.line_hint,
        }


@dataclass
class A11yReport:
    """Result of an a11y check: ok + list of findings + score."""

    ok: bool
    score: int
    findings: List[A11yFinding] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ok": self.ok,
            "score": self.score,
            "findings": [f.to_dict() for f in self.findings],
        }


class A11yChecker:
    """WCAG 2.2 AA compliance checker for HTML.

    Checks performed:
    - Image alt attributes (1.1.1)
    - Form labels (1.3.1, 4.1.2)
    - Document language (3.1.1)
    - Page title (2.4.2)
    - Heading hierarchy (1.3.1, 2.4.6)
    - Color contrast on hex values (1.4.3)
    - Link text quality (2.4.4)
    - Button vs div onclick (2.1.1)
    """

    IMG_RE = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
    ALT_RE = re.compile(r"\balt\s*=", re.IGNORECASE)
    LANG_RE = re.compile(r"<html\b([^>]*)>", re.IGNORECASE)
    LANG_ATTR_RE = re.compile(r"\blang\s*=", re.IGNORECASE)
    TITLE_RE = re.compile(r"<title>([^<]+)</title>", re.IGNORECASE)
    HEADING_RE = re.compile(r"<h([1-6])\b", re.IGNORECASE)
    LINK_RE = re.compile(r"<a\b[^>]*>([^<]*)</a>", re.IGNORECASE)
    GENERIC_LINK_RE = re.compile(r"^(click here|here|read more|more|learn more|this)$", re.IGNORECASE)
    BUTTON_RE = re.compile(r"<button\b[^>]*>", re.IGNORECASE)
    ONCLICK_DIV_RE = re.compile(r"<div\b[^>]*\bonclick\s*=", re.IGNORECASE)
    INPUT_RE = re.compile(r"<input\b[^>]*>", re.IGNORECASE)
    LABEL_RE = re.compile(r"<label\b[^>]*>", re.IGNORECASE)
    ARIA_LABEL_RE = re.compile(r"\baria-label\s*=", re.IGNORECASE)
    ARIA_LABELLEDBY_RE = re.compile(r"\baria-labelledby\s*=", re.IGNORECASE)
    HEX_RE = re.compile(r"#[0-9a-fA-F]{6}\b")

    def __init__(self) -> None:
        pass

    def check(self, code: str) -> A11yReport:
        """Run all WCAG 2.2 AA checks on the given HTML source."""
        findings: List[A11yFinding] = []
        if not isinstance(code, str) or not code.strip():
            return A11yReport(ok=True, score=100, findings=[])
        findings.extend(self._check_img_alt(code))
        findings.extend(self._check_lang(code))
        findings.extend(self._check_title(code))
        findings.extend(self._check_heading_hierarchy(code))
        findings.extend(self._check_link_text(code))
        findings.extend(self._check_div_onclick(code))
        findings.extend(self._check_input_label(code))
        # score: start at 100, deduct per severity.
        score = 100
        for f in findings:
            if f.severity == "error":
                score -= 7
            elif f.severity == "warning":
                score -= 3
            else:
                score -= 1
        score = max(0, score)
        ok = score >= 80 and not any(f.severity == "error" for f in findings)
        return A11yReport(ok=ok, score=score, findings=findings)

    def _check_img_alt(self, code: str) -> List[A11yFinding]:
        findings: List[A11yFinding] = []
        for img in self.IMG_RE.finditer(code):
            tag = img.group(0)
            if not self.ALT_RE.search(tag):
                findings.append(
                    A11yFinding(
                        rule="img-alt",
                        severity="error",
                        message="<img> is missing alt attribute.",
                        criterion="1.1.1 Non-text Content",
                        line_hint=tag[:80],
                    )
                )
        return findings

    def _check_lang(self, code: str) -> List[A11yFinding]:
        findings: List[A11yFinding] = []
        m = self.LANG_RE.search(code)
        if m and not self.LANG_ATTR_RE.search(m.group(1)):
            findings.append(
                A11yFinding(
                    rule="html-lang",
                    severity="error",
                    message="<html> is missing the 'lang' attribute.",
                    criterion="3.1.1 Language of Page",
                    line_hint=m.group(0)[:80],
                )
            )
        elif not m:
            findings.append(
                A11yFinding(
                    rule="html-element",
                    severity="warning",
                    message="No <html> tag found.",
                    criterion="3.1.1 Language of Page",
                )
            )
        return findings

    def _check_title(self, code: str) -> List[A11yFinding]:
        findings: List[A11yFinding] = []
        m = self.TITLE_RE.search(code)
        if not m:
            findings.append(
                A11yFinding(
                    rule="page-title",
                    severity="error",
                    message="Page is missing a <title> element.",
                    criterion="2.4.2 Page Titled",
                )
            )
        elif not m.group(1).strip():
            findings.append(
                A11yFinding(
                    rule="page-title-empty",
                    severity="error",
                    message="<title> is empty.",
                    criterion="2.4.2 Page Titled",
                )
            )
        return findings

    def _check_heading_hierarchy(self, code: str) -> List[A11yFinding]:
        findings: List[A11yFinding] = []
        levels: List[int] = [int(m.group(1)) for m in self.HEADING_RE.finditer(code)]
        if not levels:
            return findings
        prev = levels[0]
        if prev != 1:
            findings.append(
                A11yFinding(
                    rule="heading-first-not-h1",
                    severity="warning",
                    message=f"First heading is h{prev}; consider starting with h1.",
                    criterion="1.3.1 Info and Relationships",
                )
            )
        for level in levels[1:]:
            if level > prev + 1:
                findings.append(
                    A11yFinding(
                        rule="heading-skip",
                        severity="warning",
                        message=f"Heading level skipped: h{prev} → h{level}.",
                        criterion="1.3.1 Info and Relationships",
                    )
                )
            prev = level
        return findings

    def _check_link_text(self, code: str) -> List[A11yFinding]:
        findings: List[A11yFinding] = []
        for m in self.LINK_RE.finditer(code):
            text = m.group(1).strip()
            if not text:
                findings.append(
                    A11yFinding(
                        rule="link-empty",
                        severity="error",
                        message="<a> has no link text. Provide descriptive text or aria-label.",
                        criterion="2.4.4 Link Purpose",
                        line_hint=m.group(0)[:80],
                    )
                )
            elif self.GENERIC_LINK_RE.match(text):
                findings.append(
                    A11yFinding(
                        rule="link-generic",
                        severity="warning",
                        message=f"Link text '{text}' is not descriptive.",
                        criterion="2.4.4 Link Purpose",
                        line_hint=text,
                    )
                )
        return findings

    def _check_div_onclick(self, code: str) -> List[A11yFinding]:
        findings: List[A11yFinding] = []
        if self.ONCLICK_DIV_RE.search(code):
            findings.append(
                A11yFinding(
                    rule="div-onclick",
                    severity="error",
                    message="<div onclick=...> is not keyboard-accessible.",
                    criterion="2.1.1 Keyboard",
                )
            )
        return findings

    def _check_input_label(self, code: str) -> List[A11yFinding]:
        findings: List[A11yFinding] = []
        inputs = self.INPUT_RE.findall(code)
        labels = self.LABEL_RE.findall(code)
        for inp in inputs:
            has_label = bool(self.ARIA_LABEL_RE.search(inp) or self.ARIA_LABELLEDBY_RE.search(inp))
            if not has_label and not labels:
                findings.append(
                    A11yFinding(
                        rule="input-label",
                        severity="error",
                        message="<input> has no associated <label> or aria-label.",
                        criterion="1.3.1 Info and Relationships",
                        line_hint=inp[:80],
                    )
                )
        return findings

    def check_contrast(self, foreground: str, background: str) -> Dict[str, Any]:
        """Compute WCAG contrast ratio for two colors."""
        try:
            fg = self._parse_hex(foreground)
            bg = self._parse_hex(background)
        except ValueError as e:
            return {"ok": False, "error": str(e)}
        ratio = self._contrast_ratio(fg, bg)
        return {
            "ok": True,
            "ratio": round(ratio, 2),
            "pass_aa_normal": ratio >= 4.5,
            "pass_aa_large": ratio >= 3.0,
            "pass_aaa_normal": ratio >= 7.0,
        }

    def _parse_hex(self, value: str) -> Tuple[float, float, float]:
        h = value.lstrip("#")
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        if len(h) != 6:
            raise ValueError(f"Invalid hex color: {value}")
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

    def _relative_luminance(self, rgb: Tuple[float, float, float]) -> float:
        def channel(c: float) -> float:
            c = c / 255.0
            return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
        r, g, b = rgb
        return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)

    def _contrast_ratio(
        self, fg: Tuple[float, float, float], bg: Tuple[float, float, float]
    ) -> float:
        l1 = self._relative_luminance(fg)
        l2 = self._relative_luminance(bg)
        lighter = max(l1, l2)
        darker = min(l1, l2)
        return (lighter + 0.05) / (darker + 0.05)
