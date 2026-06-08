# mcp2hillm

MCP server exposing HILLM tools to IDE agents.

## Tools

| Tool | Description |
|------|-------------|
| `hillm_run_dsl` | Execute a dsl2hillm line |
| `hillm_to_dsl` | NL → DSL via nlp2hillm |
| `hillm_run_command` | Alias for `hillm_run_dsl` |

## Run

```bash
mcp2hillm stdio
```

Configure in your MCP client JSON (Cursor, Windsurf, …) pointing at `mcp2hillm`.

**See also:** [Control layer](../README.md)
