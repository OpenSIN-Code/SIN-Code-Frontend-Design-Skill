"""Tests for FastMCP server.

Docs: test_server.doc.md
"""
import json
from pathlib import Path
from typing import Generator
from unittest.mock import patch, Mock

import pytest

from sin_frontend_design.mcp_server import mcp  # type: ignore  # noqa
import sin_frontend_design.mcp_server as server_mod


def _tool_names() -> list:
    """Return list of tool names registered on the FastMCP server."""
    keys = list(mcp._local_provider._components.keys())  # type: ignore[attr-defined]
    names: list = []
    for k in keys:
        if k.startswith("tool:"):
            cleaned = k.replace("tool:", "").replace("@", "")
            names.append(cleaned)
    return names


class TestToolsRegistered:
    def test_design_system_load(self) -> None:
        assert "design_system_load" in _tool_names()

    def test_design_component_create(self) -> None:
        assert "design_component_create" in _tool_names()

    def test_design_page_scaffold(self) -> None:
        assert "design_page_scaffold" in _tool_names()

    def test_design_review(self) -> None:
        assert "design_review" in _tool_names()

    def test_design_token_extract(self) -> None:
        assert "design_token_extract" in _tool_names()

    def test_design_a11y_check(self) -> None:
        assert "design_a11y_check" in _tool_names()

    def test_design_responsive_test(self) -> None:
        assert "design_responsive_test" in _tool_names()

    def test_design_figma_export(self) -> None:
        assert "design_figma_export" in _tool_names()


class TestDesignSystemLoad:
    def test_returns_tokens(self) -> None:
        result = json.loads(server_mod.design_system_load())
        assert "tokens" in result
        assert "themes" in result
        assert "philosophy" in result

    def test_named(self) -> None:
        result = json.loads(server_mod.design_system_load(name="default"))
        assert "tokens" in result


class TestDesignComponentCreate:
    def test_button(self) -> None:
        result = json.loads(
            server_mod.design_component_create(
                component="button",
                framework="react",
                variant="primary",
                size="md",
                use_v0=False,
                label="Save",
                placeholder="",
                title="",
            )
        )
        assert result["name"] == "Button"
        assert result["framework"] == "react"

    def test_input(self) -> None:
        result = json.loads(
            server_mod.design_component_create(
                component="input",
                framework="html",
                variant="primary",
                size="md",
                use_v0=False,
                label="",
                placeholder="Email",
                title="",
            )
        )
        assert result["name"] == "Input"

    def test_use_v0_falls_back(self) -> None:
        # use_v0=True but v0 pool is offline (or mocked out) — fall back to templates.
        with patch.object(server_mod, "_v0_generate", return_value=None):
            result = json.loads(
                server_mod.design_component_create(
                    component="button",
                    framework="react",
                    variant="primary",
                    size="md",
                    use_v0=True,
                    label="",
                    placeholder="",
                    title="",
                )
            )
            assert result["name"] == "Button"

    def test_use_v0_returns_v0_code(self) -> None:
        with patch.object(server_mod, "_v0_generate", return_value="// v0 code"):
            result = json.loads(
                server_mod.design_component_create(
                    component="button",
                    framework="react",
                    variant="primary",
                    size="md",
                    use_v0=True,
                    label="",
                    placeholder="",
                    title="",
                )
            )
            assert "v0" in result["code"]


class TestDesignPageScaffold:
    def test_landing(self) -> None:
        result = json.loads(
            server_mod.design_page_scaffold(
                layout="landing", framework="html", title="T"
            )
        )
        assert result["layout"] == "landing"
        assert len(result["sections"]) > 0


class TestDesignReview:
    def test_clean_code(self) -> None:
        result = json.loads(
            server_mod.design_review(code="body { color: #18181b; padding: 16px; }")
        )
        assert result["ok"] is True


class TestDesignTokenExtract:
    def test_css(self) -> None:
        result = json.loads(
            server_mod.design_token_extract(
                source="--color-primary-500: #6366f1;", source_format="css"
            )
        )
        assert "color-primary-500" in result["color"]


class TestDesignA11yCheck:
    def test_clean_html(self) -> None:
        code = (
            "<html lang='en'><head><title>Hi</title></head>"
            "<body><h1>A</h1></body></html>"
        )
        result = json.loads(
            server_mod.design_a11y_check(code=code, foreground="", background="")
        )
        assert result["ok"] is True

    def test_contrast(self) -> None:
        result = json.loads(
            server_mod.design_a11y_check(
                code="<html lang='en'><head><title>Hi</title></head><body></body></html>",
                foreground="#000000",
                background="#ffffff",
            )
        )
        assert "contrast" in result
        assert result["contrast"]["ratio"] == 21.0


class TestDesignResponsiveTest:
    def test_desktop(self) -> None:
        result = json.loads(
            server_mod.design_responsive_test(viewport_width=1280, include_css=True)
        )
        assert result["current_breakpoint"] == "lg"
        assert "css" in result

    def test_no_css(self) -> None:
        result = json.loads(
            server_mod.design_responsive_test(viewport_width=360, include_css=False)
        )
        assert result["current_breakpoint"] == "xs"
        assert "css" not in result


class TestDesignFigmaExport:
    def test_export(self) -> None:
        result = json.loads(
            server_mod.design_figma_export(
                source="--color-primary-500: #6366f1;", source_format="css"
            )
        )
        assert "colors" in result
        assert result["colors"][0]["name"] == "color-primary-500"
