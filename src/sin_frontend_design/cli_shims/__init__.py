# Purpose: CLI shim for sin-frontend-design MCP tools
# Docs: __init__.doc.md
"""CLI shim package — exposes MCP tools as standalone CLI binaries.

Each shim is a thin wrapper that:
1. Parses argparse arguments
2. Calls the underlying MCP tool function from sin_frontend_design.mcp_server
3. Prints the result to stdout

This lets sub-agents and shell users invoke the tools without spinning
up the MCP server.
"""
