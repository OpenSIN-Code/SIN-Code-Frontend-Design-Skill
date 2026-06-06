"""Page scaffolder — composes pages from sections (hero, features, pricing, footer).

Docs: pages.doc.md
"""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


SUPPORTED_SECTIONS = ("hero", "features", "pricing", "cta", "footer", "testimonials", "faq")
SUPPORTED_LAYOUTS = ("landing", "pricing", "docs", "blog")


@dataclass
class PageSection:
    """A single page section with kind, content, and tokens."""

    kind: str
    content: Dict[str, Any] = field(default_factory=dict)
    tokens_used: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "kind": self.kind,
            "content": self.content,
            "tokens_used": self.tokens_used,
        }


@dataclass
class PageScaffold:
    """A full page spec: layout, sections, tokens, code."""

    layout: str
    framework: str
    title: str
    sections: List[PageSection] = field(default_factory=list)
    tokens_used: List[str] = field(default_factory=list)
    code: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "layout": self.layout,
            "framework": self.framework,
            "title": self.title,
            "sections": [s.to_dict() for s in self.sections],
            "tokens_used": self.tokens_used,
            "code": self.code,
        }


class PageScaffolder:
    """Scaffold a page from a layout + custom content.

    Each layout has a default section recipe; you can override any section's content.
    """

    LAYOUTS: Dict[str, List[str]] = {
        "landing": ["hero", "features", "testimonials", "cta", "footer"],
        "pricing": ["hero", "pricing", "faq", "footer"],
        "docs": ["hero", "features", "footer"],
        "blog": ["hero", "features", "footer"],
    }

    def __init__(self) -> None:
        self._templates = self._build_templates()

    def _build_templates(self) -> Dict[str, Dict[str, Dict[str, Any]]]:
        return {
            "landing": {
                "hero": {
                    "headline": "Build something great.",
                    "subheadline": "The fastest way to ship a beautiful product.",
                    "cta_primary": "Get started",
                    "cta_secondary": "Learn more",
                },
                "features": {
                    "headline": "Everything you need",
                    "items": [
                        {"title": "Fast", "body": "Optimized for performance from day one."},
                        {"title": "Reliable", "body": "Battle-tested by thousands of teams."},
                        {"title": "Open", "body": "Open-source and extensible."},
                    ],
                },
                "testimonials": {
                    "headline": "Loved by builders",
                    "items": [
                        {"quote": "Saved us months of work.", "author": "Engineering Lead, Acme"},
                    ],
                },
                "cta": {
                    "headline": "Ready to start?",
                    "subheadline": "Join thousands of teams shipping faster.",
                    "cta": "Sign up",
                },
                "footer": {
                    "links": ["Privacy", "Terms", "Contact"],
                },
            },
            "pricing": {
                "hero": {
                    "headline": "Simple, fair pricing",
                    "subheadline": "Pay for what you use.",
                    "cta_primary": "Start free",
                },
                "pricing": {
                    "headline": "Plans",
                    "tiers": [
                        {"name": "Free", "price": "$0", "features": ["1 project", "Community support"]},
                        {"name": "Pro", "price": "$20/mo", "features": ["Unlimited projects", "Priority support"]},
                    ],
                },
                "faq": {
                    "headline": "Frequently asked",
                    "items": [
                        {"q": "Can I cancel anytime?", "a": "Yes."},
                    ],
                },
                "footer": {"links": ["Privacy", "Terms", "Contact"]},
            },
            "docs": {
                "hero": {"headline": "Documentation", "subheadline": "Learn the basics in minutes."},
                "features": {
                    "headline": "Topics",
                    "items": [
                        {"title": "Getting started", "body": "Install and configure."},
                        {"title": "API reference", "body": "All endpoints."},
                    ],
                },
                "footer": {"links": ["Docs", "GitHub", "Discord"]},
            },
            "blog": {
                "hero": {"headline": "From the blog", "subheadline": "Latest news and updates."},
                "features": {
                    "headline": "Recent posts",
                    "items": [
                        {"title": "How we ship", "body": "A look at our release process."},
                    ],
                },
                "footer": {"links": ["RSS", "Twitter", "GitHub"]},
            },
        }

    def _default_content(self, layout: str, kind: str) -> Dict[str, Any]:
        if layout not in self.LAYOUTS:
            raise ValueError(f"Unknown layout: {layout}. Choose from {list(self.LAYOUTS.keys())}.")
        if kind not in SUPPORTED_SECTIONS:
            raise ValueError(f"Unknown section: {kind}. Choose from {SUPPORTED_SECTIONS}.")
        if kind not in self.LAYOUTS[layout]:
            raise ValueError(f"Section '{kind}' not allowed in layout '{layout}'.")
        return self._templates[layout][kind]

    def _tokens_for_section(self, kind: str) -> List[str]:
        return {
            "hero": ["color.primary.500", "typography.size-9 (60px)", "spacing.size-9 (96px)"],
            "features": ["color.neutral.50", "spacing.size-6 (24px)", "radius.card (16px)"],
            "pricing": ["color.primary.600", "spacing.size-8 (32px)", "radius.card (16px)"],
            "cta": ["color.primary.500", "color.neutral.50", "spacing.size-9 (96px)"],
            "footer": ["color.neutral.800", "color.neutral.400", "spacing.size-6 (24px)"],
            "testimonials": ["color.neutral.100", "spacing.size-4 (16px)", "radius.card (16px)"],
            "faq": ["color.neutral.100", "spacing.size-4 (16px)"],
        }.get(kind, [])

    def hero(self, layout: str = "landing", **content: Any) -> PageSection:
        base = self._default_content(layout, "hero")
        base.update(content)
        return PageSection(
            kind="hero",
            content=base,
            tokens_used=self._tokens_for_section("hero"),
        )

    def features(
        self,
        layout: str = "landing",
        items: Optional[List[Dict[str, str]]] = None,
        headline: Optional[str] = None,
    ) -> PageSection:
        base = self._default_content(layout, "features")
        if items is not None:
            base["items"] = items
        if headline is not None:
            base["headline"] = headline
        return PageSection(
            kind="features",
            content=base,
            tokens_used=self._tokens_for_section("features"),
        )

    def pricing(
        self,
        layout: str = "pricing",
        tiers: Optional[List[Dict[str, Any]]] = None,
        headline: Optional[str] = None,
    ) -> PageSection:
        base = self._default_content(layout, "pricing")
        if tiers is not None:
            base["tiers"] = tiers
        if headline is not None:
            base["headline"] = headline
        return PageSection(
            kind="pricing",
            content=base,
            tokens_used=self._tokens_for_section("pricing"),
        )

    def cta(
        self,
        layout: str = "landing",
        headline: Optional[str] = None,
        cta: Optional[str] = None,
    ) -> PageSection:
        base = self._default_content(layout, "cta")
        if headline is not None:
            base["headline"] = headline
        if cta is not None:
            base["cta"] = cta
        return PageSection(
            kind="cta",
            content=base,
            tokens_used=self._tokens_for_section("cta"),
        )

    def footer(
        self,
        layout: str = "landing",
        links: Optional[List[str]] = None,
    ) -> PageSection:
        base = self._default_content(layout, "footer")
        if links is not None:
            base["links"] = links
        return PageSection(
            kind="footer",
            content=base,
            tokens_used=self._tokens_for_section("footer"),
        )

    def testimonials(
        self,
        layout: str = "landing",
        items: Optional[List[Dict[str, str]]] = None,
    ) -> PageSection:
        base = self._default_content(layout, "testimonials")
        if items is not None:
            base["items"] = items
        return PageSection(
            kind="testimonials",
            content=base,
            tokens_used=self._tokens_for_section("testimonials"),
        )

    def faq(
        self,
        layout: str = "pricing",
        items: Optional[List[Dict[str, str]]] = None,
    ) -> PageSection:
        base = self._default_content(layout, "faq")
        if items is not None:
            base["items"] = items
        return PageSection(
            kind="faq",
            content=base,
            tokens_used=self._tokens_for_section("faq"),
        )

    def scaffold(
        self,
        layout: str = "landing",
        framework: str = "html",
        title: str = "Untitled page",
        overrides: Optional[Dict[str, Dict[str, Any]]] = None,
    ) -> PageScaffold:
        """Build a complete page scaffold.

        Args:
            layout: One of landing/pricing/docs/blog.
            framework: Target framework (html|react|vue|svelte).
            title: Page <title>.
            overrides: Map of section-kind → content overrides.
        """
        if layout not in self.LAYOUTS:
            raise ValueError(f"Unknown layout: {layout}.")
        if framework not in ("html", "react", "vue", "svelte"):
            raise ValueError(f"Unsupported framework: {framework}.")
        overrides = overrides or {}
        sections: List[PageSection] = []
        all_tokens: List[str] = []
        for kind in self.LAYOUTS[layout]:
            content = self._default_content(layout, kind)
            if kind in overrides:
                content = {**content, **overrides[kind]}
            section = PageSection(
                kind=kind,
                content=content,
                tokens_used=self._tokens_for_section(kind),
            )
            sections.append(section)
            all_tokens.extend(section.tokens_used)
        # Stable unique tokens.
        seen = set()
        unique_tokens: List[str] = []
        for tok in all_tokens:
            if tok not in seen:
                unique_tokens.append(tok)
                seen.add(tok)
        code = self._render(layout, framework, title, sections)
        return PageScaffold(
            layout=layout,
            framework=framework,
            title=title,
            sections=sections,
            tokens_used=unique_tokens,
            code=code,
        )

    def _render(
        self,
        layout: str,
        framework: str,
        title: str,
        sections: List[PageSection],
    ) -> str:
        body_parts: List[str] = []
        for s in sections:
            body_parts.append(self._render_section(s, framework))
        body = "\n".join(body_parts)
        if framework == "html":
            return (
                f"<!doctype html>\n"
                f"<html lang='en'>\n"
                f"<head>\n"
                f"  <meta charset='utf-8'>\n"
                f"  <title>{title}</title>\n"
                f"  <meta name='viewport' content='width=device-width, initial-scale=1'>\n"
                f"  <link rel='stylesheet' href='/design-system.css'>\n"
                f"</head>\n"
                f"<body>\n"
                f"{body}\n"
                f"</body>\n"
                f"</html>\n"
            )
        if framework == "react":
            return (
                f"// React page: layout={layout}, title={title}\n"
                f"export default function Page() {{\n"
                f"  return (\n"
                f"    <main>\n"
                f"      {body.replace('\\n', '\\n      ')}\n"
                f"    </main>\n"
                f"  );\n"
                f"}}\n"
            )
        if framework == "vue":
            return (
                f"<template>\n"
                f"  <main>\n"
                f"    {body.replace(chr(10), chr(10) + '    ')}\n"
                f"  </main>\n"
                f"</template>\n"
                f"<script setup>\n"
                f"// layout={layout}, title={title}\n"
                f"</script>\n"
            )
        return (
            f"<!-- Svelte page: layout={layout}, title={title} -->\n"
            f"<main>\n"
            f"  {body.replace(chr(10), chr(10) + '  ')}\n"
            f"</main>\n"
        )

    def _render_section(self, section: PageSection, framework: str) -> str:
        c = section.content
        kind = section.kind
        if kind == "hero":
            return self._hero_html(c, framework)
        if kind == "features":
            return self._features_html(c, framework)
        if kind == "pricing":
            return self._pricing_html(c, framework)
        if kind == "cta":
            return self._cta_html(c, framework)
        if kind == "footer":
            return self._footer_html(c, framework)
        if kind == "testimonials":
            return self._testimonials_html(c, framework)
        if kind == "faq":
            return self._faq_html(c, framework)
        return f"<!-- unknown section: {kind} -->"

    def _hero_html(self, c: Dict[str, Any], framework: str) -> str:
        return (
            "<section class='hero'>\n"
            f"  <h1>{c.get('headline', '')}</h1>\n"
            f"  <p>{c.get('subheadline', '')}</p>\n"
            f"  <a class='btn primary' href='#'>{c.get('cta_primary', 'Get started')}</a>\n"
            f"</section>\n"
        )

    def _features_html(self, c: Dict[str, Any], framework: str) -> str:
        items_html = "\n".join(
            f"    <div class='card'><h3>{it.get('title', '')}</h3><p>{it.get('body', '')}</p></div>"
            for it in c.get("items", [])
        )
        return (
            "<section class='features'>\n"
            f"  <h2>{c.get('headline', 'Features')}</h2>\n"
            "  <div class='grid'>\n"
            f"{items_html}\n"
            "  </div>\n"
            "</section>\n"
        )

    def _pricing_html(self, c: Dict[str, Any], framework: str) -> str:
        tiers_html = "\n".join(
            f"    <div class='card'><h3>{t.get('name', '')}</h3>"
            f"<p class='price'>{t.get('price', '')}</p>"
            f"<ul>{''.join(f'<li>{f}</li>' for f in t.get('features', []))}</ul></div>"
            for t in c.get("tiers", [])
        )
        return (
            "<section class='pricing'>\n"
            f"  <h2>{c.get('headline', 'Plans')}</h2>\n"
            "  <div class='grid'>\n"
            f"{tiers_html}\n"
            "  </div>\n"
            "</section>\n"
        )

    def _cta_html(self, c: Dict[str, Any], framework: str) -> str:
        return (
            "<section class='cta'>\n"
            f"  <h2>{c.get('headline', '')}</h2>\n"
            f"  <p>{c.get('subheadline', '')}</p>\n"
            f"  <a class='btn primary' href='#'>{c.get('cta', 'Sign up')}</a>\n"
            f"</section>\n"
        )

    def _footer_html(self, c: Dict[str, Any], framework: str) -> str:
        links_html = "\n".join(f"    <a href='#'>{link}</a>" for link in c.get("links", []))
        return (
            "<footer class='footer'>\n"
            f"  <nav>\n{links_html}\n  </nav>\n"
            f"</footer>\n"
        )

    def _testimonials_html(self, c: Dict[str, Any], framework: str) -> str:
        items_html = "\n".join(
            f"    <blockquote><p>\"{it.get('quote', '')}\"</p><cite>— {it.get('author', '')}</cite></blockquote>"
            for it in c.get("items", [])
        )
        return (
            "<section class='testimonials'>\n"
            f"  <h2>{c.get('headline', 'Loved by builders')}</h2>\n"
            f"{items_html}\n"
            f"</section>\n"
        )

    def _faq_html(self, c: Dict[str, Any], framework: str) -> str:
        items_html = "\n".join(
            f"    <details><summary>{it.get('q', '')}</summary><p>{it.get('a', '')}</p></details>"
            for it in c.get("items", [])
        )
        return (
            "<section class='faq'>\n"
            f"  <h2>{c.get('headline', 'FAQ')}</h2>\n"
            f"{items_html}\n"
            f"</section>\n"
        )
