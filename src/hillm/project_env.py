"""Bootstrap project environment from `.env`."""

from __future__ import annotations

import os
import re
from pathlib import Path

_ENV_LINE = re.compile(r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$")


def _strip_quotes(value: str) -> str:
    text = value.strip()
    if (text.startswith('"') and text.endswith('"')) or (text.startswith("'") and text.endswith("'")):
        return text[1:-1]
    return text


def load_env_file(path: Path) -> dict[str, str]:
    if not path.is_file():
        return {}
    values: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        match = _ENV_LINE.match(line)
        if not match:
            continue
        key, value = match.group(1), _strip_quotes(match.group(2))
        values[key] = value
    return values


def apply_into_environ(values: dict[str, str], *, overwrite: bool = False) -> list[str]:
    applied: list[str] = []
    for key, value in values.items():
        if not overwrite and key in os.environ and os.environ[key].strip():
            continue
        os.environ[key] = value
        applied.append(key)
    return applied


def find_project_env(project: Path | None = None) -> Path | None:
    root = (project or Path.cwd()).resolve()
    for candidate in (root, *root.parents):
        env_file = candidate / ".env"
        if env_file.is_file():
            return env_file
    return None


def bootstrap_project_env(project: Path | None = None) -> Path | None:
    env_file = find_project_env(project)
    if env_file is None:
        return None
    apply_into_environ(load_env_file(env_file))
    return env_file.parent


def env_dry_run() -> bool:
    return os.environ.get("HILLM_DRY_RUN", "").strip().lower() in {"1", "true", "yes", "on"}


def with_dry_run(line: str, *, dry_run: bool) -> str:
    if dry_run and "DRY_RUN" not in line.upper():
        return f"{line} DRY_RUN true"
    return line


HARDWARE_VERBS = frozenset(
    {"READ", "WRITE", "ACTUATE", "CONNECT", "DISCONNECT", "STATUS", "EXECUTE"},
)


def hardware_verb(line: str) -> str:
    stripped = line.strip()
    if not stripped:
        return ""
    return stripped.split()[0].upper()


def is_hardware_line(line: str) -> bool:
    return hardware_verb(line) in HARDWARE_VERBS


def apply_execution_policy(
    line: str,
    *,
    live: bool = False,
    dry_run: bool = False,
    respect_env: bool = True,
    default_hardware_dry_run: bool = False,
) -> str:
    """Apply dry-run policy before dispatch.

    - ``live=True`` — leave line unchanged
    - ``dry_run=True`` — append DRY_RUN true
    - ``respect_env=True`` — also dry-run when HILLM_DRY_RUN=1
    - ``default_hardware_dry_run=True`` — dry-run for READ/WRITE/… when not live
    """
    if live:
        return line
    use_dry = (
        dry_run
        or (respect_env and env_dry_run())
        or (default_hardware_dry_run and is_hardware_line(line))
    )
    return with_dry_run(line, dry_run=use_dry)
