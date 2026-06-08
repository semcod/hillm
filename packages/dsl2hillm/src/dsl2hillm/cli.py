from __future__ import annotations

import argparse
import json
import sys
from typing import Sequence

from dsl2hillm.bus import dispatch
from hillm.project_env import apply_execution_policy, bootstrap_project_env


def main(argv: Sequence[str] | None = None) -> int:
    bootstrap_project_env()
    parser = argparse.ArgumentParser(prog="dsl2hillm")
    parser.add_argument("line", nargs="?", help="DSL line, e.g. 'HEALTH' or 'READ DEVICE camera-usb'")
    parser.add_argument("--file", help="Default project file for relative paths")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Append DRY_RUN true (also when HILLM_DRY_RUN=1 in .env)",
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Use real hardware transports (skip dry-run defaults)",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)
    if not args.line:
        parser.print_help()
        return 2
    line = apply_execution_policy(
        args.line,
        live=args.live,
        dry_run=args.dry_run,
        respect_env=not args.live,
        default_hardware_dry_run=not args.live,
    )
    result = dispatch(line, default_file=args.file)
    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
