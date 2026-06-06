# Purpose: CLI shim for design_figma_export
# Docs: design_figma_export.doc.md
"""CLI: design-figma-export — Export tokens to Figma Tokens JSON.

Usage: design-figma-export <source> [--format css|scss|tailwind|json|figma]
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
from ..mcp_server import design_figma_export


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="design-figma-export")
    parser.add_argument("source", help="Source code (file path or '-' for stdin)")
    parser.add_argument(
        "--format",
        choices=["css", "scss", "tailwind", "json", "figma"],
        default="css",
        help="Source format hint (default: css)",
    )
    args = parser.parse_args(argv)
    if args.source == "-":
        code = sys.stdin.read()
        source_format = args.format
    else:
        code = Path(args.source).read_text(encoding="utf-8")
        source_format = args.format
    print(design_figma_export(code, source_format=source_format))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
