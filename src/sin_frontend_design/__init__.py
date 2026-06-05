"""sin-frontend-design package — SOTA design system + philosophy.

Docs: src/sin_frontend_design/__init__.doc.md
"""
from .a11y import A11yChecker, A11yFinding
from .components import ComponentGenerator, ComponentSpec
from .pages import PageScaffolder, PageSection
from .responsive import BreakpointGenerator, ResponsiveTokens
from .reviewer import DesignReviewer, ReviewFinding
from .system import DesignSystem, DesignTokens, Theme
from .tokens import TokenExtractor, TokenSet

__all__ = [
    "A11yChecker",
    "A11yFinding",
    "BreakpointGenerator",
    "ComponentGenerator",
    "ComponentSpec",
    "DesignReviewer",
    "DesignSystem",
    "DesignTokens",
    "PageScaffolder",
    "PageSection",
    "ResponsiveTokens",
    "ReviewFinding",
    "Theme",
    "TokenExtractor",
    "TokenSet",
]
