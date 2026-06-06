"""Tests for TokenExtractor.

Docs: test_tokens.doc.md
"""
import json

import pytest

from sin_frontend_design.tokens import TokenExtractor, TokenSet, SUPPORTED_FORMATS


class TestCss:
    def test_basic_css(self) -> None:
        e = TokenExtractor()
        ts = e.extract("--color-primary-500: #6366f1;", "css")
        assert "color-primary-500" in ts.color
        assert ts.color["color-primary-500"] == "#6366f1"

    def test_spacing(self) -> None:
        e = TokenExtractor()
        ts = e.extract("--spacing-md: 16px;", "css")
        assert "spacing-md" in ts.spacing

    def test_radius(self) -> None:
        e = TokenExtractor()
        ts = e.extract("--radius-default: 8px;", "css")
        assert "radius-default" in ts.radius

    def test_typography(self) -> None:
        e = TokenExtractor()
        ts = e.extract("--font-size-base: 16px;", "css")
        assert "font-size-base" in ts.typography

    def test_motion(self) -> None:
        e = TokenExtractor()
        ts = e.extract("--duration-hover: 200ms;", "css")
        assert "duration-hover" in ts.motion


class TestTailwind:
    def test_basic_tailwind(self) -> None:
        e = TokenExtractor()
        source = "module.exports = { theme: { extend: { colors: { primary: '#6366f1' } } } }"
        ts = e.extract(source, "tailwind")
        assert "primary" in ts.color

    def test_tailwind_nested(self) -> None:
        e = TokenExtractor()
        source = "module.exports = { theme: { extend: { colors: { brand: { 500: '#ff0000' } } } } }"
        ts = e.extract(source, "tailwind")
        assert "brand-500" in ts.color

    def test_tailwind_spacing(self) -> None:
        e = TokenExtractor()
        source = "module.exports = { theme: { extend: { spacing: { md: '16px' } } } }"
        ts = e.extract(source, "tailwind")
        assert ts.spacing.get("md") == "16px"


class TestJson:
    def test_basic_json(self) -> None:
        e = TokenExtractor()
        data = {"color": {"primary": "#6366f1"}, "spacing": {"md": "16px"}}
        ts = e.extract(json.dumps(data), "json")
        assert ts.color["primary"] == "#6366f1"
        assert ts.spacing["md"] == "16px"


class TestFigma:
    def test_basic_figma(self) -> None:
        e = TokenExtractor()
        figma = json.dumps(
            {
                "colors": [
                    {"name": "primary/500", "color": {"r": 0.4, "g": 0.5, "b": 0.9, "a": 1.0}}
                ]
            }
        )
        ts = e.extract(figma, "figma")
        assert "primary/500" in ts.color
        # 0.4 * 255 = 102, 0.5 * 255 = 127.5 → 128, 0.9 * 255 = 229.5 → 230
        hex_value = ts.color["primary/500"]
        assert hex_value.lower().startswith("#")

    def test_export_figma(self) -> None:
        e = TokenExtractor()
        ts = TokenSet(source_format="css", color={"primary-500": "#6366f1"})
        out = e.export_figma(ts)
        data = json.loads(out)
        assert "colors" in data
        assert data["colors"][0]["name"] == "primary-500"
        assert "r" in data["colors"][0]["color"]


class TestScss:
    def test_scss_same_as_css(self) -> None:
        e = TokenExtractor()
        ts = e.extract("--color-x: #fff;", "scss")
        assert "color-x" in ts.color


class TestErrors:
    def test_unknown_format(self) -> None:
        e = TokenExtractor()
        with pytest.raises(ValueError):
            e.extract("x", source_format="pascal")

    def test_supported_formats(self) -> None:
        assert "css" in SUPPORTED_FORMATS
        assert "figma" in SUPPORTED_FORMATS


class TestHelpers:
    def test_hex_to_rgba(self) -> None:
        e = TokenExtractor()
        rgba = e._hex_to_rgba("#6366f1")
        assert 0.0 < rgba["r"] < 1.0
        assert rgba["a"] == 1.0

    def test_rgba_to_hex(self) -> None:
        e = TokenExtractor()
        hex_value = e._rgba_to_hex(0.4, 0.5, 0.9, 1.0)
        assert hex_value.startswith("#")
        assert len(hex_value) == 7
