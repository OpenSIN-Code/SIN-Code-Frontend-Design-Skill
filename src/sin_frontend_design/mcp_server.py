"""FastMCP server exposing frontend design tools.

Docs: src/sin_frontend_design/mcp_server.doc.md
"""
import json
import os
from typing import Any, Dict, List, Optional

import requests
from fastmcp import FastMCP

from .a11y import A11yChecker
from .components import ComponentGenerator
from .pages import PageScaffolder
from .responsive import BreakpointGenerator
from .reviewer import DesignReviewer
from .system import DesignSystem
from .tokens import TokenExtractor

mcp = FastMCP("sin-frontend-design")

V0_BASE_URL = os.environ.get("V0_BASE_URL", "http://localhost:27401/v1")
V0_API_KEY = os.environ.get("V0_API_KEY", "dummy-key")
V0_LARGE_MODEL = "v0-1.5-lg"
V0_MEDIUM_MODEL = "v0-1.5-md"
V0_TIMEOUT = int(os.environ.get("V0_TIMEOUT", "30"))


def _v0_generate(prompt: str, complexity: str = "medium") -> Optional[str]:
    """Call v0 API to generate code. Returns None on failure.

    Uses v0-large for complex prompts (>200 chars), v0-medium otherwise.
    Falls back to None if the v0 pool is offline.
    """
    model = V0_LARGE_MODEL if (complexity == "complex" or len(prompt) > 200) else V0_MEDIUM_MODEL
    try:
        resp = requests.post(
            f"{V0_BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {V0_API_KEY}", "Content-Type": "application/json"},
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are a SOTA frontend engineer. Output only valid code."},
                    {"role": "user", "content": prompt},
                ],
                "max_tokens": 4096,
            },
            timeout=V0_TIMEOUT,
        )
        if resp.status_code == 200:
            data = resp.json()
            return data.get("choices", [{}])[0].get("message", {}).get("content")
    except (requests.RequestException, ValueError, KeyError):
        return None
    return None


@mcp.tool()
def design_system_load(name: str = "default") -> str:
    """Load the SOTA design system (typography, color, spacing, motion, philosophy).

    Args:
        name: Design system name (default = built-in SOTA tokens).

    Returns:
        JSON string with the full design system payload.
    """
    system = DesignSystem()
    return json.dumps(system.load(name), default=str)


@mcp.tool()
def design_component_create(
    component: str,
    framework: str = "react",
    variant: str = "primary",
    size: str = "md",
    use_v0: bool = False,
    label: str = "",
    placeholder: str = "",
    title: str = "",
) -> str:
    """Generate a UI component spec (button, input, card, modal).

    Args:
        component: Component name (button|input|card|modal).
        framework: Target framework (react|vue|svelte|html).
        variant: Visual variant (primary|secondary|ghost|outline|danger).
        size: Size token (xs|sm|md|lg|xl).
        use_v0: If true, attempt v0 code generation first; fall back to templates.
        label: Button label (for button).
        placeholder: Input placeholder (for input).
        title: Modal/card title.

    Returns:
        JSON string with ComponentSpec fields (tokens_used, props, a11y, code).
    """
    generator = ComponentGenerator()
    kwargs: Dict[str, Any] = {}
    if component.lower() == "button" and label:
        kwargs["label"] = label
    if component.lower() == "input" and placeholder:
        kwargs["placeholder"] = placeholder
    if component.lower() in {"card", "modal"} and title:
        kwargs["title"] = title
    spec = generator.generate(component, framework=framework, variant=variant, size=size, **kwargs)

    if use_v0:
        prompt = (
            f"Generate a {component} component in {framework} matching this spec:\n"
            f"Variant: {variant}\nSize: {size}\n"
            f"Tokens: {', '.join(spec.tokens_used)}\n"
            f"Props: {json.dumps(spec.props)}\n"
            f"Use these design tokens: var(--color-primary-500), var(--color-neutral-50), "
            f"var(--radius-default), 4px-grid spacing, 200ms ease-out motion."
        )
        v0_code = _v0_generate(prompt, complexity="complex" if len(prompt) > 200 else "medium")
        if v0_code:
            spec.code = v0_code
            spec.tokens_used.append("source:v0")
    return json.dumps(spec.to_dict(), default=str)


