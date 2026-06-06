# Purpose: CLI shim for design_review
# Docs: design_review.doc.md
"""CLI: design-review — Review existing UI code for design system consistency.

Usage: design-review <code-file>
       cat component.html | design-review -
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
from ..mcp_server import design_review


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="design-review")
    parser.add_argument("source", help="Source file path, or '-' for stdin")
    args = parser.parse_args(argv)
    if args.source == "-":
        code = sys.stdin.read()
    else:
        code = Path(args.source).read_text(encoding="utf-8")
    print(design_review(code))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
