from __future__ import annotations

import json
from unittest.mock import patch

from nlp2hillm.cli import main


def test_apply_defaults_to_dry_run(capsys) -> None:
    with patch.dict("os.environ", {}, clear=True):
        code = main(["read temperature from serial", "--apply"])
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["ok"]
    assert payload["command"] == "READ DEVICE sensor-temp REGISTER temperature DRY_RUN true"
    assert payload["data"]["backend"] == "dry_run"


def test_apply_dry_run_flag_appends_to_command(capsys) -> None:
    with patch.dict("os.environ", {}, clear=True):
        code = main(["read temperature from serial", "--apply", "--dry-run"])
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["ok"]
    assert "DRY_RUN true" in payload["command"]


def test_apply_live_skips_dry_run(capsys) -> None:
    with patch.dict("os.environ", {}, clear=True):
        code = main(["read usb port for mouse", "--apply", "--live"])
    payload = json.loads(capsys.readouterr().out)
    assert "DRY_RUN" not in payload["command"]
    # mouse-default uses input transport; may succeed without serial hardware
    assert payload["verb"] == "READ"
