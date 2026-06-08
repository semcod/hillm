from __future__ import annotations

import json
from unittest.mock import patch

from dsl2hillm.cli import main


def test_cli_defaults_hardware_to_dry_run(capsys) -> None:
    with patch.dict("os.environ", {}, clear=True):
        code = main(["READ DEVICE sensor-temp"])
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["ok"]
    assert payload["command"] == "READ DEVICE sensor-temp DRY_RUN true"
    assert payload["data"]["backend"] == "dry_run"


def test_cli_dry_run_flag(capsys) -> None:
    with patch.dict("os.environ", {}, clear=True):
        code = main(["READ DEVICE sensor-temp", "--dry-run"])
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["ok"]
    assert "DRY_RUN true" in payload["command"]


def test_cli_live_skips_dry_run(capsys) -> None:
    with patch.dict("os.environ", {}, clear=True):
        code = main(["READ DEVICE sensor-temp", "--live"])
    payload = json.loads(capsys.readouterr().out)
    assert "DRY_RUN" not in payload["command"]


def test_cli_health_unchanged_without_env(capsys) -> None:
    with patch.dict("os.environ", {}, clear=True):
        code = main(["HEALTH"])
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["ok"]
    assert payload["command"] == "HEALTH"
