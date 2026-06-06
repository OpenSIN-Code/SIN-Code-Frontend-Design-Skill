"""Tests for CoDocs presence.

Docs: test_codocs.doc.md
"""
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = REPO_ROOT / "src" / "sin_frontend_design"


class TestCompanionDocs:
    def test_every_py_has_doc_md(self) -> None:
        """Every .py file in src/sin_frontend_design/ must have a .doc.md companion."""
        py_files = list(SRC_DIR.glob("*.py"))
        assert len(py_files) > 0
        for py in py_files:
            stem = py.name[: -len(".py")]
            doc = SRC_DIR / f"{stem}.doc.md"
            assert doc.exists(), f"Missing companion doc for {py.name} (expected {doc.name})"

    def test_every_doc_md_has_companion_py(self) -> None:
        """Every .doc.md file must have a matching .py companion."""
        doc_files = list(SRC_DIR.glob("*.doc.md"))
        assert len(doc_files) > 0
        for doc in doc_files:
            # e.g. mcp_server.doc.md -> mcp_server.py (not .doc.py)
            stem = doc.name[: -len(".doc.md")]
            py = SRC_DIR / f"{stem}.py"
            assert py.exists(), f"Doc without companion: {doc.name} (expected {py.name})"

    def test_doc_md_referenced_in_py(self) -> None:
        """Every .py should reference its .doc.md in a header comment or docstring."""
        for py in SRC_DIR.glob("*.py"):
            content = py.read_text()
            if py.name == "__init__.py":
                continue
            stem = py.name[: -len(".py")]
            doc_name = f"{stem}.doc.md"
            assert doc_name in content, f"{py.name} does not reference its .doc.md ({doc_name})"


class TestScriptDocs:
    def test_every_sh_has_doc_md(self) -> None:
        sh_dir = REPO_ROOT / "scripts"
        sh_files = list(sh_dir.glob("*.sh"))
        assert len(sh_files) >= 6
        for sh in sh_files:
            stem = sh.name[: -len(".sh")]
            doc = sh_dir / f"{stem}.doc.md"
            assert doc.exists(), f"Missing doc for {sh.name} (expected {doc.name})"


class TestTestDocs:
    def test_every_test_has_doc_md(self) -> None:
        tests_dir = REPO_ROOT / "tests"
        for test_py in tests_dir.glob("test_*.py"):
            stem = test_py.name[: -len(".py")]
            doc = tests_dir / f"{stem}.doc.md"
            assert doc.exists(), f"Missing test doc: {test_py.name} (expected {doc.name})"
