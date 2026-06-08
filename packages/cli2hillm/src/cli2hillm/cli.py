from __future__ import annotations

import argparse
import json
import sys

from cli2hillm.shell import hillm_cli_argv, run_shell_command
from dsl2hillm import dispatch


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="cli2hillm")
    parser.add_argument("command", nargs="?", help="DSL line or hillm subcommand")
    parser.add_argument("--shell", action="store_true", help="Run via hillm CLI instead of DSL bus")
    args = parser.parse_args(argv)
    if not args.command:
        parser.print_help()
        return 2
    if args.shell:
        return run_shell_command(hillm_cli_argv(args.command))
    result = dispatch(args.command)
    print(json.dumps(result.to_dict(), indent=2))
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
