from __future__ import annotations

import shlex
import subprocess
from typing import Sequence


def run_shell_command(argv: Sequence[str], *, cwd: str | None = None) -> int:
    return subprocess.call(list(argv), cwd=cwd)


def hillm_cli_argv(line: str) -> list[str]:
    tokens = shlex.split(line)
    if tokens and tokens[0] == "hillm":
        return tokens
    return ["hillm", *tokens]
