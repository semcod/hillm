# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `uri2hillm` DSL shorthand: bare verbs (`HEALTH`), full DSL lines, `decode` / `run` subcommands
- `uri2hillm.uri.normalize_uri_input()` and `dsl_line_to_uri()` for URI ↔ DSL conversion
- `uri2hillm` tests in `packages/uri2hillm/tests/test_decode.py`
- Documentation index: [docs/README.md](docs/README.md), [docs/control-layer.md](docs/control-layer.md), [TODO.md](TODO.md)

### Changed
- [README.md](README.md): `uri2hillm` examples, documentation links
- [docs/configuration.md](docs/configuration.md): `uri2hillm` usage, cross-links
- [packages/README.md](packages/README.md): control layer quick reference

### Fixed
- `uri2hillm READ` no longer fails with `unsupported URI scheme:` — input is normalized to `hillm://cmd/READ`

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
