from __future__ import annotations

import argparse
import json
import sys

from cli2hillm.shell import hillm_cli_argv, run_shell_command
from dsl2hillm import dispatch
from hillm.project_env import apply_execution_policy, bootstrap_project_env


def main(argv: list[str] | None = None) -> int:
    bootstrap_project_env()
    parser = argparse.ArgumentParser(prog="cli2hillm")
    parser.add_argument("command", nargs="?", help="DSL line or hillm subcommand")
    parser.add_argument("--shell", action="store_true", help="Run via hillm CLI instead of DSL bus")
    parser.add_argument("--dry-run", action="store_true", help="Append DRY_RUN true to DSL command")
    parser.add_argument("--live", action="store_true", help="Use real hardware transports")
    args = parser.parse_args(argv)
    if not args.command:
        parser.print_help()
        return 2
    if args.shell:
        return run_shell_command(hillm_cli_argv(args.command))
    line = apply_execution_policy(
        args.command,
        live=args.live,
        dry_run=args.dry_run,
        respect_env=not args.live,
        default_hardware_dry_run=not args.live,
    )
    result = dispatch(line)
    print(json.dumps(result.to_dict(), indent=2))
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
