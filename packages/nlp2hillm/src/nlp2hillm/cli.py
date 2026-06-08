from __future__ import annotations

import argparse
import json
import sys

from dsl2hillm import dispatch
from nlp2hillm.to_dsl import to_dsl


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="nlp2hillm")
    parser.add_argument("prompt", nargs="?", help="Natural language hardware command")
    parser.add_argument("--apply", action="store_true", help="Execute mapped DSL")
    args = parser.parse_args(argv)
    if not args.prompt:
        parser.print_help()
        return 2
    line = to_dsl(args.prompt)
    if not args.apply:
        print(line)
        return 0
    result = dispatch(line)
    print(json.dumps(result.to_dict(), indent=2))
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
