from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from dsl2hillm.codec import parse_text, validate_payload
from dsl2hillm.events import EventStore
from dsl2hillm.result import DslResult
from dsl2hillm.schema_registry import COMMAND_VERBS, QUERY_VERBS


def dispatch(
    command: str | dict[str, Any],
    *,
    default_file: str | None = None,
    workdir: Path | None = None,
) -> DslResult:
    raw_line = ""
    try:
        if isinstance(command, dict):
            payload = validate_payload(command)
            raw_line = json.dumps(payload, ensure_ascii=False)
        else:
            raw_line = command
            payload = parse_text(command, default_file=default_file)
            if not payload:
                return DslResult(ok=True, command=raw_line, verb="noop")

        verb = str(payload["verb"]).upper()
        root = (workdir or Path(".")).expanduser().resolve()

        if verb in QUERY_VERBS:
            from dsl2hillm.handlers import run_query

            result = run_query(payload, workdir=root)
            return DslResult(
                ok=result.ok,
                verb=verb,
                command=raw_line,
                output=result.output,
                data=result.data,
                error=result.error,
            )

        if verb in COMMAND_VERBS:
            from dsl2hillm.handlers import run_command

            result = run_command(payload, workdir=root)
            event_id = None
            if result.ok:
                store = EventStore.for_workdir(root)
                event_id = store.append_command(payload, result.to_dict())
            return DslResult(
                ok=result.ok,
                verb=verb,
                command=raw_line,
                output=result.output,
                data=result.data,
                error=result.error,
                event_id=event_id,
            )

        return DslResult(ok=False, verb=verb, command=raw_line, error=f"unsupported verb: {verb}")
    except Exception as exc:
        return DslResult(ok=False, command=raw_line or str(command), error=str(exc))


def execute_dsl_line(line: str, *, default_file: str | None = None) -> DslResult:
    return dispatch(line, default_file=default_file)
