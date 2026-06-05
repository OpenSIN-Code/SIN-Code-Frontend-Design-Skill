"""Tests for BreakpointGenerator.

Docs: tests/test_responsive.doc.md
"""
import pytest

from sin_frontend_design.responsive import (
    BreakpointGenerator,
    DEFAULT_BREAKPOINTS,
    ResponsiveTokens,
)


class TestBreakpoints:
    def test_default_count(self) -> None:
        gen = BreakpointGenerator()
        assert len(gen.breakpoints) == 6

    def test_default_names(self) -> None:
        gen = BreakpointGenerator()
        names = [bp["name"] for bp in gen.breakpoints]
        assert names == ["xs", "sm", "md", "lg", "xl", "2xl"]

    def test_default_constants(self) -> None:
        assert len(DEFAULT_BREAKPOINTS) == 6


class TestTokens:
    def test_returns_responsive_tokens(self) -> None:
        gen = BreakpointGenerator()
        tokens = gen.tokens()
        assert isinstance(tokens, ResponsiveTokens)

    def test_container_widths(self) -> None:
        gen = BreakpointGenerator()
        tokens = gen.tokens()
        assert tokens.container_max_widths["md"] == "720px"
        assert tokens.container_max_widths["2xl"] == "1320px"

    def test_fluid_typography(self) -> None:
        gen = BreakpointGenerator()
        tokens = gen.tokens()
        assert tokens.fluid_typography["min_size"] == 14
        assert tokens.fluid_typography["max_size"] == 18


class TestMediaQuery:
    def test_md_query(self) -> None:
        gen = BreakpointGenerator()
        q = gen.media_query("md")
        assert "@media" in q
        assert "768px" in q

    def test_xs_query(self) -> None:
        gen = BreakpointGenerator()
        q = gen.media_query("xs")
        # xs has min 0, so no @media.
        assert "@media" not in q

    def test_unknown_query(self) -> None:
        gen = BreakpointGenerator()
        with pytest.raises(ValueError):
            gen.media_query("xxl")

    def test_all_media_queries(self) -> None:
        gen = BreakpointGenerator()
        queries = gen.all_media_queries()
        assert "md" in queries
        assert "lg" in queries


class TestCSS:
    def test_css_has_root(self) -> None:
        gen = BreakpointGenerator()
        css = gen.css()
        assert ":root {" in css
        assert "--bp-md" in css
        assert "--container-lg" in css

    def test_css_has_media_queries(self) -> None:
        gen = BreakpointGenerator()
        css = gen.css()
        assert "@media" in css


class TestViewport:
    def test_phone(self) -> None:
        gen = BreakpointGenerator()
        assert gen.test(360) == "xs"

    def test_large_phone(self) -> None:
        gen = BreakpointGenerator()
        assert gen.test(700) == "sm"

    def test_tablet(self) -> None:
        gen = BreakpointGenerator()
        assert gen.test(900) == "md"

    def test_laptop(self) -> None:
        gen = BreakpointGenerator()
        assert gen.test(1280) == "lg"

    def test_desktop(self) -> None:
        gen = BreakpointGenerator()
        assert gen.test(1600) == "xl"

    def test_wide(self) -> None:
        gen = BreakpointGenerator()
        assert gen.test(2400) == "2xl"
