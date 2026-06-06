# Purpose: CLI shim for design_responsive_test
# Docs: design_responsive_test.doc.md
"""CLI: design-responsive-test — Generate responsive breakpoints.

Usage: design-responsive-test [--viewport-width N] [--no-css]
"""
from __future__ import annotations
import argparse
import sys
from ..mcp_server import design_responsive_test


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="design-responsive-test")
    parser.add_argument("--viewport-width", type=int, default=1024, help="Current viewport width in px (default: 1024)")
    parser.add_argument("--no-css", dest="include_css", action="store_false", help="Omit CSS payload")
    args = parser.parse_args(argv)
    print(design_responsive_test(viewport_width=args.viewport_width, include_css=args.include_css))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
