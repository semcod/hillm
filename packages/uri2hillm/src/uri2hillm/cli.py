from __future__ import annotations

import argparse
import json
import sys

from uri2hillm.decode import uri_to_dsl
from uri2hillm.run import run_uri
from uri2hillm.uri import normalize_uri_input


def _target(argv: list[str]) -> str:
    return " ".join(argv).strip()


def _print_help() -> None:
    parser = argparse.ArgumentParser(
        prog="uri2hillm",
        description="Run hillm commands from hillm:// URIs or DSL shorthand.",
    )
    parser.print_help()
    print(
        "\nExamples:\n"
        "  uri2hillm HEALTH\n"
        "  uri2hillm READ DEVICE sensor-temp DRY_RUN true\n"
        "  uri2hillm 'hillm://cmd/READ?device=camera-usb&dry_run=true'\n"
        "  uri2hillm decode READ DEVICE sensor-temp\n"
        "  uri2hillm run HEALTH\n"
    )


def main(argv: list[str] | None = None) -> int:
    argv = list(argv if argv is not None else sys.argv[1:])
    if not argv or argv == ["-h"] or argv == ["--help"]:
        _print_help()
        return 0

    if argv[0] == "decode":
        parser = argparse.ArgumentParser(prog="uri2hillm decode")
        parser.add_argument("target", nargs="+", help="hillm:// URI or DSL line")
        parser.add_argument("--file", default="")
        args = parser.parse_args(argv[1:])
        target = _target(args.target)
        default_file = args.file or None
        uri = normalize_uri_input(target, default_file=default_file)
        print(uri_to_dsl(uri, default_file=default_file))
        return 0

    if argv[0] == "run":
        parser = argparse.ArgumentParser(prog="uri2hillm run")
        parser.add_argument("target", nargs="+", help="hillm:// URI or DSL line")
        parser.add_argument("--file", default="")
        parser.add_argument("--json", action="store_true")
        args = parser.parse_args(argv[1:])
        target = _target(args.target)
        default_file = args.file or None
        uri = normalize_uri_input(target, default_file=default_file)
        result = run_uri(uri, default_file=default_file)
        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print(result.output or result.error)
        return 0 if result.ok else 1

    parser = argparse.ArgumentParser(prog="uri2hillm")
    parser.add_argument("target", nargs="+", help="hillm:// URI or DSL line")
    parser.add_argument("--file", default="")
    args = parser.parse_args(argv)
    target = _target(args.target)
    default_file = args.file or None
    uri = normalize_uri_input(target, default_file=default_file)
    result = run_uri(uri, default_file=default_file)
    print(json.dumps(result.to_dict(), indent=2))
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
