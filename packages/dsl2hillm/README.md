# dsl2hillm

CQRS bus and JSON Schema DSL for HILLM hardware control.

## Verbs

| Type | Verbs |
|------|-------|
| Query | `HEALTH`, `DEVICES`, `ORIENT`, `ACTIONS`, `VALIDATE`, `READ`, `STATUS`, `RESOLVE` |
| Command | `WRITE`, `ACTUATE`, `CONNECT`, `DISCONNECT`, `EXECUTE` |

## CLI

```bash
dsl2hillm HEALTH
dsl2hillm 'READ DEVICE sensor-temp DRY_RUN true'
dsl2hillm 'WRITE DEVICE actuator-relay VALUE 1 REGISTER coil:0 DRY_RUN true'
```

## Python

```python
from dsl2hillm import dispatch

result = dispatch("HEALTH")
result = dispatch({"verb": "READ", "device": "camera-usb", "dry_run": True})
```

## Event store

Commands append to `.hillm/events/app.hillm.events.jsonl` in the working directory.

**See also:** [Control layer](../README.md) · [hillm README](../../README.md)
