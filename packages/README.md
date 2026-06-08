# HILLM control layer packages

Hardware Interface LLM adapters — same `*2hillm` pattern as `tillm` / `gillm`.

| Package | CLI | Docs | Role |
|---------|-----|------|------|
| `dsl2hillm` | `dsl2hillm` | [README](dsl2hillm/README.md) | CQRS bus + JSON Schema DSL |
| `uri2hillm` | `uri2hillm` | [README](uri2hillm/README.md) | `hillm://cmd/VERB?...` → DSL |
| `nlp2hillm` | `nlp2hillm` | [README](nlp2hillm/README.md) | Natural language → DSL |
| `cli2hillm` | `cli2hillm` | [README](cli2hillm/README.md) | Shell / hillm CLI passthrough |
| `mcp2hillm` | `mcp2hillm` | [README](mcp2hillm/README.md) | MCP tools (`hillm_run_dsl`, …) |
| `rest2hillm` | `rest2hillm` | [README](rest2hillm/README.md) | FastAPI on port **8218** |

```bash
bash packages/install-dev.sh
hillm devices
dsl2hillm HEALTH
uri2hillm HEALTH
uri2hillm READ DEVICE sensor-temp DRY_RUN true
rest2hillm --port 8218
```

**See also:** [../docs/control-layer.md](../docs/control-layer.md) · [../examples/README.md](../examples/README.md) · [../CHANGELOG.md](../CHANGELOG.md) · [../TODO.md](../TODO.md)
