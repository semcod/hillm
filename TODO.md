# TODO

Wnioski z praktycznych testów (2026-06-08) — co psuło UX i co zostało naprawione:

| Problem | Przyczyna | Status |
|---------|-----------|--------|
| `uri2hillm READ` → `unsupported URI scheme` | CLI wymagał pełnego `hillm://` | [x] shorthand DSL |
| `nlp2hillm` → `unknown device: serial/usb` | słowa kluczowe ≠ ID rejestru | [x] `hillm.resolve` |
| `nlp2hillm --apply` → błąd `/dev/ttyUSB0` | brak domyślnego dry-run | [x] `--apply` = dry-run |
| `dsl2hillm` bez `DRY_RUN` → real serial | brak `.env` / flagi | [x] `--dry-run`, auto `.env` |
| Niespójne flagi między adapterami | każdy CLI osobno | [x] `apply_execution_policy()` |
| `unknown device` bez podpowiedzi | brak suggest w registry | [x] `suggest_device_ids()` |

## Refaktoryzacja — wykonane

- [x] `hillm.project_env` — `.env`, `apply_execution_policy()`, `with_dry_run()`
- [x] `hillm.resolve` — centralne mapowanie NL → device id
- [x] `registry.suggest_device_ids()` + `format_unknown_device()`
- [x] Ujednolicone flagi `--dry-run` / `--live` w `dsl2hillm`, `nlp2hillm`, `uri2hillm`, `cli2hillm`
- [x] `uri2hillm` domyślny dry-run przy wykonaniu (bez `--live`)
- [x] `examples/nlp2hillm/*` — smoke testy NL → DSL → apply
- [x] `examples/cli/*`, `examples/dsl/*`, `examples/control-layer/*` — rozszerzone smoke skrypty
- [x] `examples/devices/{input,sensor}/*` — mouse live, sensor-temp resolve + status
- [x] `registry` serial auto-fallback (`ttyACM0` / `ttyUSB0`)
- [x] `goal.yaml` — test przez `uv sync` + `uv run pytest` (nie sam `pytest`)
- [x] Testy: resolve, execution policy, suggest devices, registry serial (70+)

## Kolejne kroki (plan)

### Stabilność runtime

- [x] Serial port auto-fallback w `resolve_address()` (`sensor-temp` → pierwszy istniejący `/dev/tty*`)
- [ ] Auto-fallback dry-run gdy urządzenie `not ready` (port/moduł niedostępny) zamiast błędu
- [ ] Parser/komenda odczytu temperatury per protokół czujnika (obecnie surowy serial read)
- [ ] `hillm devices --ready` — filtr gotowych profili w CLI
- [ ] Walidacja `READ`/`WRITE` z podpowiedzią `suggest_device_ids` już w `dsl2hillm` (przed dispatch)

### Control layer

- [ ] `rest2hillm`: query param `?dry_run=true` / header `X-Hillm-Dry-Run`
- [ ] `rest2hillm` live server smoke w CI
- [ ] MCP: pokrycie wszystkich query verbs
- [ ] `uri2hillm READ` bez `DEVICE` → komunikat z listą urządzeń

### Transports & devices

- [ ] Real GPIO backend (platform-specific)
- [ ] Live integration tests: serial, Modbus RTU/TCP, MQTT
- [ ] Per-category docs: `docs/devices/{display,camera,serial,modbus,mqtt}.md`

### DevEx

- [x] Rozszerzone `examples/*/*` + podlinkowanie w [README.md](README.md) i [examples/README.md](examples/README.md)
- [ ] `examples/env.example` merge hint w README (dodać `HILLM_DRY_RUN=1` do istniejącego `.env`)
- [ ] Ujednolicić `venv` vs `.venv` w dokumentacji (`uv sync --active`)
- [ ] `make lint` / ruff cleanup
- [ ] Publish `hillm` + `*2hillm` na PyPI

### Dokumentacja

- [x] Tabela polityki dry-run per adapter w [docs/control-layer.md](docs/control-layer.md)
- [x] [docs/configuration.md](docs/configuration.md) — `.env`, device resolution, nlp2hillm
- [x] Package READMEs — `--live` / `--dry-run` we wszystkich adapterach
- [ ] `SUMD.md` — DSL verbs + device registry
- [ ] Per-category docs: `docs/devices/{display,camera,serial,modbus,mqtt}.md`

**See also:** [CHANGELOG.md](CHANGELOG.md) · [README.md](README.md) · [docs/README.md](docs/README.md)
