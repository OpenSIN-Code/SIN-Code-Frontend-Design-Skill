"""Tests for A11yChecker (WCAG 2.2 AA).

Docs: test_a11y.doc.md
"""
import pytest

from sin_frontend_design.a11y import A11yChecker


class TestEmpty:
    def test_empty_string(self) -> None:
        c = A11yChecker()
        report = c.check("")
        assert report.ok is True
        assert report.score == 100


class TestImages:
    def test_img_without_alt_errors(self) -> None:
        c = A11yChecker()
        report = c.check("<img src='x.png'>")
        assert any(f.rule == "img-alt" for f in report.findings)

    def test_img_with_alt_passes(self) -> None:
        c = A11yChecker()
        report = c.check("<html lang='en'><head><title>T</title></head><body><img src='x' alt='X'></body></html>")
        assert not any(f.rule == "img-alt" for f in report.findings)


class TestLang:
    def test_html_without_lang_errors(self) -> None:
        c = A11yChecker()
        report = c.check("<html><head><title>T</title></head><body></body></html>")
        assert any(f.rule == "html-lang" for f in report.findings)

    def test_html_with_lang_passes(self) -> None:
        c = A11yChecker()
        report = c.check("<html lang='en'><head><title>T</title></head><body></body></html>")
        assert not any(f.rule == "html-lang" for f in report.findings)


class TestTitle:
    def test_no_title_errors(self) -> None:
        c = A11yChecker()
        report = c.check("<html lang='en'><head></head><body></body></html>")
        assert any(f.rule == "page-title" for f in report.findings)

    def test_with_title_passes(self) -> None:
        c = A11yChecker()
        report = c.check("<html lang='en'><head><title>Hello</title></head><body></body></html>")
        assert not any(f.rule == "page-title" for f in report.findings)


class TestHeadings:
    def test_heading_skip_warns(self) -> None:
        c = A11yChecker()
        report = c.check(
            "<html lang='en'><head><title>T</title></head><body><h1>A</h1><h3>Skip</h3></body></html>"
        )
        assert any(f.rule == "heading-skip" for f in report.findings)

    def test_no_skip_sequential(self) -> None:
        c = A11yChecker()
        report = c.check(
            "<html lang='en'><head><title>T</title></head><body><h1>A</h1><h2>B</h2><h3>C</h3></body></html>"
        )
        assert not any(f.rule == "heading-skip" for f in report.findings)

    def test_first_heading_h1_passes(self) -> None:
        c = A11yChecker()
        report = c.check(
            "<html lang='en'><head><title>T</title></head><body><h1>A</h1></body></html>"
        )
        assert not any(f.rule == "heading-first-not-h1" for f in report.findings)

    def test_first_heading_h2_warns(self) -> None:
        c = A11yChecker()
        report = c.check(
            "<html lang='en'><head><title>T</title></head><body><h2>A</h2></body></html>"
        )
        assert any(f.rule == "heading-first-not-h1" for f in report.findings)


class TestLinks:
    def test_empty_link_errors(self) -> None:
        c = A11yChecker()
        report = c.check("<html lang='en'><head><title>T</title></head><body><a href='#'></a></body></html>")
        assert any(f.rule == "link-empty" for f in report.findings)

    def test_descriptive_link_passes(self) -> None:
        c = A11yChecker()
        report = c.check(
            "<html lang='en'><head><title>T</title></head><body><a href='#'>Read the docs</a></body></html>"
        )
        assert not any(f.rule == "link-empty" for f in report.findings)

    def test_generic_link_warns(self) -> None:
        c = A11yChecker()
        report = c.check(
            "<html lang='en'><head><title>T</title></head><body><a href='#'>click here</a></body></html>"
        )
        assert any(f.rule == "link-generic" for f in report.findings)


class TestInputs:
    def test_input_without_label_errors(self) -> None:
        c = A11yChecker()
        report = c.check(
            "<html lang='en'><head><title>T</title></head><body><input type='text'></body></html>"
        )
        assert any(f.rule == "input-label" for f in report.findings)

    def test_input_with_label_passes(self) -> None:
        c = A11yChecker()
        report = c.check(
            "<html lang='en'><head><title>T</title></head><body><label>Name</label><input type='text'></body></html>"
        )
        assert not any(f.rule == "input-label" for f in report.findings)

    def test_input_with_aria_label_passes(self) -> None:
        c = A11yChecker()
        report = c.check(
            "<html lang='en'><head><title>T</title></head><body><input type='text' aria-label='Name'></body></html>"
        )
        assert not any(f.rule == "input-label" for f in report.findings)


class TestDivOnclick:
    def test_div_onclick_errors(self) -> None:
        c = A11yChecker()
        report = c.check(
            "<html lang='en'><head><title>T</title></head><body><div onclick='x()'>Click</div></body></html>"
        )
        assert any(f.rule == "div-onclick" for f in report.findings)


class TestContrast:
    def test_black_on_white(self) -> None:
        c = A11yChecker()
        result = c.check_contrast("#000000", "#ffffff")
        assert result["ok"] is True
        assert result["ratio"] == 21.0
        assert result["pass_aa_normal"] is True
        assert result["pass_aaa_normal"] is True

    def test_low_contrast(self) -> None:
        c = A11yChecker()
        result = c.check_contrast("#777777", "#888888")
        assert result["pass_aa_normal"] is False

    def test_invalid_hex(self) -> None:
        c = A11yChecker()
        result = c.check_contrast("not-a-color", "#fff")
        assert result["ok"] is False
        assert "error" in result


class TestScoring:
    def test_clean_doc_scores_100(self) -> None:
        c = A11yChecker()
        code = (
            "<html lang='en'><head><title>Hi</title></head>"
            "<body><h1>A</h1><a href='#'>Read the docs</a>"
            "<label>Name</label><input type='text' aria-label='Name'>"
            "<img src='x' alt='X'></body></html>"
        )
        report = c.check(code)
        assert report.score >= 90
        assert report.ok is True
