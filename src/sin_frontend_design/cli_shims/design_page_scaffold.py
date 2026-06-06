# Purpose: CLI shim for design_page_scaffold
# Docs: design_page_scaffold.doc.md
"""CLI: design-page-scaffold — Scaffold a full page.

Usage: design-page-scaffold [--layout landing|pricing|docs|blog]
                            [--framework html|react|vue|svelte]
                            [--title TITLE]
"""
from __future__ import annotations
import argparse
import sys
from ..mcp_server import design_page_scaffold


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="design-page-scaffold")
    parser.add_argument("--layout", default="landing", choices=["landing", "pricing", "docs", "blog"])
    parser.add_argument("--framework", default="html", choices=["html", "react", "vue", "svelte"])
    parser.add_argument("--title", default="Untitled page")
    args = parser.parse_args(argv)
    print(design_page_scaffold(layout=args.layout, framework=args.framework, title=args.title))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
