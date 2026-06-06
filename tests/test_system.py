"""Tests for DesignSystem.

Docs: test_system.doc.md
"""
from sin_frontend_design.system import (
    DEFAULT_TOKENS,
    DARK_THEME,
    DURATION_HOVER_MS,
    DURATION_PAGE_MS,
    DURATION_TRANSITION_MS,
    EASE_HOVER,
    EASE_PAGE,
    EASE_TRANSITION,
    LIGHT_THEME,
    NEUTRAL,
    PRIMARY,
    RADIUS_CARD,
    RADIUS_DEFAULT,
    SECONDARY,
    SPACING_SCALE,
    SUCCESS,
    TYPOGRAPHY_SCALE,
    WARNING,
    ColorRamp,
    DesignSystem,
    DesignTokens,
    ERROR,
    Theme,
)


class TestTypographyScale:
    def test_typography_scale_values(self) -> None:
        assert TYPOGRAPHY_SCALE == [12, 14, 16, 18, 20, 24, 30, 36, 48, 60, 72]

    def test_typography_scale_in_body_size(self) -> None:
        assert 16 in TYPOGRAPHY_SCALE

    def test_typography_scale_in_display(self) -> None:
        assert 72 in TYPOGRAPHY_SCALE


class TestSpacingScale:
    def test_spacing_scale_values(self) -> None:
        assert SPACING_SCALE == [4, 8, 12, 16, 24, 32, 48, 64, 96]

    def test_spacing_scale_grid_4px(self) -> None:
        for v in SPACING_SCALE:
            assert v % 4 == 0


class TestRadii:
    def test_radius_default(self) -> None:
        assert RADIUS_DEFAULT == 8

    def test_radius_card(self) -> None:
        assert RADIUS_CARD == 16


class TestMotion:
    def test_hover_duration(self) -> None:
        assert DURATION_HOVER_MS == 200

    def test_transition_duration(self) -> None:
        assert DURATION_TRANSITION_MS == 300

    def test_page_duration(self) -> None:
        assert DURATION_PAGE_MS == 500

    def test_easings(self) -> None:
        assert EASE_HOVER == "ease-out"
        assert EASE_TRANSITION == "ease-in-out"
        assert EASE_PAGE.startswith("cubic-bezier")


class TestColorRamps:
    def test_neutral_ramp_count(self) -> None:
        assert len(NEUTRAL.as_dict()) == 10

    def test_primary_ramp_has_500(self) -> None:
        assert NEUTRAL.hex_500.startswith("#")
        assert PRIMARY.hex_500 == "#6366f1"

    def test_secondary_ramp(self) -> None:
        assert SECONDARY.hex_500 == "#8b5cf6"

    def test_success_ramp(self) -> None:
        assert SUCCESS.hex_500 == "#22c55e"

    def test_warning_ramp(self) -> None:
        assert WARNING.hex_500 == "#f59e0b"

    def test_error_ramp(self) -> None:
        assert ERROR.hex_500 == "#ef4444"

    def test_ramp_dict_keys(self) -> None:
        keys = set(PRIMARY.as_dict().keys())
        assert keys == {"50", "100", "200", "300", "400", "500", "600", "700", "800", "900"}


class TestDesignTokens:
    def test_default_tokens_typography(self) -> None:
        assert DEFAULT_TOKENS.typography["size-0"] == 12
        assert DEFAULT_TOKENS.typography["size-10"] == 72

    def test_default_tokens_spacing(self) -> None:
        assert 16 in DEFAULT_TOKENS.spacing

    def test_default_tokens_motion(self) -> None:
        assert DEFAULT_TOKENS.motion["duration"]["hover"] == 200

    def test_default_tokens_radius(self) -> None:
        assert DEFAULT_TOKENS.radius["default"] == 8

    def test_to_dict_round_trip(self) -> None:
        d = DEFAULT_TOKENS.to_dict()
        assert "typography" in d
        assert "color" in d
        assert "spacing" in d
        assert "motion" in d


class TestThemes:
    def test_light_theme_exists(self) -> None:
        assert LIGHT_THEME.is_dark is False
        assert LIGHT_THEME.semantic["primary"] == "primary"

    def test_dark_theme_flag(self) -> None:
        assert DARK_THEME.is_dark is True

    def test_theme_get_ramp(self) -> None:
        ramp = LIGHT_THEME.get_ramp("primary")
        assert ramp is not None
        assert ramp.name == "primary"

    def test_theme_get_unknown(self) -> None:
        assert LIGHT_THEME.get_ramp("nonexistent") is None


class TestDesignSystem:
    def test_load_default(self) -> None:
        ds = DesignSystem()
        data = ds.load("default")
        assert "tokens" in data
        assert "themes" in data
        assert "philosophy" in data

    def test_list_themes(self) -> None:
        ds = DesignSystem()
        assert "light" in ds.list_themes()
        assert "dark" in ds.list_themes()

    def test_register_theme(self) -> None:
        ds = DesignSystem()
        custom = Theme(name="brand", semantic={"primary": "primary"}, is_dark=False)
        ds.register_theme(custom)
        assert "brand" in ds.list_themes()
        assert ds.get_theme("brand") is not None

    def test_get_theme_default(self) -> None:
        ds = DesignSystem()
        assert ds.get_theme("light") is LIGHT_THEME
        assert ds.get_theme("missing") is None

    def test_philosophy_count(self) -> None:
        ds = DesignSystem()
        assert len(ds.philosophy()) >= 5

    def test_to_dict(self) -> None:
        ds = DesignSystem()
        d = ds.to_dict()
        assert "philosophy" in d
        assert "tokens" in d

    def test_tokens_property(self) -> None:
        ds = DesignSystem()
        assert isinstance(ds.tokens, DesignTokens)
