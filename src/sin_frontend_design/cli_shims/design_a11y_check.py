# Purpose: CLI shim for design_a11y_check
# Docs: design_a11y_check.doc.md
"""CLI: design-a11y-check — Check WCAG 2.2 AA compliance of HTML code.

Usage: design-a11y-check <code-file> [--foreground HEX] [--background HEX]
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
from ..mcp_server import design_a11y_check


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="design-a11y-check")
    parser.add_argument("source", help="HTML source file path, or '-' for stdin")
    parser.add_argument("--foreground", default="", help="Optional foreground hex color (e.g. #000000)")
    parser.add_argument("--background", default="", help="Optional background hex color (e.g. #ffffff)")
    args = parser.parse_args(argv)
    if args.source == "-":
        code = sys.stdin.read()
    else:
        code = Path(args.source).read_text(encoding="utf-8")
    print(design_a11y_check(code, foreground=args.foreground, background=args.background))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
