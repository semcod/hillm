# hillm — Hardware Interface LLM


## AI Cost Tracking

![PyPI](https://img.shields.io/badge/pypi-costs-blue) ![Version](https://img.shields.io/badge/version-0.1.1-blue) ![Python](https://img.shields.io/badge/python-3.9+-blue) ![License](https://img.shields.io/badge/license-Apache--2.0-green)
![AI Cost](https://img.shields.io/badge/AI%20Cost-$0.15-orange) ![Human Time](https://img.shields.io/badge/Human%20Time-1.0h-blue) ![Model](https://img.shields.io/badge/Model-openrouter%2Fqwen%2Fqwen3--coder--next-lightgrey)

- 🤖 **LLM usage:** $0.1500 (1 commits)
- 👤 **Human dev:** ~$100 (1.0h @ $100/h, 30min dedup)

Generated on 2026-06-08 using [openrouter/qwen/qwen3-coder-next](https://openrouter.ai/qwen/qwen3-coder-next)

---

Control platform hardware through a unified registry and transport layer:

- **Displays / HDMI** — `xrandr`, `wlr-randr`
- **Cameras** — V4L (`/dev/video*`)
- **Audio** — microphones / speakers via PulseAudio
- **Input** — keyboard / mouse discovery (`/dev/input`)
- **USB** — `lsusb` enumeration
- **Serial / RS232 / RS485** — `pyserial`
- **Modbus RTU/TCP** — `pymodbus`
- **MQTT / HTTP** — network device gateways

Pairs with:

| Package | Role |
|---------|------|
| [`gillm`](../gillm/) | GUI / IDE keyboard injection |
| [`tillm`](../tillm/) | Shell LLM clients (aider, codex, …) |
| **`hillm`** | Physical devices and field interfaces |

## Install

```bash
cd /home/tom/github/semcod/hillm
make install-dev          # uv sync + control layer (recommended)
make install-transports   # + serial/modbus/mqtt
make help                 # all targets
```

Or manually:

```bash
pip install -e .
pip install -e ".[serial,modbus,mqtt]"   # optional transports
bash packages/install-dev.sh             # all *2hillm adapters
```

## CLI

```bash
hillm devices
hillm scan
hillm read --device camera-usb --dry-run
hillm write --device actuator-relay --value 1 --register coil:0 --dry-run
hillm actuate --device display-primary --action on
hillm status --ecosystem
```

## DSL / integrations

```bash
dsl2hillm HEALTH
dsl2hillm 'READ DEVICE sensor-temp DRY_RUN true'
uri2hillm HEALTH
uri2hillm READ DEVICE sensor-temp DRY_RUN true
uri2hillm 'hillm://cmd/READ?device=camera-usb&dry_run=true'
nlp2hillm "read temperature from serial" --apply
rest2hillm --port 8218   # in another terminal
curl -X POST http://127.0.0.1:8218/v1/dsl -d HEALTH
# nlp2uri: pip install nlp2uri[hillm]
uri2hillm 'hillm://cmd/HEALTH'
```

See [docs/control-layer.md](docs/control-layer.md) for adapter details.

## Architecture

```
hillm (core)
  registry.py      — declarative device catalog
  controller.py    — read / write / actuate / connect
  transports/      — serial, modbus, mqtt, display, v4l, audio, usb, …
  compat.py        — Koru backend + tool registry exports

packages/
  dsl2hillm        — CQRS bus (single mutation point)
  uri2hillm        — hillm:// URI adapter
  nlp2hillm        — NL → DSL
  cli2hillm        — shell passthrough
  mcp2hillm        — MCP tools
  rest2hillm       — REST API (:8218)
```

## Examples

```bash
bash packages/install-dev.sh
cp examples/env.example .env    # optional
bash examples/run-all-dry-run.sh
```

See [examples/README.md](examples/README.md) for per-device and control-layer scripts.

## Tests

```bash
bash packages/install-dev.sh
python -m pytest tests/ packages/dsl2hillm/tests packages/uri2hillm/tests -q
```

## Documentation

| Doc | Content |
|-----|---------|
| [docs/README.md](docs/README.md) | Documentation index |
| [docs/configuration.md](docs/configuration.md) | Env vars, install profiles, ports |
| [docs/control-layer.md](docs/control-layer.md) | `*2hillm` adapters (DSL, URI, REST, MCP) |
| [packages/README.md](packages/README.md) | Control layer package matrix |
| [examples/README.md](examples/README.md) | Runnable smoke scripts |
| [CHANGELOG.md](CHANGELOG.md) | Release history |
| [TODO.md](TODO.md) | Roadmap and open items |

## Environment

| Variable | Purpose |
|----------|---------|
| `HILLM_DRY_RUN` | Force dry-run transport globally |
| `HILLM_MODBUS_HOST` | Default Modbus TCP host |
| `HILLM_MQTT_URL` | Default MQTT broker URL |
| `HILLM_<DEVICE>_ADDRESS` | Per-device address override |

## License

Licensed under Apache-2.0.