@mcp.tool()
def design_page_scaffold(
    layout: str = "landing",
    framework: str = "html",
    title: str = "Untitled page",
) -> str:
    """Scaffold a full page with sections (hero, features, pricing, cta, footer).

    Args:
        layout: Page layout (landing|pricing|docs|blog).
        framework: Target framework (html|react|vue|svelte).
        title: Page title.

    Returns:
        JSON string with PageScaffold (layout, framework, title, sections, code).
    """
    scaffolder = PageScaffolder()
    page = scaffolder.scaffold(layout=layout, framework=framework, title=title)
    return json.dumps(page.to_dict(), default=str)


@mcp.tool()
def design_review(code: str) -> str:
    """Review existing UI code for design system consistency.

    Args:
        code: Source code to review (HTML/CSS/JSX/TSX).

    Returns:
        JSON string with ReviewReport (ok, score, findings).
    """
    reviewer = DesignReviewer()
    report = reviewer.review(code)
    return json.dumps(report.to_dict(), default=str)


@mcp.tool()
def design_token_extract(source: str, source_format: str = "css") -> str:
    """Extract design tokens from existing code.

    Args:
        source: Source code to parse.
        source_format: Format hint (css|scss|tailwind|json|figma).

    Returns:
        JSON string with TokenSet (typography, color, spacing, radius, motion).
    """
    extractor = TokenExtractor()
    tokens = extractor.extract(source, source_format=source_format)
    return json.dumps(tokens.to_dict(), default=str)


@mcp.tool()
def design_a11y_check(code: str, foreground: str = "", background: str = "") -> str:
    """Check WCAG 2.2 AA compliance of HTML code.

    Args:
        code: HTML source to check.
        foreground: Optional foreground hex color for contrast check.
        background: Optional background hex color for contrast check.

    Returns:
        JSON string with A11yReport (ok, score, findings). If both
        foreground and background are provided, also includes contrast.
    """
    checker = A11yChecker()
    report = checker.check(code)
    if foreground and background:
        report.to_dict()  # No-op; ensure calls don't surprise in tests.
        # Embed contrast in the result.
        result = report.to_dict()
        result["contrast"] = checker.check_contrast(foreground, background)
        return json.dumps(result, default=str)
    return json.dumps(report.to_dict(), default=str)


@mcp.tool()
def design_responsive_test(viewport_width: int = 1024, include_css: bool = True) -> str:
    """Generate responsive breakpoints and identify current breakpoint.

    Args:
        viewport_width: Current viewport width in pixels.
        include_css: If true, include a full CSS payload.

    Returns:
        JSON string with current breakpoint, all breakpoints, and optional CSS.
    """
    generator = BreakpointGenerator()
    tokens = generator.tokens()
    current = generator.test(viewport_width)
    result: Dict[str, Any] = {
        "viewport_width": viewport_width,
        "current_breakpoint": current,
        "breakpoints": tokens.breakpoints,
        "container_max_widths": tokens.container_max_widths,
    }
    if include_css:
        result["css"] = generator.css()
    return json.dumps(result, default=str)


@mcp.tool()
def design_figma_export(source: str, source_format: str = "css") -> str:
    """Export extracted tokens to Figma Tokens JSON.

    Args:
        source: Source code with design tokens.
        source_format: Format of source (css|scss|tailwind|json|figma).

    Returns:
        JSON string in Figma Tokens format ({"colors": [{name, color: {r,g,b,a}}]}).
    """
    extractor = TokenExtractor()
    tokens = extractor.extract(source, source_format=source_format)
    return extractor.export_figma(tokens)


def main() -> None:
    """Entry point for the MCP server (`python -m sin_frontend_design.mcp_server`)."""
    mcp.run()


if __name__ == "__main__":
    main()
