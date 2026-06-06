"""Design system data — typography, color, spacing, motion primitives.

Docs: system.doc.md
"""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


TYPOGRAPHY_SCALE: List[int] = [12, 14, 16, 18, 20, 24, 30, 36, 48, 60, 72]
# Anthropic-style: minor third + major third ratio from 16.
# Index 0..10 corresponds to: caption, small, body, lead, h6, h5, h4, h3, h2, h1, display.

SPACING_SCALE: List[int] = [4, 8, 12, 16, 24, 32, 48, 64, 96]
# 4px grid. Indices map to: 1, 2, 3, 4, 6, 8, 12, 16, 24 (multiples of 4).

RADIUS_DEFAULT = 8
RADIUS_CARD = 16

# Motion tokens — single source of truth.
DURATION_HOVER_MS = 200
DURATION_TRANSITION_MS = 300
DURATION_PAGE_MS = 500
EASE_HOVER = "ease-out"
EASE_TRANSITION = "ease-in-out"
EASE_PAGE = "cubic-bezier(0.16, 1, 0.3, 1)"


@dataclass(frozen=True)
class ColorRamp:
    """A 50–900 scale of a single hue, like Tailwind but semantic."""

    name: str
    hex_50: str
    hex_100: str
    hex_200: str
    hex_300: str
    hex_400: str
    hex_500: str
    hex_600: str
    hex_700: str
    hex_800: str
    hex_900: str

    def as_dict(self) -> Dict[str, str]:
        return {
            "50": self.hex_50,
            "100": self.hex_100,
            "200": self.hex_200,
            "300": self.hex_300,
            "400": self.hex_400,
            "500": self.hex_500,
            "600": self.hex_600,
            "700": self.hex_700,
            "800": self.hex_800,
            "900": self.hex_900,
        }


NEUTRAL = ColorRamp(
    name="neutral",
    hex_50="#fafafa",
    hex_100="#f4f4f5",
    hex_200="#e4e4e7",
    hex_300="#d4d4d8",
    hex_400="#a1a1aa",
    hex_500="#71717a",
    hex_600="#52525b",
    hex_700="#3f3f46",
    hex_800="#27272a",
    hex_900="#18181b",
)

PRIMARY = ColorRamp(
    name="primary",
    hex_50="#eef2ff",
    hex_100="#e0e7ff",
    hex_200="#c7d2fe",
    hex_300="#a5b4fc",
    hex_400="#818cf8",
    hex_500="#6366f1",
    hex_600="#4f46e5",
    hex_700="#4338ca",
    hex_800="#3730a3",
    hex_900="#312e81",
)

SECONDARY = ColorRamp(
    name="secondary",
    hex_50="#f5f3ff",
    hex_100="#ede9fe",
    hex_200="#ddd6fe",
    hex_300="#c4b5fd",
    hex_400="#a78bfa",
    hex_500="#8b5cf6",
    hex_600="#7c3aed",
    hex_700="#6d28d9",
    hex_800="#5b21b6",
    hex_900="#4c1d95",
)

SUCCESS = ColorRamp(
    name="success",
    hex_50="#f0fdf4",
    hex_100="#dcfce7",
    hex_200="#bbf7d0",
    hex_300="#86efac",
    hex_400="#4ade80",
    hex_500="#22c55e",
    hex_600="#16a34a",
    hex_700="#15803d",
    hex_800="#166534",
    hex_900="#14532d",
)

WARNING = ColorRamp(
    name="warning",
    hex_50="#fffbeb",
    hex_100="#fef3c7",
    hex_200="#fde68a",
    hex_300="#fcd34d",
    hex_400="#fbbf24",
    hex_500="#f59e0b",
    hex_600="#d97706",
    hex_700="#b45309",
    hex_800="#92400e",
    hex_900="#78350f",
)

ERROR = ColorRamp(
    name="error",
    hex_50="#fef2f2",
    hex_100="#fee2e2",
    hex_200="#fecaca",
    hex_300="#fca5a5",
    hex_400="#f87171",
    hex_500="#ef4444",
    hex_600="#dc2626",
    hex_700="#b91c1c",
    hex_800="#991b1b",
    hex_900="#7f1d1d",
)


