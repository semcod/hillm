# hillm documentation

| Document | Description |
| --- | --- |
| [../examples/README.md](../examples/README.md) | Runnable CLI, DSL, NLP, and control-layer smoke scripts |
| [configuration.md](configuration.md) | Install, `.env`, dry-run, env vars, ports |
| [control-layer.md](control-layer.md) | `*2hillm` adapters, dry-run policy, DSL verbs |

## Quick reference

| Task | Command |
| --- | --- |
| List devices | `hillm devices` |
| Safe read (dry-run) | `uri2hillm 'READ DEVICE sensor-temp'` |
| NL → execute | `nlp2hillm "read temperature from serial" --apply` |
| DSL health check | `dsl2hillm HEALTH` |
| Real hardware | add `--live` (nlp2hillm, uri2hillm) or omit `--dry-run` |

All CLIs auto-load `<project>/.env`. Copy [examples/env.example](../examples/env.example) for `HILLM_DRY_RUN=1`.

**See also:** [README.md](../README.md) · [packages/README.md](../packages/README.md) · [CHANGELOG.md](../CHANGELOG.md) · [TODO.md](../TODO.md)
