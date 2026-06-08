# Control layer (`*2hillm`)

Thin adapters around `dsl2hillm.dispatch()` — same pattern as [`tillm/packages/*2tillm`](../../tillm/packages/) and [`gillm/packages/*2gillm`](../../gillm/packages/).

Domain logic (registry, controller, transports) stays in `src/hillm/`.

## Packages

| Package | Role | Port |
| --- | --- | --- |
| **dsl2hillm** | DSL + JSON Schema + CQRS bus | — |
| **uri2hillm** | `hillm://` or DSL shorthand → `dispatch()` | — |
| **nlp2hillm** | NL → DSL (rules or OpenRouter LLM); `--apply` dry-run default | — |
| **cli2hillm** | Shell / hillm CLI passthrough | — |
| **mcp2hillm** | MCP stdio tools | — |
| **rest2hillm** | FastAPI `/v1/dsl` | **8218** |

Package READMEs: [packages/README.md](../packages/README.md)

## Core helpers (shared)

| Module | Role |
| --- | --- |
| `hillm.project_env` | Auto-load `.env`; `apply_execution_policy()` for dry-run/live |
| `hillm.resolve` | NL keywords → registry device id |
| `hillm.registry` | Device catalog, aliases, `suggest_device_ids()` |

## Install (dev)

```bash
make install-dev
# or
bash packages/install-dev.sh
cp examples/env.example .env
```

## DSL verbs

| Type | Verbs |
| --- | --- |
| Query | `HEALTH`, `DEVICES`, `ORIENT`, `ACTIONS`, `VALIDATE`, `READ`, `STATUS`, `RESOLVE` |
| Command | `WRITE`, `ACTUATE`, `CONNECT`, `DISCONNECT`, `EXECUTE` |

Example:

```text
HEALTH
READ DEVICE sensor-temp DRY_RUN true
WRITE DEVICE actuator-relay VALUE 1 REGISTER coil:0 DRY_RUN true
ACTUATE DEVICE display-primary ACTION on
```

## Dry-run policy

| Adapter | Default | Real hardware |
| --- | --- | --- |
| `nlp2hillm --apply` | dry-run | `--live` |
| `uri2hillm` / `uri2hillm run` | dry-run | `--live` |
| `dsl2hillm` | dry-run for hardware verbs | `--live` |
| `cli2hillm` | dry-run for hardware verbs | `--live` |
| `hillm` CLI | `--dry-run` flag | without flag |

All CLIs load `<project>/.env` automatically via `hillm.project_env.bootstrap_project_env()`.

## Adapters

```bash
# DSL
dsl2hillm HEALTH
dsl2hillm 'READ DEVICE sensor-temp' --dry-run
dsl2hillm 'READ DEVICE sensor-temp' --live

# URI — dry-run by default
uri2hillm HEALTH
uri2hillm READ DEVICE sensor-temp
uri2hillm READ DEVICE sensor-temp --live
uri2hillm 'hillm://cmd/READ?device=camera-usb&dry_run=true'
uri2hillm decode READ DEVICE sensor-temp
uri2hillm run HEALTH

# NLP — OpenRouter z .env lub reguły (--no-llm)
nlp2hillm "read temperature from serial"
nlp2hillm "read temperature from serial" --no-llm
nlp2hillm "read temperature from serial" --apply
nlp2hillm "read temperature from serial" --apply --live

# Shell passthrough
cli2hillm HEALTH
cli2hillm 'READ DEVICE sensor-temp' --dry-run
cli2hillm "devices --format json" --shell

# REST (pair with rest2gillm :8220, rest2tillm :8216)
rest2hillm serve --port 8218
curl -X POST http://127.0.0.1:8218/v1/dsl -d HEALTH
curl -X POST http://127.0.0.1:8218/v1/dsl -d 'READ DEVICE sensor-temp DRY_RUN true'

# MCP
mcp2hillm serve
```

## URI shape

```
hillm://cmd/{VERB}?device=...&register=...&dry_run=true
```

`uri2hillm` accepts:

1. Full `hillm://` URI (for nlp2uri and automation)
2. DSL shorthand (`HEALTH`, `READ DEVICE sensor-temp`)

Bare `READ` without `DEVICE` returns a schema validation error with device required.

Details: [packages/uri2hillm/README.md](../packages/uri2hillm/README.md)

## nlp2uri integration

When `nlp2uri[hillm]` is installed, `compile_uri_to_actions("hillm://...")` returns
`OSAction(host, "uri2hillm", [uri])`.

Examples: [examples/nlp2uri/](../examples/nlp2uri/) · [examples/nlp2hillm/](../examples/nlp2hillm/)

## Architecture

```mermaid
flowchart TB
  subgraph adapters [Input adapters]
    NL[nlp2hillm]
    URI[uri2hillm]
    CLI[cli2hillm]
    MCP[mcp2hillm]
    REST[rest2hillm]
  end

  subgraph control [Control layer]
    DSL[dsl2hillm.dispatch]
    POL[apply_execution_policy]
    SCH[JSON Schema]
    ES[(EventStore)]
  end

  subgraph domain [Domain — src/hillm]
    RES[resolve]
    REG[registry]
    CTL[controller]
    TR[transports]
  end

  NL --> RES
  RES --> DSL
  NL --> POL
  URI --> POL
  CLI --> POL
  POL --> DSL
  URI --> DSL
  CLI --> DSL
  MCP --> DSL
  REST --> DSL
  DSL --> SCH
  DSL --> REG
  DSL --> CTL
  CTL --> TR
  DSL --> ES
```

**See also:** [configuration.md](configuration.md) · [examples/control-layer/](../examples/control-layer/) · [TODO.md](../TODO.md)
