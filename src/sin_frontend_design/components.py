"""Component spec generator — produces UI specs for button, input, card, etc.

Docs: components.doc.md
"""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .system import DEFAULT_TOKENS, DesignSystem


SUPPORTED_FRAMEWORKS = ("react", "vue", "svelte", "html")
SUPPORTED_VARIANTS = ("primary", "secondary", "ghost", "outline", "danger")
SUPPORTED_SIZES = ("xs", "sm", "md", "lg", "xl")


@dataclass
class ComponentSpec:
    """A complete component specification with tokens, props, and code skeleton."""

    name: str
    framework: str
    variant: str
    size: str
    tokens_used: List[str] = field(default_factory=list)
    props: Dict[str, Any] = field(default_factory=dict)
    a11y: List[str] = field(default_factory=list)
    code: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "framework": self.framework,
            "variant": self.variant,
            "size": self.size,
            "tokens_used": self.tokens_used,
            "props": self.props,
            "a11y": self.a11y,
            "code": self.code,
        }


_BUTTON_TOKENS = {
    "padding_x": "16",
    "padding_y": "8",
    "radius": "default",
    "font_size": "size-2",
    "font_weight": 500,
    "transition_ms": 200,
}

_INPUT_TOKENS = {
    "padding_x": "12",
    "padding_y": "8",
    "radius": "default",
    "font_size": "size-2",
    "border": "neutral-300",
    "focus_ring": "primary-500",
}

_CARD_TOKENS = {
    "padding": "16",
    "radius": "card",
    "shadow": "0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.04)",
    "border": "neutral-200",
    "background": "neutral-50",
}

_MODAL_TOKENS = {
    "padding": "24",
    "radius": "card",
    "overlay": "rgba(0,0,0,0.5)",
    "z_index": 1000,
    "max_width": "512px",
}


