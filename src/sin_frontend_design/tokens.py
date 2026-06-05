"""Design token extraction — parses CSS/Tailwind/JSON sources.

Docs: src/sin_frontend_design/tokens.doc.md
"""
import json
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


SUPPORTED_FORMATS = ("css", "tailwind", "scss", "json", "figma")


@dataclass
class TokenSet:
    """An extracted set of design tokens grouped by family."""

    source_format: str
    typography: Dict[str, Any] = field(default_factory=dict)
    color: Dict[str, str] = field(default_factory=dict)
    spacing: Dict[str, str] = field(default_factory=dict)
    radius: Dict[str, str] = field(default_factory=dict)
    motion: Dict[str, Any] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_format": self.source_format,
            "typography": self.typography,
            "color": self.color,
            "spacing": self.spacing,
            "radius": self.radius,
            "motion": self.motion,
        }


class TokenExtractor:
    """Extract design tokens from CSS, Tailwind config, SCSS, JSON, or Figma.

    Returns a TokenSet with the discovered tokens, structured by family.
    """

    # CSS custom property: --color-primary-500: #6366f1;
    CSS_VAR_RE = re.compile(r"--([a-zA-Z0-9-]+)\s*:\s*([^;]+);")
    # CSS property (non-custom): color: red; font-size: 16px;
    CSS_PX_RE = re.compile(r"(\d+(?:\.\d+)?)\s*px")
    CSS_HEX_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b")
    # Tailwind extend: extend: { colors: { primary: { 500: '#6366f1' } } }
    TAILWIND_NESTED_RE = re.compile(r'"([a-zA-Z0-9-]+)"\s*:\s*\{([^}]+)\}')
    # Figma: "color" : { "r": 0.4, "g": 0.5, "b": 0.9, "a": 1 }
    FIGMA_COLOR_RE = re.compile(
        r'"name"\s*:\s*"([^"]+)"\s*,\s*"color"\s*:\s*\{\s*"r"\s*:\s*([\d.]+)\s*,\s*"g"\s*:\s*([\d.]+)\s*,\s*"b"\s*:\s*([\d.]+)\s*(?:,\s*"a"\s*:\s*([\d.]+)\s*)?\}'
    )

    def __init__(self) -> None:
        self.supported = SUPPORTED_FORMATS

    def extract(self, source: str, source_format: str = "css") -> TokenSet:
        if source_format == "css":
            return self._extract_css(source)
        if source_format == "scss":
            return self._extract_css(source)
        if source_format == "tailwind":
            return self._extract_tailwind(source)
        if source_format == "json":
            return self._extract_json(source)
        if source_format == "figma":
            return self._extract_figma(source)
        raise ValueError(
            f"Unsupported source_format: {source_format}. Choose from {SUPPORTED_FORMATS}."
        )

    def _extract_css(self, source: str) -> TokenSet:
        ts = TokenSet(source_format="css")
        for match in self.CSS_VAR_RE.finditer(source):
            name = match.group(1).strip()
            value = match.group(2).strip()
            self._classify(name, value, ts)
        ts.raw = {"declarations": [m.group(0) for m in self.CSS_VAR_RE.finditer(source)]}
        return ts

    def _classify(self, name: str, value: str, ts: TokenSet) -> None:
        lower = name.lower()
        if "color" in lower or self.CSS_HEX_RE.match(value):
            ts.color[name] = value
        elif "spacing" in lower or "space" in lower or "gap" in lower or "padding" in lower or "margin" in lower:
            ts.spacing[name] = value
        elif "radius" in lower or "border-radius" in lower:
            ts.radius[name] = value
        elif "font" in lower or "text" in lower or "size" in lower:
            ts.typography[name] = value
        elif "duration" in lower or "transition" in lower or "ease" in lower:
            ts.motion[name] = value
        else:
            ts.color[name] = value

    def _extract_tailwind(self, source: str) -> TokenSet:
        ts = TokenSet(source_format="tailwind")
        # Try to parse as JS/JSObject first.
        cleaned = self._strip_js_comments(source)
        # If the source doesn't start with '{', wrap it.
        if "{" in cleaned:
            start = cleaned.find("{")
            end = cleaned.rfind("}")
            if start >= 0 and end > start:
                cleaned = cleaned[start : end + 1]
        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError:
            data = {}
        # Look for theme.extend.colors, theme.colors, theme.spacing, etc.
        colors = self._dig(data, ["theme", "extend", "colors"]) or self._dig(data, ["theme", "colors"])
        if isinstance(colors, dict):
            for name, value in colors.items():
                if isinstance(value, str):
                    ts.color[name] = value
                elif isinstance(value, dict):
                    for step, hex_value in value.items():
                        ts.color[f"{name}-{step}"] = hex_value
        spacing = self._dig(data, ["theme", "extend", "spacing"]) or self._dig(data, ["theme", "spacing"])
        if isinstance(spacing, dict):
            ts.spacing.update({k: v for k, v in spacing.items() if isinstance(v, str)})
        radius = self._dig(data, ["theme", "extend", "borderRadius"]) or self._dig(data, ["theme", "borderRadius"])
        if isinstance(radius, dict):
            ts.radius.update({k: v for k, v in radius.items() if isinstance(v, str)})
        ts.raw = data
        return ts

    def _dig(self, data: Any, path: List[str]) -> Any:
        cur: Any = data
        for k in path:
            if not isinstance(cur, dict):
                return None
            cur = cur.get(k)
        return cur

    def _strip_js_comments(self, s: str) -> str:
        # Remove // line comments and /* block */ comments.
        s = re.sub(r"/\*[\s\S]*?\*/", "", s)
        s = re.sub(r"//.*", "", s)
        # Quote unquoted keys (alpha, underscore, digit start):
        #   {colors: ...}  ->  {"colors": ...}
        #   {500: ...}     ->  {"500": ...}
        s = re.sub(r"([{,]\s*)([a-zA-Z_][a-zA-Z0-9_-]*|[0-9]+)\s*:", r'\1"\2":', s)
        # Replace single-quoted strings with double-quoted ones.
        s = re.sub(r"'([^']*)'", r'"\1"', s)
        return s

    def _extract_json(self, source: str) -> TokenSet:
        ts = TokenSet(source_format="json")
        data = json.loads(source)
        if not isinstance(data, dict):
            return ts
        for family in ("typography", "color", "spacing", "radius", "motion"):
            value = data.get(family)
            if isinstance(value, dict):
                getattr(ts, family).update({k: str(v) for k, v in value.items()})
        ts.raw = data
        return ts

    def _extract_figma(self, source: str) -> TokenSet:
        ts = TokenSet(source_format="figma")
        data = json.loads(source)
        items = data if isinstance(data, list) else data.get("colors", [])
        for item in items:
            if not isinstance(item, dict):
                continue
            name = item.get("name", "")
            color = item.get("color", {})
            if not (name and isinstance(color, dict)):
                continue
            r = color.get("r", 0)
            g = color.get("g", 0)
            b = color.get("b", 0)
            a = color.get("a", 1)
            hex_value = self._rgba_to_hex(r, g, b, a)
            ts.color[name] = hex_value
        ts.raw = data
        return ts

    def _rgba_to_hex(self, r: float, g: float, b: float, a: float = 1.0) -> str:
        def to_byte(v: float) -> int:
            return max(0, min(255, int(round(v * 255))))
        if a < 1:
            return f"#{to_byte(r):02x}{to_byte(g):02x}{to_byte(b):02x}{to_byte(a):02x}"
        return f"#{to_byte(r):02x}{to_byte(g):02x}{to_byte(b):02x}"

    def export_figma(self, tokens: TokenSet) -> str:
        """Export a TokenSet to Figma Tokens JSON format."""
        out: Dict[str, Any] = {"colors": []}
        for name, value in tokens.color.items():
            if value.startswith("#"):
                rgba = self._hex_to_rgba(value)
                out["colors"].append({"name": name, "color": rgba})
        return json.dumps(out, indent=2)

    def _hex_to_rgba(self, hex_value: str) -> Dict[str, float]:
        h = hex_value.lstrip("#")
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        if len(h) >= 6:
            r = int(h[0:2], 16) / 255.0
            g = int(h[2:4], 16) / 255.0
            b = int(h[4:6], 16) / 255.0
            a = int(h[6:8], 16) / 255.0 if len(h) == 8 else 1.0
            return {"r": round(r, 4), "g": round(g, 4), "b": round(b, 4), "a": round(a, 4)}
        return {"r": 0, "g": 0, "b": 0, "a": 1}
