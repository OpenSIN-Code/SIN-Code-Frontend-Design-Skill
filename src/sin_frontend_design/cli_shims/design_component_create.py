# Purpose: CLI shim for design_component_create
# Docs: design_component_create.doc.md
"""CLI: design-component-create — Generate component spec.

Usage: design-component-create <component> [--framework react|vue|svelte|html]
                                   [--variant ...] [--size ...] [--label ...]
                                   [--placeholder ...] [--title ...]
"""
from __future__ import annotations
import argparse
import sys
from ..mcp_server import design_component_create


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="design-component-create")
    parser.add_argument("component", choices=["button", "input", "card", "modal"])
    parser.add_argument("--framework", default="react", choices=["react", "vue", "svelte", "html"])
    parser.add_argument("--variant", default="primary", choices=["primary", "secondary", "ghost", "outline", "danger"])
    parser.add_argument("--size", default="md", choices=["xs", "sm", "md", "lg", "xl"])
    parser.add_argument("--label", default="")
    parser.add_argument("--placeholder", default="")
    parser.add_argument("--title", default="")
    args = parser.parse_args(argv)
    print(design_component_create(
        component=args.component,
        framework=args.framework,
        variant=args.variant,
        size=args.size,
        label=args.label,
        placeholder=args.placeholder,
        title=args.title,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
