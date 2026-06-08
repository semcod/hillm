# uri2hillm

`hillm://` URI adapter — decodes to DSL and dispatches via `dsl2hillm`.

## URI shape

```
hillm://cmd/{VERB}?device=...&register=...&dry_run=true
```

## CLI

```bash
uri2hillm HEALTH
uri2hillm READ DEVICE sensor-temp DRY_RUN true
uri2hillm 'hillm://cmd/HEALTH'
uri2hillm 'hillm://cmd/READ?device=camera-usb&dry_run=true'
uri2hillm decode READ DEVICE sensor-temp
uri2hillm run HEALTH
```

## Python

```python
from uri2hillm.uri import uri_for_cmd, is_hillm_uri
from uri2hillm.run import run_uri

uri = uri_for_cmd("READ", device="sensor-temp", dry_run=True)
result = run_uri(uri)
```

## nlp2uri integration

When `nlp2uri[hillm]` is installed, `compile_uri_to_actions("hillm://...")` returns
`OSAction(host, "uri2hillm", [uri])`.

**See also:** [docs/control-layer.md](../../docs/control-layer.md) · [examples/nlp2uri/](../../examples/nlp2uri/) · [packages/README.md](../README.md) · [CHANGELOG.md](../../CHANGELOG.md)
