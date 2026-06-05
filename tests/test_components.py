"""Tests for ComponentGenerator.

Docs: tests/test_components.doc.md
"""
import pytest

from sin_frontend_design.components import (
    ComponentGenerator,
    ComponentSpec,
    SUPPORTED_FRAMEWORKS,
    SUPPORTED_SIZES,
    SUPPORTED_VARIANTS,
)


class TestButton:
    def test_button_default(self) -> None:
        g = ComponentGenerator()
        spec = g.button()
        assert spec.name == "Button"
        assert spec.framework == "react"
        assert spec.variant == "primary"
        assert spec.size == "md"

    def test_button_label(self) -> None:
        g = ComponentGenerator()
        spec = g.button(label="Save")
        assert "Save" in spec.code or spec.props["label"]["default"] == "Save"

    def test_button_size_lg(self) -> None:
        g = ComponentGenerator()
        spec = g.button(size="lg")
        assert spec.size == "lg"

    def test_button_framework_html(self) -> None:
        g = ComponentGenerator()
        spec = g.button(framework="html")
        assert "<button" in spec.code

    def test_button_framework_vue(self) -> None:
        g = ComponentGenerator()
        spec = g.button(framework="vue")
        assert "<template>" in spec.code

    def test_button_framework_svelte(self) -> None:
        g = ComponentGenerator()
        spec = g.button(framework="svelte")
        assert "<script>" in spec.code

    def test_button_invalid_framework(self) -> None:
        g = ComponentGenerator()
        with pytest.raises(ValueError):
            g.button(framework="angular")

    def test_button_invalid_variant(self) -> None:
        g = ComponentGenerator()
        with pytest.raises(ValueError):
            g.button(variant="neon")

    def test_button_invalid_size(self) -> None:
        g = ComponentGenerator()
        with pytest.raises(ValueError):
            g.button(size="huge")

    def test_button_a11y_notes(self) -> None:
        g = ComponentGenerator()
        spec = g.button()
        assert any("button" in note.lower() for note in spec.a11y)

    def test_button_to_dict(self) -> None:
        g = ComponentGenerator()
        spec = g.button()
        d = spec.to_dict()
        assert d["name"] == "Button"
        assert "tokens_used" in d


class TestInput:
    def test_input_default(self) -> None:
        g = ComponentGenerator()
        spec = g.input()
        assert spec.name == "Input"

    def test_input_placeholder(self) -> None:
        g = ComponentGenerator()
        spec = g.input(placeholder="Email")
        assert spec.props["placeholder"]["default"] == "Email"

    def test_input_type_email(self) -> None:
        g = ComponentGenerator()
        spec = g.input(input_type="email")
        assert spec.props["type"]["default"] == "email"

    def test_input_a11y_label_rule(self) -> None:
        g = ComponentGenerator()
        spec = g.input()
        assert any("label" in note.lower() for note in spec.a11y)

    def test_input_invalid_framework(self) -> None:
        g = ComponentGenerator()
        with pytest.raises(ValueError):
            g.input(framework="angular")


class TestCard:
    def test_card_default(self) -> None:
        g = ComponentGenerator()
        spec = g.card()
        assert spec.name == "Card"

    def test_card_title(self) -> None:
        g = ComponentGenerator()
        spec = g.card(title="Hello")
        assert "Hello" in spec.code or spec.props["title"]["default"] == "Hello"

    def test_card_a11y_heading_rule(self) -> None:
        g = ComponentGenerator()
        spec = g.card()
        assert any("heading" in note.lower() or "h3" in note.lower() for note in spec.a11y)


class TestModal:
    def test_modal_default(self) -> None:
        g = ComponentGenerator()
        spec = g.modal()
        assert spec.name == "Modal"

    def test_modal_a11y_focus_trap(self) -> None:
        g = ComponentGenerator()
        spec = g.modal()
        assert any("focus" in note.lower() for note in spec.a11y)

    def test_modal_a11y_escape(self) -> None:
        g = ComponentGenerator()
        spec = g.modal()
        assert any("escape" in note.lower() for note in spec.a11y)


class TestGenerate:
    def test_generate_button(self) -> None:
        g = ComponentGenerator()
        spec = g.generate("button", framework="react", variant="primary", size="md", label="Go")
        assert spec.name == "Button"

    def test_generate_unknown(self) -> None:
        g = ComponentGenerator()
        with pytest.raises(ValueError):
            g.generate("navbar")


class TestSupportedSets:
    def test_frameworks(self) -> None:
        assert "react" in SUPPORTED_FRAMEWORKS
        assert "html" in SUPPORTED_FRAMEWORKS

    def test_variants(self) -> None:
        assert "primary" in SUPPORTED_VARIANTS
        assert "danger" in SUPPORTED_VARIANTS

    def test_sizes(self) -> None:
        assert "xs" in SUPPORTED_SIZES
        assert "xl" in SUPPORTED_SIZES
