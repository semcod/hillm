# HILLM configuration

## Install profiles

```bash
uv sync --all-packages --extra dev   # recommended (workspace + dev)
pip install -e .                              # core only
pip install -e ".[serial,modbus,mqtt]"        # field transports
pip install -e ".[dev]"                       # pytest, goal, ruff, …
bash packages/install-dev.sh                  # editable control layer (*2hillm)
```

## Project `.env`

All CLIs (`hillm`, `dsl2hillm`, `nlp2hillm`, `uri2hillm`, `cli2hillm`) and `dispatch()` auto-load `.env` from the current directory or parents.

```bash
cp examples/env.example .env
# minimum for safe local dev:
# HILLM_DRY_RUN=1
```

If your `.env` already has other keys (e.g. `OPENROUTER_API_KEY`), append `HILLM_DRY_RUN=1` on a new line.

## Dry-run policy

| Adapter | Default | Real hardware |
| --- | --- | --- |
| `nlp2hillm --apply` | dry-run | `--live` |
| `uri2hillm` / `uri2hillm run` | dry-run | `--live` |
| `dsl2hillm` | dry-run for `READ`/`WRITE`/… | `--live` |
| `cli2hillm` | dry-run for `READ`/`WRITE`/… | `--live` |
| `hillm` CLI | `--dry-run` flag | without flag |

Implementation: `hillm.project_env.apply_execution_policy()`.

Without dry-run, serial devices need the port present (e.g. `/dev/ttyUSB0`). Errors include a hint to use `DRY_RUN true` or `HILLM_DRY_RUN=1`.

## Environment variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `HILLM_DRY_RUN` | off | Force `dry_run` transport for every device |
| `HILLM_MODBUS_HOST` | — | Required for `modbus-tcp` profile readiness |
| `HILLM_MODBUS_PORT` | — | Required for `modbus-rtu` profile readiness |
| `HILLM_MQTT_URL` | — | Required for `mqtt-broker` profile readiness |
| `HILLM_<DEVICE_ID>_ADDRESS` | profile default | Per-device address override (`-` → `_`) |

Example:

```bash
export HILLM_DRY_RUN=1
export HILLM_SENSOR_TEMP_ADDRESS=/dev/ttyACM0
hillm read --device sensor-temp --dry-run
dsl2hillm 'READ DEVICE sensor-temp'              # dry-run when HILLM_DRY_RUN=1
dsl2hillm 'READ DEVICE sensor-temp' --dry-run    # explicit
nlp2hillm "read temperature from serial" --apply # dry-run by default
uri2hillm 'READ DEVICE sensor-temp'              # dry-run by default
```

## Device resolution

Natural-language keywords map to registry device ids via `hillm.resolve`:

| Input keyword | Device id |
| --- | --- |
| `temperature` + `serial` | `sensor-temp` |
| `mouse` (over `usb`) | `mouse-default` |
| `usb` (alone) | `usb-hub` |
| `camera` | `camera-usb` |
| `modbus` | `modbus-rtu` |

Unknown devices return suggestions: `unknown device: serial (try: sensor-temp, serial-ttyacm0, …)`.

## uri2hillm

Accepts full `hillm://` URI or DSL shorthand:

```bash
uri2hillm HEALTH
uri2hillm READ DEVICE sensor-temp          # dry-run by default
uri2hillm READ DEVICE sensor-temp --live
uri2hillm 'hillm://cmd/READ?device=camera-usb&dry_run=true'
uri2hillm decode READ DEVICE sensor-temp
uri2hillm run HEALTH
```

Bare `READ` without `DEVICE` returns a schema validation error (device is required).

Details: [control-layer.md](control-layer.md) · [packages/uri2hillm/README.md](../packages/uri2hillm/README.md)

## OpenRouter (nlp2hillm LLM)

When `OPENROUTER_API_KEY` is set in `.env`, `nlp2hillm` uses OpenRouter via `litellm` for **ambiguous** prompts. Clear patterns (e.g. temperature + serial → `sensor-temp`) always use rules. `--use-llm` forces LLM; `--no-llm` forces rules.

```bash
# .env
OPENROUTER_API_KEY=sk-or-v1-...
LLM_MODEL=openrouter/qwen/qwen3-coder-next

pip install -e packages/nlp2hillm[llm]
nlp2hillm "read temperature from serial"          # LLM if key present
nlp2hillm "read temperature from serial" --no-llm  # rules only
```

## nlp2hillm

```bash
nlp2hillm "read temperature from serial"           # → DSL only
nlp2hillm "read temperature from serial" --apply     # dry-run execute
nlp2hillm "read usb port for mouse" --apply --live # real input scan
```

Examples: [examples/nlp2hillm/](../examples/nlp2hillm/)

## REST port

`rest2hillm` listens on **8218** by default (gillm uses 8220, tillm uses 8216).

## Koru / nlp2uri

- Koru compat: `hillm.compat` exports `hillm_shell` backend profile.
- nlp2uri: `hillm://` URIs compile to `uri2hillm <uri>` when `pip install nlp2uri[hillm]`.
- Examples: [examples/nlp2uri/](../examples/nlp2uri/)

## See also

- [README.md](README.md) — documentation index
- [control-layer.md](control-layer.md) — `*2hillm` adapters
- [examples/README.md](../examples/README.md)
- [packages/README.md](../packages/README.md)
- [CHANGELOG.md](../CHANGELOG.md)
- [TODO.md](../TODO.md)
