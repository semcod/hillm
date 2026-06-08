# cli2hillm

Shell passthrough — run `hillm` subcommands or raw DSL through the bus.

## CLI

```bash
cli2hillm HEALTH
cli2hillm 'READ DEVICE sensor-temp' --dry-run
cli2hillm 'READ DEVICE sensor-temp' --live
cli2hillm "devices --format json" --shell
```

Without `--shell`, input goes to `dsl2hillm.dispatch()`. Loads `.env` automatically.

**See also:** [Control layer](../README.md) · [docs/control-layer.md](../../docs/control-layer.md)
