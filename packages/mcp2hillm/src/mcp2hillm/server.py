from __future__ import annotations

import json

from dsl2hillm import dispatch
from mcp.server.fastmcp import FastMCP
from nlp2hillm.to_dsl import to_dsl

mcp = FastMCP("hillm")


@mcp.tool()
def hillm_run_dsl(line: str) -> str:
    """Execute a dsl2hillm command line."""
    return json.dumps(dispatch(line).to_dict(), indent=2)


@mcp.tool()
def hillm_to_dsl(prompt: str) -> str:
    """Map natural language to dsl2hillm without executing."""
    return to_dsl(prompt)


@mcp.tool()
def hillm_run_command(command: str) -> str:
    """Alias for hillm_run_dsl."""
    return hillm_run_dsl(command)