class ComponentGenerator:
    """Generate UI component specs for React, Vue, Svelte, or HTML.

    Each generated spec contains:
    - tokens_used: explicit list of design tokens referenced
    - props: documented prop signatures
    - a11y: WCAG-relevant notes
    - code: a working code skeleton in the target framework
    """

    def __init__(self, system: Optional[DesignSystem] = None) -> None:
        self.system = system or DesignSystem()

    def _validate(self, framework: str, variant: str, size: str) -> None:
        if framework not in SUPPORTED_FRAMEWORKS:
            raise ValueError(
                f"Unsupported framework: {framework}. "
                f"Choose from {SUPPORTED_FRAMEWORKS}."
            )
        if variant not in SUPPORTED_VARIANTS:
            raise ValueError(
                f"Unsupported variant: {variant}. "
                f"Choose from {SUPPORTED_VARIANTS}."
            )
        if size not in SUPPORTED_SIZES:
            raise ValueError(
                f"Unsupported size: {size}. Choose from {SUPPORTED_SIZES}."
            )

    def _size_to_px(self, size: str) -> Dict[str, int]:
        """Map a size token to padding + font-size in px."""
        scale = {"xs": 2, "sm": 1, "md": 0, "lg": -1, "xl": -2}
        offset = scale[size]
        base_padding_x = 16
        base_padding_y = 8
        base_font = DEFAULT_TOKENS.typography["size-2"]
        step = 2
        return {
            "padding_x": base_padding_x + offset * step,
            "padding_y": max(2, base_padding_y + offset),
            "font_size": DEFAULT_TOKENS.typography[f"size-{2 + offset}"]
            if (2 + offset) >= 0
            else base_font,
        }

    def button(
        self,
        framework: str = "react",
        variant: str = "primary",
        size: str = "md",
        label: str = "Click me",
    ) -> ComponentSpec:
        """Generate a Button component spec."""
        self._validate(framework, variant, size)
        sizes = self._size_to_px(size)
        tokens = [
            "color.primary.500",
            "color.neutral.50",
            "spacing.size-2 (8px)",
            "radius.default (8px)",
            f"motion.duration.hover ({DEFAULT_TOKENS.motion['duration']['hover']}ms)",
        ]
        props = {
            "label": {"type": "string", "default": label, "required": True},
            "variant": {"type": "enum", "values": list(SUPPORTED_VARIANTS)},
            "size": {"type": "enum", "values": list(SUPPORTED_SIZES)},
            "disabled": {"type": "boolean", "default": False},
            "onClick": {"type": "function", "required": False},
        }
        a11y = [
            "Use <button> element (not <div>) for native keyboard support.",
            "Provide a discernible label (visible text or aria-label).",
            "Maintain 4.5:1 contrast for text vs background.",
            "Focus ring must be visible — never outline:none without replacement.",
            "Disabled buttons should still be focusable for screen readers.",
        ]
        code = self._button_code(framework, variant, size, sizes, label)
        return ComponentSpec(
            name="Button",
            framework=framework,
            variant=variant,
            size=size,
            tokens_used=tokens,
            props=props,
            a11y=a11y,
            code=code,
        )

    def _button_code(
        self,
        framework: str,
        variant: str,
        size: str,
        sizes: Dict[str, int],
        label: str,
    ) -> str:
        bg = {
            "primary": "var(--color-primary-500)",
            "secondary": "var(--color-secondary-500)",
            "ghost": "transparent",
            "outline": "transparent",
            "danger": "var(--color-error-500)",
        }[variant]
        fg = "var(--color-neutral-50)" if variant in {"primary", "secondary", "danger"} else "var(--color-primary-600)"
        border = (
            "1px solid var(--color-primary-500)" if variant == "outline" else "none"
        )
        transition = f"all {DEFAULT_TOKENS.motion['duration']['hover']}ms {DEFAULT_TOKENS.motion['easing']['hover']}"
        if framework == "react":
            return (
                "export function Button({ label, variant = 'primary', size = 'md', ...rest }) {\n"
                "  return (\n"
                "    <button\n"
                f"      style={{{{ background: '{bg}', color: '{fg}', border: '{border}',\n"
                f"        padding: '{sizes['padding_y']}px {sizes['padding_x']}px',\n"
                f"        borderRadius: 'var(--radius-default)',\n"
                f"        fontSize: '{sizes['font_size']}px', cursor: 'pointer',\n"
                f"        transition: '{transition}' }}}}\n"
                "      {...rest}\n"
                f"    >\n"
                f"      {{label || '{label}'}}\n"
                "    </button>\n"
                "  );\n"
                "}\n"
            )
        if framework == "vue":
            return (
                "<template>\n"
                "  <button :style=\"style\">{{ label }}</button>\n"
                "</template>\n"
                "<script setup>\n"
                "defineProps({ label: String })\n"
                f"const style = {{ background: '{bg}', color: '{fg}', border: '{border}',\n"
                f"  padding: '{sizes['padding_y']}px {sizes['padding_x']}px',\n"
                f"  borderRadius: 'var(--radius-default)', fontSize: '{sizes['font_size']}px',\n"
                f"  transition: '{transition}' }}\n"
                "</script>\n"
            )
        if framework == "svelte":
            return (
                "<script>\n"
                "  export let label = '{label}';\n"
                "</script>\n"
                f"<button style=\"background:{bg};color:{fg};border:{border};\n"
                f"  padding:{sizes['padding_y']}px {sizes['padding_x']}px;\n"
                f"  border-radius:var(--radius-default);font-size:{sizes['font_size']}px;\n"
                f"  transition:{transition}\">{{label}}</button>\n"
            )
        return (
            f'<button style="background:{bg};color:{fg};border:{border};\n'
            f'  padding:{sizes["padding_y"]}px {sizes["padding_x"]}px;\n'
            f'  border-radius:var(--radius-default);font-size:{sizes["font_size"]}px;\n'
            f'  transition:{transition}">{label}</button>\n'
        )

    def input(
        self,
        framework: str = "react",
        placeholder: str = "Type here...",
        input_type: str = "text",
    ) -> ComponentSpec:
        """Generate an Input component spec."""
        if framework not in SUPPORTED_FRAMEWORKS:
            raise ValueError(f"Unsupported framework: {framework}.")
        tokens = [
            "color.neutral.300 (border)",
            "color.primary.500 (focus ring)",
            "spacing.size-2 (8px)",
            "typography.size-2 (16px)",
        ]
        props = {
            "type": {"type": "string", "default": input_type, "values": ["text", "email", "password", "number", "search"]},
            "placeholder": {"type": "string", "default": placeholder},
            "value": {"type": "string", "required": False},
            "onChange": {"type": "function", "required": False},
            "disabled": {"type": "boolean", "default": False},
        }
        a11y = [
            "Always pair input with a <label> (htmlFor/id).",
            "Use aria-describedby for helper text and error messages.",
            "Use aria-invalid='true' for error state.",
            "Placeholder is NOT a substitute for label.",
            "Autocomplete attribute is encouraged for common input types.",
        ]
        code = self._input_code(framework, placeholder, input_type)
        return ComponentSpec(
            name="Input",
            framework=framework,
            variant="default",
            size="md",
            tokens_used=tokens,
            props=props,
            a11y=a11y,
            code=code,
        )

    def _input_code(self, framework: str, placeholder: str, input_type: str) -> str:
        style = (
            "padding:8px 12px;border:1px solid var(--color-neutral-300);"
            "border-radius:var(--radius-default);font-size:16px;"
            "outline:none;transition:border-color 200ms ease-out;"
        )
        if framework == "react":
            return (
                "export function Input({ type = 'text', placeholder, ...rest }) {\n"
                f"  return <input type={{type}} placeholder={{placeholder || '{placeholder}'}}\n"
                f"    style={{{{ {style} }}}} {{...rest}} />;\n"
                "}\n"
            )
        if framework == "vue":
            return (
                "<template>\n"
                f"  <input :type=\"type\" :placeholder=\"{placeholder}\" :style=\"style\" />\n"
                "</template>\n"
                "<script setup>\n"
                "defineProps({ type: { type: String, default: 'text' }, placeholder: String })\n"
                f"const style = '{style}'\n"
                "</script>\n"
            )
        if framework == "svelte":
            return (
                "<script>\n"
                "  export let type = 'text';\n"
                "  export let placeholder = '{placeholder}';\n"
                "</script>\n"
                f"<input {{type}} {{placeholder}} style=\"{style}\" />\n"
            )
        return f'<input type="{input_type}" placeholder="{placeholder}" style="{style}" />\n'

    def card(
        self,
        framework: str = "react",
        title: str = "Card title",
        body: str = "Card body content.",
    ) -> ComponentSpec:
        """Generate a Card component spec."""
        if framework not in SUPPORTED_FRAMEWORKS:
            raise ValueError(f"Unsupported framework: {framework}.")
        tokens = [
            "color.neutral.50 (background)",
            "color.neutral.200 (border)",
            "spacing.size-4 (16px)",
            "radius.card (16px)",
        ]
        props = {
            "title": {"type": "string", "default": title},
            "body": {"type": "string", "default": body},
            "footer": {"type": "node", "required": False},
        }
        a11y = [
            "If the card is interactive, wrap in <a> or <button> with role.",
            "Heading hierarchy: card title should use h3 or h4 by default.",
            "Avoid link nesting — don't put <a> inside <a>.",
        ]
        code = self._card_code(framework, title, body)
        return ComponentSpec(
            name="Card",
            framework=framework,
            variant="default",
            size="md",
            tokens_used=tokens,
            props=props,
            a11y=a11y,
            code=code,
        )

    def _card_code(self, framework: str, title: str, body: str) -> str:
        style = (
            "padding:16px;border:1px solid var(--color-neutral-200);"
            "border-radius:var(--radius-card);background:var(--color-neutral-50);"
            "box-shadow:0 1px 3px rgba(0,0,0,0.08),0 1px 2px rgba(0,0,0,0.04);"
        )
        if framework == "react":
            return (
                "export function Card({ title, body, children }) {\n"
                f"  return (\n"
                f"    <div style={{{{ {style} }}}}>\n"
                f"      <h3 style={{{{ margin: 0, fontSize: '20px' }}}}>{{title || '{title}'}}</h3>\n"
                f"      <p style={{{{ marginTop: '8px', color: 'var(--color-neutral-600)' }}}}>\n"
                f"        {{body || '{body}'}}\n"
                f"      </p>\n"
                f"      {{children}}\n"
                f"    </div>\n"
                f"  );\n"
                f"}}\n"
            )
        return f'<div style="{style}"><h3>{title}</h3><p>{body}</p></div>\n'

    def modal(
        self,
        framework: str = "react",
        title: str = "Confirm",
    ) -> ComponentSpec:
        """Generate a Modal component spec."""
        if framework not in SUPPORTED_FRAMEWORKS:
            raise ValueError(f"Unsupported framework: {framework}.")
        tokens = [
            "color.neutral.50 (surface)",
            "color.neutral.900 (overlay)",
            "spacing.size-6 (24px)",
            "radius.card (16px)",
        ]
        props = {
            "open": {"type": "boolean", "default": False},
            "title": {"type": "string", "default": title},
            "onClose": {"type": "function", "required": True},
        }
        a11y = [
            "Use role='dialog' and aria-modal='true'.",
            "Set aria-labelledby to the title's id.",
            "Trap focus inside the modal while open.",
            "Restore focus to the trigger element on close.",
            "Close on Escape key.",
        ]
        code = (
            "export function Modal({ open, title, onClose, children }) {\n"
            "  if (!open) return null;\n"
            "  return (\n"
            "    <div role='dialog' aria-modal='true' aria-labelledby='modal-title'\n"
            "      style={{ position:'fixed', inset:0, background:'rgba(0,0,0,0.5)', zIndex:1000 }}>\n"
            "      <div style={{ background:'var(--color-neutral-50)', padding:24, borderRadius:'var(--radius-card)',\n"
            "        maxWidth:512, margin:'10vh auto' }}>\n"
            f"        <h2 id='modal-title'>{title or '{title}'}</h2>\n"
            "        {children}\n"
            "        <button onClick={onClose}>Close</button>\n"
            "      </div>\n"
            "    </div>\n"
            "  );\n"
            "}\n"
        )
        return ComponentSpec(
            name="Modal",
            framework=framework,
            variant="default",
            size="md",
            tokens_used=tokens,
            props=props,
            a11y=a11y,
            code=code,
        )

    def generate(
        self,
        component: str,
        framework: str = "react",
        variant: str = "primary",
        size: str = "md",
        **kwargs: Any,
    ) -> ComponentSpec:
        """Top-level dispatcher: component name → spec."""
        c = component.lower().strip()
        if c == "button":
            return self.button(framework, variant, size, kwargs.get("label", "Click me"))
        if c == "input":
            return self.input(framework, kwargs.get("placeholder", "Type here..."), kwargs.get("input_type", "text"))
        if c == "card":
            return self.card(framework, kwargs.get("title", "Card title"), kwargs.get("body", "Card body content."))
        if c == "modal":
            return self.modal(framework, kwargs.get("title", "Confirm"))
        raise ValueError(f"Unknown component: {component}. Supported: button, input, card, modal.")
