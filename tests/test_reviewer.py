"""Tests for DesignReviewer.

Docs: tests/test_reviewer.doc.md
"""
from sin_frontend_design.reviewer import DesignReviewer, ReviewReport


class TestEmptyInput:
    def test_empty_string(self) -> None:
        r = DesignReviewer()
        report = r.review("")
        assert report.ok is True
        assert report.score == 100
        assert report.findings == []

    def test_whitespace(self) -> None:
        r = DesignReviewer()
        report = r.review("   \n   ")
        assert report.ok is True


class TestColors:
    def test_known_color_passes(self) -> None:
        r = DesignReviewer()
        report = r.review("color: #6366f1;")
        # 6366f1 is the primary-500, so no warning.
        color_findings = [f for f in report.findings if f.rule == "color.hardcoded"]
        assert color_findings == []

    def test_unknown_color_warns(self) -> None:
        r = DesignReviewer()
        report = r.review("color: #abcdef;")
        assert any(f.rule == "color.hardcoded" for f in report.findings)

    def test_transparent_is_known(self) -> None:
        r = DesignReviewer()
        report = r.review("background: transparent;")
        color_findings = [f for f in report.findings if f.rule == "color.hardcoded"]
        assert color_findings == []


class TestSpacing:
    def test_on_grid_value_passes(self) -> None:
        r = DesignReviewer()
        report = r.review("padding: 16px;")
        spacing_findings = [f for f in report.findings if f.rule == "spacing.off-grid"]
        assert spacing_findings == []

    def test_off_grid_value_warns(self) -> None:
        r = DesignReviewer()
        report = r.review("padding: 13px;")
        assert any(f.rule == "spacing.off-grid" for f in report.findings)


class TestTypography:
    def test_on_scale(self) -> None:
        r = DesignReviewer()
        report = r.review("font-size: 16px;")
        typo_findings = [f for f in report.findings if f.rule == "typography.off-scale"]
        assert typo_findings == []

    def test_off_scale(self) -> None:
        r = DesignReviewer()
        report = r.review("font-size: 17px;")
        assert any(f.rule == "typography.off-scale" for f in report.findings)


class TestA11y:
    def test_img_without_alt_errors(self) -> None:
        r = DesignReviewer()
        report = r.review('<img src="x.png">')
        assert any(f.rule == "a11y.img-alt" and f.severity == "error" for f in report.findings)

    def test_img_with_alt_passes(self) -> None:
        r = DesignReviewer()
        report = r.review('<img src="x.png" alt="A picture">')
        assert not any(f.rule == "a11y.img-alt" for f in report.findings)

    def test_input_without_label_errors(self) -> None:
        r = DesignReviewer()
        report = r.review("<input type='text'>")
        assert any(f.rule == "a11y.input-label" for f in report.findings)

    def test_input_with_label_passes(self) -> None:
        r = DesignReviewer()
        report = r.review("<label>Name</label><input type='text'>")
        assert not any(f.rule == "a11y.input-label" for f in report.findings)

    def test_div_onclick_warns(self) -> None:
        r = DesignReviewer()
        report = r.review("<div onclick='x()'>click</div>")
        assert any(f.rule == "a11y.div-onclick" for f in report.findings)


class TestFocus:
    def test_outline_none_without_replacement_warns(self) -> None:
        r = DesignReviewer()
        report = r.review("button { outline: none; }")
        assert any(f.rule == "a11y.focus-visible" for f in report.findings)

    def test_outline_none_with_focus_replacement_passes(self) -> None:
        r = DesignReviewer()
        report = r.review("button { outline: none; }\nbutton:focus { outline: 2px solid blue; }")
        assert not any(f.rule == "a11y.focus-visible" for f in report.findings)


class TestScoring:
    def test_clean_code_scores_100(self) -> None:
        r = DesignReviewer()
        report = r.review("body { color: #18181b; padding: 16px; }")
        # No findings, no errors.
        assert report.score == 100
        assert report.ok is True

    def test_score_floors_at_zero(self) -> None:
        r = DesignReviewer()
        # Many errors.
        code = "\n".join(["<img src='x'>" for _ in range(50)])
        report = r.review(code)
        assert report.score >= 0
        assert report.score <= 100

    def test_ok_requires_no_errors(self) -> None:
        r = DesignReviewer()
        report = r.review("<img src='x'>")
        assert any(f.severity == "error" for f in report.findings)
        assert report.ok is False