@dataclass(frozen=True)
class DesignTokens:
    """The 4 token families — typography, color, spacing, motion."""

    typography: Dict[str, int]
    color: Dict[str, ColorRamp]
    spacing: List[int]
    motion: Dict[str, Any]
    radius: Dict[str, int]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "typography": self.typography,
            "color": {k: v.as_dict() for k, v in self.color.items()},
            "spacing": self.spacing,
            "motion": self.motion,
            "radius": self.radius,
        }


@dataclass
class Theme:
    """A semantic mapping (primary, secondary, danger, ...) → ramp name."""

    name: str
    semantic: Dict[str, str]
    is_dark: bool = False

    def get_ramp(self, semantic_role: str) -> Optional[ColorRamp]:
        ramp_name = self.semantic.get(semantic_role)
        if not ramp_name:
            return None
        return DEFAULT_TOKENS.color.get(ramp_name)


LIGHT_THEME = Theme(
    name="light",
    semantic={
        "background": "neutral",
        "surface": "neutral",
        "text": "neutral",
        "muted": "neutral",
        "primary": "primary",
        "secondary": "secondary",
        "success": "success",
        "warning": "warning",
        "error": "error",
        "border": "neutral",
    },
    is_dark=False,
)

DARK_THEME = Theme(
    name="dark",
    semantic={
        "background": "neutral",
        "surface": "neutral",
        "text": "neutral",
        "muted": "neutral",
        "primary": "primary",
        "secondary": "secondary",
        "success": "success",
        "warning": "warning",
        "error": "error",
        "border": "neutral",
    },
    is_dark=True,
)


DEFAULT_TOKENS = DesignTokens(
    typography={f"size-{i}": px for i, px in enumerate(TYPOGRAPHY_SCALE)},
    color={
        "neutral": NEUTRAL,
        "primary": PRIMARY,
        "secondary": SECONDARY,
        "success": SUCCESS,
        "warning": WARNING,
        "error": ERROR,
    },
    spacing=SPACING_SCALE,
    motion={
        "duration": {
            "hover": DURATION_HOVER_MS,
            "transition": DURATION_TRANSITION_MS,
            "page": DURATION_PAGE_MS,
        },
        "easing": {
            "hover": EASE_HOVER,
            "transition": EASE_TRANSITION,
            "page": EASE_PAGE,
        },
    },
    radius={
        "default": RADIUS_DEFAULT,
        "card": RADIUS_CARD,
    },
)


class DesignSystem:
    """SOTA design system loader — provides tokens, themes, and philosophy.

    The system exposes:
    - Default tokens (typography, color, spacing, motion, radius)
    - Built-in themes (light, dark)
    - A philosophy summary that agents should internalize
    - A custom-theme registry
    """

    PHILOSOPHY: List[str] = [
        "Hierarchy is created by contrast, not by decoration.",
        "Type is the primary voice — choose one family and use scale.",
        "Color is functional: primary, secondary, success, warning, error, neutral.",
        "Spacing follows a 4px grid — never arbitrary values.",
        "Motion is felt, not seen: 200ms hovers, 300ms transitions.",
        "Components are predictable: same name, same shape, same tokens.",
        "States are explicit: default, hover, focus, active, disabled.",
        "Accessibility is non-negotiable: WCAG 2.2 AA is the floor.",
        "Dark mode is not inverted — it's a parallel semantic map.",
        "Famous brands feel calm because they use restraint.",
    ]

    def __init__(self) -> None:
        self._tokens = DEFAULT_TOKENS
        self._themes: Dict[str, Theme] = {"light": LIGHT_THEME, "dark": DARK_THEME}

    @property
    def tokens(self) -> DesignTokens:
        return self._tokens

    def get_theme(self, name: str = "light") -> Optional[Theme]:
        return self._themes.get(name)

    def register_theme(self, theme: Theme) -> None:
        """Add a custom theme (e.g. brand-specific)."""
        self._themes[theme.name] = theme

    def list_themes(self) -> List[str]:
        return list(self._themes.keys())

    def philosophy(self) -> List[str]:
        return list(self.PHILOSOPHY)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tokens": self._tokens.to_dict(),
            "themes": [
                {
                    "name": t.name,
                    "is_dark": t.is_dark,
                    "semantic": t.semantic,
                }
                for t in self._themes.values()
            ],
            "philosophy": self.philosophy(),
        }

    def load(self, name: str = "default") -> Dict[str, Any]:
        """Load a named design system (default = built-in)."""
        if name == "default":
            return self.to_dict()
        # Future: support loading from JSON files.
        return self.to_dict()
