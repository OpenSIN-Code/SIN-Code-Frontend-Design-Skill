# Purpose: CLI shim for design_system_load
# Docs: design_system_load.doc.md
"""CLI: design-system-load — Load the SOTA design system tokens.

Usage: design-system-load [--name NAME]
"""
from __future__ import annotations
import argparse
import sys
from ..mcp_server import design_system_load


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="design-system-load")
    parser.add_argument("--name", default="default", help="Design system name (default: 'default')")
    args = parser.parse_args(argv)
    print(design_system_load(name=args.name))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
