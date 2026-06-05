"""Tests for shell scripts (smoke tests).

Docs: tests/test_scripts.doc.md
"""
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"


def _run_script(name: str, *args: str, env: dict | None = None) -> subprocess.CompletedProcess:
    script = SCRIPTS_DIR / name
    assert script.exists(), f"Script not found: {script}"
    full_env = os.environ.copy()
    full_env["PYTHONPATH"] = str(REPO_ROOT / "src")
    if env:
        full_env.update(env)
    return subprocess.run(
        ["bash", str(script), *args],
        capture_output=True,
        text=True,
        env=full_env,
        timeout=30,
    )


class TestDesignLoad:
    def test_load_default(self) -> None:
        result = _run_script("design-load.sh", "--json")
        assert result.returncode == 0
        assert "philosophy" in result.stdout

    def test_load_named(self) -> None:
        result = _run_script("design-load.sh", "--name=default", "--json")
        assert result.returncode == 0


class TestDesignComponent:
    def test_button(self) -> None:
        result = _run_script("design-component.sh", "button", "--framework=react")
        assert result.returncode == 0
        assert "Button" in result.stdout

    def test_input(self) -> None:
        result = _run_script("design-component.sh", "input", "--framework=html", "--placeholder=Email")
        assert result.returncode == 0
        assert "Input" in result.stdout

    def test_card(self) -> None:
        result = _run_script("design-component.sh", "card", "--framework=html")
        assert result.returncode == 0
        assert "Card" in result.stdout

    def test_modal(self) -> None:
        result = _run_script("design-component.sh", "modal", "--framework=react")
        assert result.returncode == 0
        assert "Modal" in result.stdout

    def test_unknown_component(self) -> None:
        result = _run_script("design-component.sh", "navbar")
        assert result.returncode != 0

    def test_no_args(self) -> None:
        result = _run_script("design-component.sh")
        assert result.returncode != 0


class TestDesignPage:
    def test_landing(self) -> None:
        result = _run_script("design-page.sh", "landing", "--framework=html")
        assert result.returncode == 0
        assert "hero" in result.stdout

    def test_pricing(self) -> None:
        result = _run_script("design-page.sh", "pricing", "--framework=html")
        assert result.returncode == 0
        assert "pricing" in result.stdout

    def test_no_args(self) -> None:
        result = _run_script("design-page.sh")
        assert result.returncode != 0


class TestDesignReview:
    def test_stdin(self) -> None:
        result = subprocess.run(
            ["bash", str(SCRIPTS_DIR / "design-review.sh"), "-"],
            input="body { color: #18181b; padding: 16px; }",
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONPATH": str(REPO_ROOT / "src")},
            timeout=30,
        )
        assert result.returncode == 0
        assert "ok" in result.stdout


class TestDesignTokens:
    def test_css(self, tmp_path: Path) -> None:
        css_file = tmp_path / "tokens.css"
        css_file.write_text("--color-primary-500: #6366f1;")
        result = _run_script("design-tokens.sh", str(css_file), "--format=css")
        assert result.returncode == 0
        assert "color-primary-500" in result.stdout

    def test_missing_file(self) -> None:
        result = _run_script("design-tokens.sh", "/tmp/missing.css")
        assert result.returncode != 0


class TestDesignA11y:
    def test_clean_html(self, tmp_path: Path) -> None:
        html_file = tmp_path / "clean.html"
        html_file.write_text(
            "<html lang='en'><head><title>Hi</title></head><body><h1>A</h1></body></html>"
        )
        result = _run_script("design-a11y.sh", str(html_file))
        assert result.returncode == 0
        assert "ok" in result.stdout

    def test_with_contrast(self, tmp_path: Path) -> None:
        html_file = tmp_path / "page.html"
        html_file.write_text(
            "<html lang='en'><head><title>Hi</title></head><body></body></html>"
        )
        result = _run_script(
            "design-a11y.sh",
            str(html_file),
            "--fg=#000000",
            "--bg=#ffffff",
        )
        assert result.returncode == 0
        assert "contrast" in result.stdout
