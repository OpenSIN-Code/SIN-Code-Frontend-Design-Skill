"""Tests for PageScaffolder.

Docs: test_pages.doc.md
"""
import pytest

from sin_frontend_design.pages import (
    PageScaffolder,
    SUPPORTED_LAYOUTS,
    SUPPORTED_SECTIONS,
)


class TestScaffold:
    def test_default_landing(self) -> None:
        s = PageScaffolder()
        page = s.scaffold()
        assert page.layout == "landing"
        assert page.framework == "html"
        assert any(sec.kind == "hero" for sec in page.sections)

    def test_landing_sections(self) -> None:
        s = PageScaffolder()
        page = s.scaffold(layout="landing")
        kinds = [sec.kind for sec in page.sections]
        assert "hero" in kinds
        assert "features" in kinds
        assert "cta" in kinds
        assert "footer" in kinds

    def test_pricing_sections(self) -> None:
        s = PageScaffolder()
        page = s.scaffold(layout="pricing")
        kinds = [sec.kind for sec in page.sections]
        assert "pricing" in kinds
        assert "faq" in kinds

    def test_docs_sections(self) -> None:
        s = PageScaffolder()
        page = s.scaffold(layout="docs")
        kinds = [sec.kind for sec in page.sections]
        assert "hero" in kinds
        assert "features" in kinds

    def test_blog_sections(self) -> None:
        s = PageScaffolder()
        page = s.scaffold(layout="blog")
        kinds = [sec.kind for sec in page.sections]
        assert "hero" in kinds

    def test_unknown_layout(self) -> None:
        s = PageScaffolder()
        with pytest.raises(ValueError):
            s.scaffold(layout="storefront")

    def test_unknown_framework(self) -> None:
        s = PageScaffolder()
        with pytest.raises(ValueError):
            s.scaffold(framework="angular")

    def test_overrides(self) -> None:
        s = PageScaffolder()
        page = s.scaffold(
            layout="landing",
            overrides={"hero": {"headline": "Custom Headline"}},
        )
        hero = next(sec for sec in page.sections if sec.kind == "hero")
        assert hero.content["headline"] == "Custom Headline"

    def test_tokens_unique(self) -> None:
        s = PageScaffolder()
        page = s.scaffold(layout="landing")
        assert len(page.tokens_used) == len(set(page.tokens_used))

    def test_to_dict(self) -> None:
        s = PageScaffolder()
        page = s.scaffold()
        d = page.to_dict()
        assert "sections" in d
        assert "code" in d


class TestFrameworks:
    def test_html_output(self) -> None:
        s = PageScaffolder()
        page = s.scaffold(framework="html")
        assert "<!doctype html>" in page.code
        assert "<html lang='en'>" in page.code

    def test_react_output(self) -> None:
        s = PageScaffolder()
        page = s.scaffold(framework="react")
        assert "export default function" in page.code

    def test_vue_output(self) -> None:
        s = PageScaffolder()
        page = s.scaffold(framework="vue")
        assert "<template>" in page.code

    def test_svelte_output(self) -> None:
        s = PageScaffolder()
        page = s.scaffold(framework="svelte")
        assert "<main>" in page.code


class TestSections:
    def test_hero_section(self) -> None:
        s = PageScaffolder()
        section = s.hero(layout="landing", headline="Hi")
        assert section.kind == "hero"
        assert section.content["headline"] == "Hi"

    def test_features_with_items(self) -> None:
        s = PageScaffolder()
        section = s.features(layout="landing", items=[{"title": "A", "body": "B"}])
        assert section.content["items"][0]["title"] == "A"

    def test_pricing_with_tiers(self) -> None:
        s = PageScaffolder()
        section = s.pricing(layout="pricing", tiers=[{"name": "Free", "price": "$0", "features": ["x"]}])
        assert section.content["tiers"][0]["name"] == "Free"

    def test_footer_with_links(self) -> None:
        s = PageScaffolder()
        section = s.footer(layout="landing", links=["a", "b"])
        assert section.content["links"] == ["a", "b"]

    def test_testimonials_with_items(self) -> None:
        s = PageScaffolder()
        section = s.testimonials(layout="landing", items=[{"quote": "x", "author": "y"}])
        assert section.content["items"][0]["author"] == "y"

    def test_faq_with_items(self) -> None:
        s = PageScaffolder()
        section = s.faq(layout="pricing", items=[{"q": "?", "a": "!"}])
        assert section.content["items"][0]["a"] == "!"

    def test_cta_with_headline(self) -> None:
        s = PageScaffolder()
        section = s.cta(layout="landing", headline="Go", cta="Click")
        assert section.content["headline"] == "Go"
        assert section.content["cta"] == "Click"


class TestSupported:
    def test_supported_sections(self) -> None:
        assert "hero" in SUPPORTED_SECTIONS
        assert "footer" in SUPPORTED_SECTIONS

    def test_supported_layouts(self) -> None:
        assert "landing" in SUPPORTED_LAYOUTS
        assert "pricing" in SUPPORTED_LAYOUTS
