from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from hillm.project_env import (
    apply_execution_policy,
    apply_into_environ,
    bootstrap_project_env,
    env_dry_run,
    with_dry_run,
)


def test_with_dry_run_appends_flag() -> None:
    assert with_dry_run("READ DEVICE sensor-temp", dry_run=True) == "READ DEVICE sensor-temp DRY_RUN true"
    assert with_dry_run("READ DEVICE sensor-temp DRY_RUN true", dry_run=True) == "READ DEVICE sensor-temp DRY_RUN true"


def test_bootstrap_project_env_loads_dotenv(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("HILLM_DRY_RUN", raising=False)
    (tmp_path / ".env").write_text("HILLM_DRY_RUN=1\n", encoding="utf-8")
    loaded = bootstrap_project_env()
    assert loaded == tmp_path
    assert env_dry_run()


def test_apply_execution_policy_live_skips_dry_run() -> None:
    line = apply_execution_policy("READ DEVICE sensor-temp", live=True)
    assert line == "READ DEVICE sensor-temp"


def test_apply_execution_policy_forces_dry_run() -> None:
    line = apply_execution_policy("READ DEVICE sensor-temp", dry_run=True)
    assert line.endswith("DRY_RUN true")


def test_apply_execution_policy_defaults_hardware_dry_run() -> None:
    with patch.dict("os.environ", {}, clear=True):
        line = apply_execution_policy(
            "READ DEVICE sensor-temp",
            default_hardware_dry_run=True,
        )
    assert line.endswith("DRY_RUN true")


def test_apply_execution_policy_skips_health_default() -> None:
    with patch.dict("os.environ", {}, clear=True):
        line = apply_execution_policy(
            "HEALTH",
            default_hardware_dry_run=True,
        )
    assert line == "HEALTH"


def test_apply_into_environ_respects_existing(monkeypatch) -> None:
    monkeypatch.setenv("HILLM_DRY_RUN", "0")
    apply_into_environ({"HILLM_DRY_RUN": "1"})
    assert env_dry_run() is False
