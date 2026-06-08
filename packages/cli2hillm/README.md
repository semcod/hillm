# cli2hillm

Shell passthrough — run `hillm` subcommands or raw DSL through the bus.

## CLI

```bash
cli2hillm HEALTH
cli2hillm 'READ DEVICE sensor-temp DRY_RUN true'
cli2hillm "devices --format json" --shell
```

Without `--shell`, input is sent to `dsl2hillm.dispatch()`.

**See also:** [Control layer](../README.md)
