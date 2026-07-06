# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `examples/cli/*` — status ecosystem, mouse dry-run, dsl health
- `examples/dsl/*` — read sensor-temp, devices usb
- `examples/control-layer/*` — uri shorthand/decode, nlp mouse port, dsl live policy
- `examples/devices/input/*` — mouse status live (`/dev/input/by-id`)
- `examples/devices/sensor/*` — temp read dry-run, status live, serial address resolve
- `examples/nlp2hillm/check-serial-env.sh` — install + port diagnostics
- `registry.first_existing_serial_path()` — auto-fallback `/dev/ttyACM0` when `/dev/ttyUSB0` missing
- `sensor-temp` `detect_paths` + serial port auto-resolve in `resolve_address()`
- `nlp2hillm -v` — resolved device address + package paths on stderr
- `pygments` in `[dev]`; `goal.yaml` test via `uv sync --all-packages --extra dev && uv run pytest`
- `nlp2hillm` OpenRouter LLM backend (`litellm`, `OPENROUTER_API_KEY` + `LLM_MODEL` z `.env`)
- `nlp2hillm --use-llm` / `--no-llm`; reguły jako fallback
- `hillm.resolve` — centralne mapowanie NL/alias → device id
- `registry.suggest_device_ids()` + `format_unknown_device()` — podpowiedzi przy błędach
- `apply_execution_policy()` — wspólna polityka dry-run/live dla wszystkich adapterów
- `uri2hillm` / `cli2hillm`: `--live`, `--dry-run`, domyślny dry-run przy wykonaniu (uri2hillm)
- `hillm.project_env` — auto-load `<project>/.env` in `hillm`, `dsl2hillm`, `nlp2hillm` CLIs and `dispatch()`
- `dsl2hillm --dry-run` and auto `DRY_RUN` when `HILLM_DRY_RUN=1` in `.env`
- `nlp2hillm --apply` defaults to dry-run; `--live` opts into real hardware
- `examples/nlp2hillm/*` — NL mapping and dry-run apply smoke scripts
- `uri2hillm` DSL shorthand: bare verbs (`HEALTH`), full DSL lines, `decode` / `run` subcommands
- `uri2hillm.uri.normalize_uri_input()` and `dsl_line_to_uri()` for URI ↔ DSL conversion
- `uri2hillm` tests in `packages/uri2hillm/tests/test_decode.py`
- Documentation index: [docs/README.md](docs/README.md), [docs/control-layer.md](docs/control-layer.md), [TODO.md](TODO.md)

### Changed
- `nlp2hillm.to_dsl` korzysta z `hillm.resolve` (jedno źródło mapowania urządzeń)
- Dokumentacja: [docs/README.md](docs/README.md), [docs/configuration.md](docs/configuration.md), [docs/control-layer.md](docs/control-layer.md), wszystkie package READMEs, [examples/README.md](examples/README.md)
- [TODO.md](TODO.md): wnioski z testów + plan refaktoryzacji
- [README.md](README.md): dry-run policy, architektura (`resolve`, `project_env`), `make test`

### Fixed
- `dsl2hillm` / `cli2hillm`: hardware verbs (`READ`, `WRITE`, …) default to dry-run (aligned with `nlp2hillm`, `uri2hillm`)
- Serial transport errors hint available port (`HILLM_<DEVICE>_ADDRESS=/dev/ttyACM0`) when default missing
- `sensor-temp` live read uses first existing serial port (fixes `/dev/ttyUSB0` on hosts with only `ttyACM0`)
- `goal -a` test failures from broken `.venv` (partial pytest/pygments installs) — use full `uv sync` in test strategy
- `nlp2hillm`: map `serial`/`usb` to registry IDs (`sensor-temp`, `mouse-default`); `read` wins over `port` keyword
- `uri2hillm READ` no longer fails with `unsupported URI scheme:` — input is normalized to `hillm://cmd/READ`

## [0.1.6] - 2026-07-06

### Docs
- Update README.md

