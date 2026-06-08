from __future__ import annotations

import json
from unittest.mock import patch

from uri2hillm.run import run_uri


def test_run_uri_defaults_to_dry_run() -> None:
    with patch.dict("os.environ", {}, clear=True):
        result = run_uri("hillm://cmd/READ?device=sensor-temp", dry_run=True)
    assert result.ok
    assert result.data["backend"] == "dry_run"