### Other
- Update .hillm/events/app.hillm.events.jsonl

## [0.1.5] - 2026-06-29

### Docs
- Update README.md

### Other
- Update .hillm/events/app.hillm.events.jsonl

## [0.1.4] - 2026-06-29

### Docs
- Update README.md

### Other
- Update .hillm/events/app.hillm.events.jsonl

## [0.1.3] - 2026-06-09

### Docs
- Update CHANGELOG.md
- Update README.md
- Update TODO.md
- Update examples/README.md

### Test
- Update tests/test_examples.py

### Other
- Update .hillm/events/app.hillm.events.jsonl
- Update examples/cli/dsl-health.sh
- Update examples/cli/status-ecosystem.sh
- Update examples/cli/status-mouse-dry-run.sh
- Update examples/control-layer/dsl-live-policy.sh
- Update examples/control-layer/nlp-mouse-port.sh
- Update examples/control-layer/uri-decode-sensor.sh
- Update examples/control-layer/uri-shorthand-read.sh
- Update examples/devices/input/mouse-status-live.sh
- Update examples/devices/sensor/temp-read-dry-run.sh
- ... and 5 more files

## [0.1.2] - 2026-06-08

### Docs
- Update CHANGELOG.md
- Update README.md
- Update TODO.md
- Update docs/README.md
- Update docs/configuration.md
- Update docs/control-layer.md
- Update examples/README.md
- Update packages/README.md
- Update packages/cli2hillm/README.md
- Update packages/dsl2hillm/README.md
- ... and 4 more files

### Test
- Update tests/test_examples.py
- Update tests/test_hillm.py
- Update tests/test_project_env.py
- Update tests/test_registry_serial.py
- Update tests/test_resolve.py

### Other
- Update .gitignore
- Update .hillm/events/app.hillm.events.jsonl
- Update Makefile
- Update examples/control-layer/nlp-to-dsl.sh
- Update examples/env.example
- Update examples/nlp2hillm/apply-connect-modbus.sh
- Update examples/nlp2hillm/apply-env-dry-run.sh
- Update examples/nlp2hillm/apply-read-dry-run.sh
- Update examples/nlp2hillm/apply-status-mouse-dry-run.sh
- Update examples/nlp2hillm/apply-status-mouse-live.sh
- ... and 31 more files

## [0.1.1] - 2026-06-08

### Docs
- Update CHANGELOG.md
- Update README.md
- Update TODO.md
- Update docs/README.md
- Update docs/configuration.md
- Update docs/control-layer.md
- Update examples/README.md
- Update packages/README.md
- Update packages/cli2hillm/README.md
- Update packages/dsl2hillm/README.md
- ... and 4 more files

### Test
- Update testql-scenarios/generated-cli-tests.testql.toon.yaml
- Update tests/test_examples.py
- Update tests/test_hillm.py

### Other
- Update .gitignore
- Update .hillm/events/app.hillm.events.jsonl
- Update .idea/.gitignore
- Update Makefile
- Update VERSION
- Update app.doql.less
- Update examples/cli/devices.sh
- Update examples/cli/read-dry-run.sh
- Update examples/cli/scan.sh
- Update examples/cli/write-dry-run.sh
- ... and 64 more files

## [0.1.0] - 2026-06-08

### Added
- Initial HILLM scaffold: hardware device registry, transports, controller, CLI
- Control layer packages: `dsl2hillm`, `uri2hillm`, `nlp2hillm`, `cli2hillm`, `mcp2hillm`, `rest2hillm` (port **8218**)
- Device categories: display/HDMI, camera, audio, input, USB, serial, Modbus, MQTT, HTTP, GPIO
- Koru compat exports: `hillm_shell` backend profile and tool registry entries
- Package READMEs, [docs/configuration.md](docs/configuration.md), [examples/*/*](examples/), `tests/test_examples.py`
- nlp2uri integration via `hillm://` URIs (`nlp2uri[hillm]`)

### Fixed
- `VALIDATE` DSL schema (device optional for ecosystem validate)
